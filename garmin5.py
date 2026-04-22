import fitparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime


def check_fit_file_type(fit_file_path: str) -> Dict[str, any]:
    """
    Quickly check what type of FIT file this is
    Returns file type information
    """
    try:
        fitfile = fitparse.FitFile(fit_file_path)

        # Count message types
        message_counts = {}
        has_records = False
        has_sessions = False
        has_activities = False

        for message in fitfile.get_messages():
            msg_type = message.name
            message_counts[msg_type] = message_counts.get(msg_type, 0) + 1

            if msg_type == 'record':
                has_records = True
            elif msg_type == 'session':
                has_sessions = True
            elif msg_type == 'activity':
                has_activities = True

        # Determine file type
        is_activity_file = has_records and (has_sessions or has_activities)
        is_monitoring_file = 'monitoring' in message_counts

        file_info = {
            'file_path': fit_file_path,
            'filename': os.path.basename(fit_file_path),
            'is_activity_file': is_activity_file,
            'is_monitoring_file': is_monitoring_file,
            'message_counts': message_counts,
            'total_records': message_counts.get('record', 0),
            'total_sessions': message_counts.get('session', 0),
            'total_activities': message_counts.get('activity', 0)
        }

        return file_info

    except Exception as e:
        return {
            'file_path': fit_file_path,
            'filename': os.path.basename(fit_file_path),
            'is_activity_file': False,
            'is_monitoring_file': False,
            'error': str(e)
        }


def scan_directory_for_activities(directory_path: str) -> List[Dict]:
    """
    Scan directory for FIT files and categorize them
    """
    print(f"🔍 SCANNING DIRECTORY: {directory_path}")
    print("=" * 60)

    all_fit_files = []
    activity_files = []
    monitoring_files = []
    unknown_files = []

    # Find all .fit files
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.fit'):
            fit_path = os.path.join(directory_path, filename)
            all_fit_files.append(fit_path)

    print(f"Found {len(all_fit_files)} FIT files. Analyzing...")

    # Analyze each file
    for i, fit_path in enumerate(all_fit_files):
        print(f"   Checking {i + 1}/{len(all_fit_files)}: {os.path.basename(fit_path)}")

        file_info = check_fit_file_type(fit_path)

        if 'error' in file_info:
            print(f"      ❌ Error: {file_info['error']}")
            unknown_files.append(file_info)
        elif file_info['is_activity_file']:
            print(f"      ✅ ACTIVITY FILE - {file_info['total_records']} records")
            activity_files.append(file_info)
        elif file_info['is_monitoring_file']:
            print(f"      ⏰ Monitoring file - skipping")
            monitoring_files.append(file_info)
        else:
            print(f"      ❓ Unknown type - {list(file_info['message_counts'].keys())}")
            unknown_files.append(file_info)

    print(f"\n📊 SCAN RESULTS:")
    print(f"   ✅ Activity files: {len(activity_files)}")
    print(f"   ⏰ Monitoring files: {len(monitoring_files)}")
    print(f"   ❓ Unknown/Error files: {len(unknown_files)}")

    return {
        'activity_files': activity_files,
        'monitoring_files': monitoring_files,
        'unknown_files': unknown_files
    }


class ActivityFitParser:
    """
    Parser specifically for activity FIT files with comprehensive data extraction
    """

    def __init__(self, fit_file_path: str):
        self.fit_file_path = fit_file_path
        self.fitfile = fitparse.FitFile(fit_file_path)
        self.records = []
        self.session_info = {}
        self.activity_info = {}

    def _extract_records_flexible(self):
        """Extract ALL record data flexibly"""
        print("   Extracting record data...")

        for record in self.fitfile.get_messages('record'):
            record_data = {}

            # Extract ALL fields present in the record
            for field in record:
                field_name = field.name
                field_value = field.value

                # Handle special conversions
                if field_name == 'position_lat' and field_value is not None:
                    record_data['latitude'] = field_value * (180.0 / (2 ** 31))
                elif field_name == 'position_long' and field_value is not None:
                    record_data['longitude'] = field_value * (180.0 / (2 ** 31))
                else:
                    # Store all other fields as-is
                    record_data[field_name] = field_value

            # Add record if it has any data at all
            if record_data:
                self.records.append(record_data)

        print(f"   Extracted {len(self.records)} data records")

    def _extract_session_info(self):
        """Extract session information"""
        print("   Extracting session information...")

        for session in self.fitfile.get_messages('session'):
            for field in session:
                field_name = field.name
                field_value = field.value
                self.session_info[field_name] = field_value

                # Add human-readable versions
                if field_name == 'start_time':
                    self.session_info['start_time_readable'] = str(field_value)
                elif field_name == 'total_elapsed_time' and field_value:
                    self.session_info['duration_minutes'] = field_value / 60
                    self.session_info['duration_hours'] = field_value / 3600
                elif field_name == 'total_distance' and field_value:
                    self.session_info['distance_km'] = field_value / 1000
                elif field_name == 'sport':
                    self.session_info['sport_name'] = str(field_value)

    def _extract_activity_info(self):
        """Extract activity information"""
        print("   Extracting activity information...")

        for activity in self.fitfile.get_messages('activity'):
            for field in activity:
                self.activity_info[field.name] = field.value

    def parse_file(self) -> Dict:
        """Parse the FIT file completely"""
        print(f"📊 PARSING ACTIVITY FILE: {os.path.basename(self.fit_file_path)}")


        # Extract all data
        self._extract_records_flexible()
        self._extract_session_info()
        self._extract_activity_info()

        # Calculate aggregates
        aggregates = self._calculate_aggregates()

        return {
            'file_path': self.fit_file_path,
            'records': self.records,
            'session_info': self.session_info,
            'activity_info': self.activity_info,
            'aggregates': aggregates,
            'records_df': pd.DataFrame(self.records) if self.records else pd.DataFrame()
        }

    def _calculate_aggregates(self) -> Dict:
        """Calculate aggregates from available data"""
        if not self.records:
            return {'total_records': 0}

        df = pd.DataFrame(self.records)
        aggregates = {'total_records': len(self.records)}

        # Time calculations
        if 'timestamp' in df.columns:
            timestamps = df['timestamp'].dropna()
            if len(timestamps) > 1:
                duration_seconds = (timestamps.iloc[-1] - timestamps.iloc[0]).total_seconds()
                aggregates['duration'] = {
                    'seconds': duration_seconds,
                    'minutes': duration_seconds / 60,
                    'hours': duration_seconds / 3600
                }

        # Calculate stats for important fields
        key_fields = ['heart_rate', 'speed', 'altitude', 'distance', 'power', 'cadence']

        for field in key_fields:
            if field in df.columns and not df[field].isna().all():
                data = df[field].dropna()
                if len(data) > 0:
                    aggregates[f'{field}_stats'] = {
                        'count': len(data),
                        'mean': data.mean(),
                        'min': data.min(),
                        'max': data.max(),
                        'std': data.std() if len(data) > 1 else 0
                    }

        # GPS bounds if available
        if 'latitude' in df.columns and 'longitude' in df.columns:
            lat_data = df['latitude'].dropna()
            lon_data = df['longitude'].dropna()
            if len(lat_data) > 0 and len(lon_data) > 0:
                aggregates['gps_bounds'] = {
                    'north': lat_data.max(),
                    'south': lat_data.min(),
                    'east': lon_data.max(),
                    'west': lon_data.min(),
                    'center_lat': lat_data.mean(),
                    'center_lon': lon_data.mean(),
                    'gps_points': len(lat_data)
                }

        return aggregates

    def print_summary(self):
        """Print comprehensive summary"""
        print("\n" + "=" * 50)
        print("ACTIVITY SUMMARY")
        print("=" * 50)

        print(f"File: {os.path.basename(self.fit_file_path)}")
        print(f"Total Records: {len(self.records)}")

        if self.records:
            df = pd.DataFrame(self.records)
            print(f"Available Columns: {list(df.columns)}")
            print(f"Data Shape: {df.shape}")

            # Show data availability for key fields
            key_fields = ['timestamp', 'heart_rate', 'speed', 'distance', 'latitude', 'longitude', 'altitude']
            print(f"\nKey Data Availability:")
            for field in key_fields:
                if field in df.columns:
                    non_null = df[field].count()
                    total = len(df)
                    percentage = (non_null / total) * 100 if total > 0 else 0
                    print(f"   {field:12}: {non_null:4}/{total:4} ({percentage:5.1f}%)")

        # Session summary
        if self.session_info:
            print(f"\nSession Information:")
            interesting_fields = ['sport_name', 'start_time_readable', 'duration_minutes', 'distance_km']
            for field in interesting_fields:
                if field in self.session_info:
                    print(f"   {field}: {self.session_info[field]}")


def export_to_csv(data, fit_file_path):
    """Export data to CSV"""
    base_name = os.path.splitext(os.path.basename(fit_file_path))[0]

    # Export main data
    df = data['records_df']
    if not df.empty:
        csv_file = f"{base_name}_activity_data.csv"
        df.to_csv(csv_file, index=False)
        print(f"   ✅ Exported {len(df)} records to: {csv_file}")
        return csv_file
    else:
        print(f"   ❌ No data to export")
        return None


def create_plots(df, filename):
    """Create plots for activity data"""
    if df.empty:
        print("   ⚠️  No data for plotting")
        return

    print(f"   📈 Creating plots...")

    # Find plottable fields
    key_fields = ['heart_rate', 'speed', 'altitude', 'distance']
    plottable_fields = [field for field in key_fields if field in df.columns and not df[field].isna().all()]

    if not plottable_fields:
        print("   ⚠️  No key fields available for plotting")
        return

    # Create subplots
    n_plots = len(plottable_fields)
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten() if n_plots > 1 else [axes]

    fig.suptitle(f'Activity Analysis: {filename}', fontsize=14)

    for i, field in enumerate(plottable_fields[:4]):
        if i < len(axes):
            data = df[field].dropna()
            if len(data) > 0:
                axes[i].plot(data.index, data.values, alpha=0.7)
                axes[i].set_title(f'{field.replace("_", " ").title()}')
                axes[i].set_ylabel(field)
                axes[i].set_xlabel('Data Point')
                axes[i].grid(True, alpha=0.3)

    # Hide unused subplots
    for i in range(n_plots, 4):
        if i < len(axes):
            axes[i].set_visible(False)

    plt.tight_layout()

    plot_file = f"{os.path.splitext(filename)[0]}_analysis.png"
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"   ✅ Plots saved to: {plot_file}")


def main():
    """Main function to find and analyze activity files"""

    # Directory containing FIT files
    directory_path = r"C:\Users\robin\PycharmProjects\rvo_garmin\DI_CONNECT\DI-Connect-Uploaded-Files\UploadedFiles_0-_Part1"

    print("🚀 SMART FIT FILE ANALYZER")
    print("=" * 60)
    print("🎯 Goal: Find activity files, skip monitoring files")
    print("=" * 60)

    try:
        # Scan directory for activity files
        scan_results = scan_directory_for_activities(directory_path)

        activity_files = scan_results['activity_files']
        monitoring_files = scan_results['monitoring_files']

        if not activity_files:
            print("\n❌ NO ACTIVITY FILES FOUND!")
            print("\n📋 What was found instead:")
            if monitoring_files:
                print(f"   • {len(monitoring_files)} monitoring/wellness files")
                print("   • These contain daily activity tracking, not workout data")
            print("\n💡 Try looking for files that contain actual workout/exercise data")
            print("   • Look for files created during specific workouts")
            print("   • Activity files usually have GPS tracks, heart rate data")
            return

        print(f"\n🎉 FOUND {len(activity_files)} ACTIVITY FILES!")

        # Process each activity file
        successful_exports = []

        for i, file_info in enumerate(activity_files):
            print(f"\n📊 PROCESSING ACTIVITY {i + 1}/{len(activity_files)}:")
            print(f"   File: {file_info['filename']}")
            print(f"   Records: {file_info['total_records']}")

            try:
                # Parse the activity file
                parser = ActivityFitParser(file_info['file_path'])
                data = parser.parse_file()
                parser.print_summary()

                # Export to CSV
                csv_file = export_to_csv(data, file_info['file_path'])
                if csv_file:
                    successful_exports.append(csv_file)

                # Create plots
                create_plots(data['records_df'], file_info['filename'])

            except Exception as e:
                print(f"   ❌ Error processing {file_info['filename']}: {e}")

        print("\n" + "=" * 60)
        print("🎉 ANALYSIS COMPLETE!")
        print("=" * 60)

        if successful_exports:
            print(f"✅ Successfully exported {len(successful_exports)} activity files:")
            for csv_file in successful_exports:
                print(f"   • {csv_file}")

            print("\n📧 NEXT STEPS:")
            print("1. Open the CSV files to explore your workout data")
            print("2. Share the CSV files for detailed analysis")
            print("3. Look at the generated plots")
        else:
            print("❌ No files could be successfully processed")

        print(f"\n📊 SUMMARY:")
        print(f"   • Total FIT files found: {len(activity_files) + len(monitoring_files)}")
        print(f"   • Activity files: {len(activity_files)}")
        print(f"   • Monitoring files (skipped): {len(monitoring_files)}")
        print(f"   • Successfully processed: {len(successful_exports)}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()