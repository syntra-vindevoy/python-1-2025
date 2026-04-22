import fitparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict, List, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time


def quick_fit_file_check(fit_file_path: str) -> Dict[str, any]:
    """
    Ultra-fast FIT file type detection - only reads first few messages
    """
    try:
        fitfile = fitparse.FitFile(fit_file_path)

        message_counts = {}
        messages_checked = 0
        max_messages_to_check = 10  # Only check first 10 messages for speed

        # Quick scan of first few messages only
        for message in fitfile.get_messages():
            msg_type = message.name
            message_counts[msg_type] = message_counts.get(msg_type, 0) + 1

            messages_checked += 1
            if messages_checked >= max_messages_to_check:
                break

        # Quick determination based on partial scan
        has_records = 'record' in message_counts
        has_sessions = 'session' in message_counts
        has_monitoring = 'monitoring' in message_counts

        is_activity_file = has_records or has_sessions

        return {
            'file_path': fit_file_path,
            'filename': os.path.basename(fit_file_path),
            'is_activity_file': is_activity_file,
            'is_monitoring_file': has_monitoring,
            'quick_scan': True,
            'messages_scanned': messages_checked
        }

    except Exception as e:
        return {
            'file_path': fit_file_path,
            'filename': os.path.basename(fit_file_path),
            'is_activity_file': False,
            'is_monitoring_file': False,
            'error': str(e)
        }


def parallel_scan_directory(directory_path: str, max_workers: int = 4) -> Dict:
    """
    Parallel scanning of directory for much faster processing
    """
    print(f"⚡ FAST SCANNING DIRECTORY: {directory_path}")
    print("=" * 60)

    # Find all .fit files first
    all_fit_files = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.fit'):
            fit_path = os.path.join(directory_path, filename)
            all_fit_files.append(fit_path)

    print(f"Found {len(all_fit_files)} FIT files. Quick-scanning in parallel...")

    start_time = time.time()

    # Use ThreadPoolExecutor for I/O bound operations
    activity_files = []
    monitoring_files = []
    unknown_files = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all files for parallel processing
        future_to_file = {executor.submit(quick_fit_file_check, fit_path): fit_path
                          for fit_path in all_fit_files}

        for future in future_to_file:
            try:
                file_info = future.result(timeout=5)  # 5 second timeout per file

                if 'error' in file_info:
                    unknown_files.append(file_info)
                elif file_info['is_activity_file']:
                    activity_files.append(file_info)
                elif file_info['is_monitoring_file']:
                    monitoring_files.append(file_info)
                else:
                    unknown_files.append(file_info)

            except Exception as e:
                filename = future_to_file[future]
                unknown_files.append({
                    'file_path': filename,
                    'filename': os.path.basename(filename),
                    'error': f"Timeout or error: {str(e)}"
                })

    scan_time = time.time() - start_time

    print(f"\n⚡ FAST SCAN COMPLETE ({scan_time:.1f}s):")
    print(f"   ✅ Activity files: {len(activity_files)}")
    print(f"   ⏰ Monitoring files: {len(monitoring_files)}")
    print(f"   ❓ Unknown/Error files: {len(unknown_files)}")

    return {
        'activity_files': activity_files,
        'monitoring_files': monitoring_files,
        'unknown_files': unknown_files,
        'scan_time': scan_time
    }


class FastActivityParser:
    """
    Optimized parser that only extracts essential data quickly
    """

    def __init__(self, fit_file_path: str):
        self.fit_file_path = fit_file_path
        self.fitfile = fitparse.FitFile(fit_file_path)

    def fast_extract(self) -> Dict:
        """
        Fast extraction - only get essential data, skip detailed processing
        """
        records = []
        session_info = {}

        # Pre-allocate lists for speed
        timestamps = []
        heart_rates = []
        speeds = []
        latitudes = []
        longitudes = []
        altitudes = []
        distances = []

        # Fast record extraction - use lists instead of dicts
        record_count = 0
        for record in self.fitfile.get_messages('record'):
            record_data = {}

            for field in record:
                field_name = field.name
                field_value = field.value

                # Only extract most important fields for speed
                if field_name == 'timestamp':
                    timestamps.append(field_value)
                    record_data['timestamp'] = field_value
                elif field_name == 'heart_rate' and field_value is not None:
                    heart_rates.append(field_value)
                    record_data['heart_rate'] = field_value
                elif field_name == 'speed' and field_value is not None:
                    speeds.append(field_value)
                    record_data['speed'] = field_value
                elif field_name == 'position_lat' and field_value is not None:
                    lat = field_value * (180.0 / (2 ** 31))
                    latitudes.append(lat)
                    record_data['latitude'] = lat
                elif field_name == 'position_long' and field_value is not None:
                    lon = field_value * (180.0 / (2 ** 31))
                    longitudes.append(lon)
                    record_data['longitude'] = lon
                elif field_name == 'altitude' and field_value is not None:
                    altitudes.append(field_value)
                    record_data['altitude'] = field_value
                elif field_name == 'distance' and field_value is not None:
                    distances.append(field_value)
                    record_data['distance'] = field_value

            if record_data:  # Only add if we got some data
                records.append(record_data)
                record_count += 1

                # Limit records for very large files to keep it fast
                if record_count > 50000:  # Stop at 50k records for speed
                    break

        # Fast session info extraction - only get key fields
        for session in self.fitfile.get_messages('session'):
            for field in session:
                field_name = field.name
                field_value = field.value

                # Only extract essential session info
                if field_name in ['start_time', 'total_elapsed_time', 'total_distance', 'sport']:
                    session_info[field_name] = field_value

        # Quick stats calculation using numpy for speed
        quick_stats = {}
        if heart_rates:
            hr_array = np.array(heart_rates)
            quick_stats['heart_rate'] = {
                'count': len(hr_array),
                'mean': float(np.mean(hr_array)),
                'min': float(np.min(hr_array)),
                'max': float(np.max(hr_array))
            }

        if speeds:
            speed_array = np.array(speeds)
            quick_stats['speed_kmh'] = {
                'count': len(speed_array),
                'mean': float(np.mean(speed_array) * 3.6),
                'min': float(np.min(speed_array) * 3.6),
                'max': float(np.max(speed_array) * 3.6)
            }

        if latitudes and longitudes:
            quick_stats['gps'] = {
                'points': len(latitudes),
                'lat_range': [float(np.min(latitudes)), float(np.max(latitudes))],
                'lon_range': [float(np.min(longitudes)), float(np.max(longitudes))]
            }

        return {
            'file_path': self.fit_file_path,
            'records': records,
            'session_info': session_info,
            'quick_stats': quick_stats,
            'record_count': len(records),
            'records_df': pd.DataFrame(records) if records else pd.DataFrame()
        }


def fast_export_csv(data: Dict, fit_file_path: str) -> Optional[str]:
    """
    Fast CSV export with minimal processing
    """
    df = data['records_df']
    if df.empty:
        return None

    base_name = os.path.splitext(os.path.basename(fit_file_path))[0]
    csv_file = f"{base_name}_FAST_export.csv"

    # Use fast CSV export
    df.to_csv(csv_file, index=False)
    return csv_file


def create_quick_plots(df: pd.DataFrame, filename: str):
    """
    Create basic plots quickly with minimal processing
    """
    if df.empty:
        return

    # Only plot if we have reasonable amount of data points
    if len(df) < 10:
        print(f"   ⚠️  Too few data points ({len(df)}) for plotting")
        return

    # Find available numeric columns quickly
    available_fields = []
    for field in ['heart_rate', 'speed', 'altitude', 'distance']:
        if field in df.columns and df[field].notna().sum() > 10:
            available_fields.append(field)

    if not available_fields:
        print(f"   ⚠️  No suitable data for plotting")
        return

    # Create simple, fast plot
    n_plots = min(len(available_fields), 2)  # Max 2 plots for speed

    fig, axes = plt.subplots(1, n_plots, figsize=(12, 4))
    if n_plots == 1:
        axes = [axes]

    for i, field in enumerate(available_fields[:n_plots]):
        data = df[field].dropna()
        if len(data) > 0:
            # Simple line plot - fastest option
            axes[i].plot(data.values, alpha=0.8, linewidth=1)
            axes[i].set_title(f'{field.replace("_", " ").title()}')
            axes[i].set_ylabel(field)
            axes[i].grid(True, alpha=0.3)

    plt.suptitle(f'Quick Analysis: {os.path.splitext(filename)[0]}', fontsize=12)
    plt.tight_layout()

    # Save plot quickly
    plot_file = f"{os.path.splitext(filename)[0]}_quick_plot.png"
    plt.savefig(plot_file, dpi=100, bbox_inches='tight')  # Lower DPI for speed
    plt.show()

    return plot_file


def parallel_process_activities(activity_files: List[Dict], max_workers: int = 2) -> List[str]:
    """
    Process multiple activity files in parallel
    """
    print(f"\n⚡ FAST PROCESSING {len(activity_files)} ACTIVITY FILES:")

    def process_single_activity(file_info):
        try:
            print(f"   Processing: {file_info['filename']}")

            # Fast parsing
            parser = FastActivityParser(file_info['file_path'])
            data = parser.fast_extract()

            # Quick export
            csv_file = fast_export_csv(data, file_info['file_path'])

            # Basic stats
            stats = {
                'filename': file_info['filename'],
                'records': data['record_count'],
                'csv_file': csv_file,
                'stats': data['quick_stats']
            }

            return stats

        except Exception as e:
            return {
                'filename': file_info['filename'],
                'error': str(e)
            }

    # Process in parallel for speed
    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_activity, file_info)
                   for file_info in activity_files]

        for future in futures:
            try:
                result = future.result(timeout=30)  # 30 second timeout
                results.append(result)
            except Exception as e:
                results.append({'error': f"Processing failed: {e}"})

    process_time = time.time() - start_time
    print(f"\n⚡ PARALLEL PROCESSING COMPLETE ({process_time:.1f}s)")

    return results


def main():
    """
    Super-fast main function optimized for speed
    """
    directory_path = r"C:\Users\robin\PycharmProjects\rvo_garmin\DI_CONNECT\DI-Connect-Uploaded-Files\UploadedFiles_0-_Part1"

    print("⚡ ULTRA-FAST FIT FILE ANALYZER")
    print("=" * 60)
    print("🚀 Optimized for maximum speed!")
    print("=" * 60)

    total_start = time.time()

    try:
        # Step 1: Fast parallel directory scan
        scan_results = parallel_scan_directory(directory_path, max_workers=6)

        activity_files = scan_results['activity_files']
        monitoring_files = scan_results['monitoring_files']

        if not activity_files:
            print(f"\n❌ NO ACTIVITY FILES FOUND!")
            print(f"   Found {len(monitoring_files)} monitoring files (skipped)")
            return

        print(f"\n🎉 FOUND {len(activity_files)} ACTIVITY FILES!")

        # Step 2: Fast parallel processing
        results = parallel_process_activities(activity_files, max_workers=3)

        # Step 3: Quick summary
        successful_exports = []
        for result in results:
            if 'csv_file' in result and result['csv_file']:
                successful_exports.append(result['csv_file'])

        total_time = time.time() - total_start

        print("\n" + "=" * 60)
        print("⚡ ULTRA-FAST ANALYSIS COMPLETE!")
        print("=" * 60)
        print(f"⏱️  Total processing time: {total_time:.1f} seconds")
        print(f"📁 Files exported: {len(successful_exports)}")

        if successful_exports:
            print(f"\n✅ CSV FILES CREATED:")
            for csv_file in successful_exports[:5]:  # Show first 5
                print(f"   • {csv_file}")
            if len(successful_exports) > 5:
                print(f"   ... and {len(successful_exports) - 5} more")

        print(f"\n📊 PERFORMANCE:")
        print(f"   • Directory scan: {scan_results['scan_time']:.1f}s")
        print(f"   • File processing: {total_time - scan_results['scan_time']:.1f}s")
        print(f"   • Average per file: {(total_time - scan_results['scan_time']) / len(activity_files):.1f}s")

        print(f"\n📧 NEXT STEPS:")
        print("   1. Open any CSV file to see your activity data")
        print("   2. Share CSV files for analysis")
        print("   3. All files processed in parallel for maximum speed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()