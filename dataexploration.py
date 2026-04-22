import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gamin2 import parse_fit_file, GarminFitParser
import numpy as np


def explore_fit_data(fit_file_path: str):
    """
    Comprehensive data exploration for a parsed FIT file
    """
    print("🔍 Loading and exploring FIT data...")

    # Parse the file
    data = parse_fit_file(fit_file_path)
    df = data['records_df']
    aggregates = data['aggregates']
    session_info = data['session_info']

    print("\n" + "=" * 60)
    print("📊 DATA EXPLORATION")
    print("=" * 60)

    # Check if DataFrame is empty
    if df.empty:
        print("⚠️  No data records found in the FIT file!")
        return data, df

    # 1. Basic DataFrame info
    print("\n1. DATAFRAME OVERVIEW:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Data types:\n{df.dtypes}")

    # 2. Check what data is available
    print("\n2. DATA AVAILABILITY:")
    for col in df.columns:
        non_null = df[col].count()
        total = len(df)
        percentage = (non_null / total) * 100 if total > 0 else 0
        print(f"   {col:15}: {non_null:4}/{total:4} ({percentage:5.1f}%) non-null")

    # 3. Show first few records
    print("\n3. FIRST 5 RECORDS:")
    print(df.head().to_string())

    # 4. Show time range - with safe column access
    if 'timestamp' in df.columns and not df['timestamp'].isna().all():
        start_time = df['timestamp'].min()
        end_time = df['timestamp'].max()
        duration = end_time - start_time
        print(f"\n4. TIME RANGE:")
        print(f"   Start: {start_time}")
        print(f"   End:   {end_time}")
        print(f"   Duration: {duration}")
        print(f"   Data points: {len(df)} (avg every {duration.total_seconds() / len(df):.1f} seconds)")
    else:
        print(f"\n4. TIME RANGE:")
        print("   ⚠️  No timestamp data available")

    # 5. Heart rate analysis - with safe column access
    if 'heart_rate' in df.columns and not df['heart_rate'].isna().all():
        hr_data = df['heart_rate'].dropna()
        print(f"\n5. HEART RATE ANALYSIS:")
        print(f"   Min:  {hr_data.min():.0f} bpm")
        print(f"   Max:  {hr_data.max():.0f} bpm")
        print(f"   Mean: {hr_data.mean():.0f} bpm")
        print(f"   Std:  {hr_data.std():.0f} bpm")
    else:
        print(f"\n5. HEART RATE ANALYSIS:")
        print("   ⚠️  No heart rate data available")

    # 6. Speed analysis - with safe column access
    if 'speed' in df.columns and not df['speed'].isna().all():
        speed_data = df['speed'].dropna() * 3.6  # Convert to km/h
        print(f"\n6. SPEED ANALYSIS (km/h):")
        print(f"   Min:  {speed_data.min():.1f} km/h")
        print(f"   Max:  {speed_data.max():.1f} km/h")
        print(f"   Mean: {speed_data.mean():.1f} km/h")
    else:
        print(f"\n6. SPEED ANALYSIS:")
        print("   ⚠️  No speed data available")

    # 7. GPS coverage - with safe column access
    if 'latitude' in df.columns and 'longitude' in df.columns:
        lat_data = df['latitude'].dropna()
        lon_data = df['longitude'].dropna()
        if len(lat_data) > 0 and len(lon_data) > 0:
            print(f"\n7. GPS COVERAGE:")
            print(f"   GPS points: {len(lat_data)}")
            print(f"   Latitude range:  {lat_data.min():.6f} to {lat_data.max():.6f}")
            print(f"   Longitude range: {lon_data.min():.6f} to {lon_data.max():.6f}")
            print(f"   Center point: ({lat_data.mean():.6f}, {lon_data.mean():.6f})")
        else:
            print(f"\n7. GPS COVERAGE:")
            print("   ⚠️  No GPS coordinate data available")
    else:
        print(f"\n7. GPS COVERAGE:")
        print("   ⚠️  No GPS columns (latitude/longitude) found")

    # 8. Show aggregates summary
    print(f"\n8. CALCULATED AGGREGATES:")
    for key, value in aggregates.items():
        if isinstance(value, dict) and value:
            print(f"   {key}:")
            for subkey, subvalue in value.items():
                print(f"      {subkey}: {subvalue}")
        elif value is not None:
            print(f"   {key}: {value}")

    return data, df


def create_basic_plots(df):
    """Create basic visualization plots"""
    print("\n📈 Creating basic plots...")

    # Set up the plot style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Garmin Activity Data Analysis', fontsize=16)

    # Plot 1: Heart Rate over time
    if not df['heart_rate'].isna().all():
        axes[0, 0].plot(df.index, df['heart_rate'], color='red', alpha=0.7)
        axes[0, 0].set_title('Heart Rate Over Time')
        axes[0, 0].set_ylabel('Heart Rate (bpm)')
        axes[0, 0].set_xlabel('Data Point #')
        axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Speed over time
    if not df['speed'].isna().all():
        speed_kmh = df['speed'] * 3.6  # Convert to km/h
        axes[0, 1].plot(df.index, speed_kmh, color='blue', alpha=0.7)
        axes[0, 1].set_title('Speed Over Time')
        axes[0, 1].set_ylabel('Speed (km/h)')
        axes[0, 1].set_xlabel('Data Point #')
        axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Altitude profile
    if not df['altitude'].isna().all():
        axes[1, 0].plot(df.index, df['altitude'], color='green', alpha=0.7)
        axes[1, 0].fill_between(df.index, df['altitude'], alpha=0.3, color='green')
        axes[1, 0].set_title('Altitude Profile')
        axes[1, 0].set_ylabel('Altitude (m)')
        axes[1, 0].set_xlabel('Data Point #')
        axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: GPS track (if available)
    lat_data = df['latitude'].dropna()
    lon_data = df['longitude'].dropna()
    if len(lat_data) > 0 and len(lon_data) > 0:
        # Get matching indices for lat/lon
        gps_df = df.dropna(subset=['latitude', 'longitude'])
        axes[1, 1].plot(gps_df['longitude'], gps_df['latitude'], 'o-', markersize=1, alpha=0.7)
        axes[1, 1].set_title('GPS Track')
        axes[1, 1].set_xlabel('Longitude')
        axes[1, 1].set_ylabel('Latitude')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].axis('equal')

    plt.tight_layout()
    plt.show()


def detailed_data_inspection(df):
    """Show detailed data for manual inspection"""
    print("\n🔍 DETAILED DATA INSPECTION")
    print("=" * 50)

    # Show summary statistics
    print("\nSUMMARY STATISTICS:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe().round(2))

    # Show data with specific intervals
    print(f"\nEVERY 10th DATA POINT (showing 10 samples):")
    sample_df = df.iloc[::max(1, len(df) // 10)].head(10)
    print(sample_df.to_string())

    # Heart rate zones (if available)
    if not df['heart_rate'].isna().all():
        hr_data = df['heart_rate'].dropna()
        print(f"\nHEART RATE ZONES:")
        zones = {
            'Rest (50-60%)': len(hr_data[(hr_data >= 50) & (hr_data < 60)]),
            'Easy (60-70%)': len(hr_data[(hr_data >= 60) & (hr_data < 70)]),
            'Aerobic (70-80%)': len(hr_data[(hr_data >= 70) & (hr_data < 80)]),
            'Threshold (80-90%)': len(hr_data[(hr_data >= 80) & (hr_data < 90)]),
            'Max (90%+)': len(hr_data[hr_data >= 90])
        }
        for zone, count in zones.items():
            percentage = (count / len(hr_data)) * 100
            print(f"   {zone:20}: {count:4} points ({percentage:5.1f}%)")


def export_comprehensive_excel(df, fit_file_path, aggregates, session_info):
    """Export comprehensive analysis to Excel for external analysis"""
    output_file = fit_file_path.replace('.fit', '_comprehensive_analysis.xlsx')

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 1. Raw data with all columns
        df.to_excel(writer, sheet_name='Raw_Data', index=False)

        # 2. Summary statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        summary_stats = df[numeric_cols].describe()
        summary_stats.to_excel(writer, sheet_name='Statistics')

        # 3. Session info
        if session_info:
            session_df = pd.DataFrame(list(session_info.items()), columns=['Field', 'Value'])
            session_df.to_excel(writer, sheet_name='Session_Info', index=False)

        # 4. Aggregates
        if aggregates:
            agg_rows = []
            for key, value in aggregates.items():
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        agg_rows.append([key, subkey, subvalue])
                else:
                    agg_rows.append([key, '', value])
            agg_df = pd.DataFrame(agg_rows, columns=['Category', 'Metric', 'Value'])
            agg_df.to_excel(writer, sheet_name='Aggregates', index=False)

        # 5. Heart rate analysis by minute
        if 'heart_rate' in df.columns and not df['heart_rate'].isna().all():
            hr_by_minute = df.groupby(df.index // 60)['heart_rate'].agg(['mean', 'min', 'max']).round(1)
            hr_by_minute.index.name = 'Minute'
            hr_by_minute.to_excel(writer, sheet_name='HR_by_Minute')

        # 6. Speed analysis by minute
        if 'speed' in df.columns and not df['speed'].isna().all():
            speed_kmh = df['speed'] * 3.6  # Convert to km/h
            speed_by_minute = speed_kmh.groupby(df.index // 60).agg(['mean', 'min', 'max']).round(1)
            speed_by_minute.index.name = 'Minute'
            speed_by_minute.to_excel(writer, sheet_name='Speed_by_Minute')

        # 7. GPS data (if available)
        if 'latitude' in df.columns and 'longitude' in df.columns:
            gps_data = df[['timestamp', 'latitude', 'longitude', 'altitude']].dropna(subset=['latitude', 'longitude'])
            if not gps_data.empty:
                gps_data.to_excel(writer, sheet_name='GPS_Track', index=False)

        # 8. Data quality report
        quality_report = []
        for col in df.columns:
            total_count = len(df)
            non_null_count = df[col].count()
            null_count = total_count - non_null_count
            null_percentage = (null_count / total_count) * 100
            quality_report.append([col, total_count, non_null_count, null_count, null_percentage])

        quality_df = pd.DataFrame(quality_report,
                                  columns=['Column', 'Total_Records', 'Non_Null', 'Null_Count', 'Null_Percentage'])
        quality_df.to_excel(writer, sheet_name='Data_Quality', index=False)

    print(f"\n💾 Comprehensive data exported to: {output_file}")
    return output_file


def debug_fit_file(fit_file_path: str):
    """
    Debug function to see what message types and fields are available in the FIT file
    """
    print(f"🔍 DEBUGGING FIT FILE: {os.path.basename(fit_file_path)}")
    print("=" * 60)

    fitfile = fitparse.FitFile(fit_file_path)

    # Count different message types
    message_counts = {}
    all_fields = {}

    for message in fitfile.get_messages():
        msg_type = message.name
        if msg_type not in message_counts:
            message_counts[msg_type] = 0
            all_fields[msg_type] = set()

        message_counts[msg_type] += 1

        # Collect all field names for this message type
        for field in message:
            all_fields[msg_type].add(field.name)

    print("\n📊 MESSAGE TYPES FOUND:")
    for msg_type, count in sorted(message_counts.items()):
        print(f"   {msg_type:20}: {count:4} messages")

    print(f"\n🔍 AVAILABLE FIELDS BY MESSAGE TYPE:")
    for msg_type in sorted(all_fields.keys()):
        if all_fields[msg_type]:  # Only show types with fields
            print(f"\n   {msg_type}:")
            for field_name in sorted(all_fields[msg_type]):
                print(f"      - {field_name}")

    # Let's look specifically at record messages and their actual content
    print(f"\n🎯 DETAILED RECORD MESSAGE INSPECTION:")
    record_count = 0
    for record in fitfile.get_messages('record'):
        record_count += 1
        if record_count <= 3:  # Show first 3 records
            print(f"\n   Record #{record_count}:")
            for field in record:
                print(f"      {field.name}: {field.value} (type: {type(field.value)})")

    print(f"\n   Total records found: {record_count}")

    return message_counts, all_fields

# Main exploration function
def main():
    # Use your FIT file path
    fit_file_path = r"C:\Users\robin\PycharmProjects\rvo_garmin\DI_CONNECT\DI-Connect-Uploaded-Files\UploadedFiles_0-_Part1\robinvorsselmans1@hotmail.com_74724999004.fit"

    # Explore the data
    data, df = explore_fit_data(fit_file_path)

    if not df.empty:
        # Export comprehensive Excel file
        excel_file = export_comprehensive_excel(df, fit_file_path, data['aggregates'], data['session_info'])

        # Create plots
        create_basic_plots(df)

        # Detailed inspection
        detailed_data_inspection(df)

        print("\n" + "=" * 60)
        print("✅ DATA ANALYSIS COMPLETE!")
        print("=" * 60)
        print("📧 Next steps:")
        print(f"1. Open the Excel file: {excel_file}")
        print("2. Share the Excel file for detailed analysis")
        print("3. Use Excel's built-in charts and pivot tables")
        print("4. Filter and analyze specific time periods")
    else:
        print("❌ No data to export - check your FIT file")


if __name__ == "__main__":
    main()
