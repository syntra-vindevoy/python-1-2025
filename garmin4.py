import fitparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Dict, List, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
import traceback
import glob


def deep_fit_file_analysis(fit_file_path: str) -> Dict:
    """
    DEEP analysis of FIT file - reads ALL messages
    """
    try:
        fitfile = fitparse.FitFile(fit_file_path)

        message_counts = {}
        all_fields = {}
        sample_data = {}

        messages_read = 0
        for message in fitfile.get_messages():
            msg_type = message.name
            messages_read += 1

            if msg_type not in message_counts:
                message_counts[msg_type] = 0
                all_fields[msg_type] = set()
                sample_data[msg_type] = []

            message_counts[msg_type] += 1

            message_data = {}
            for field in message:
                all_fields[msg_type].add(field.name)
                message_data[field.name] = field.value

            if len(sample_data[msg_type]) < 3:
                sample_data[msg_type].append(message_data)

        has_records = message_counts.get('record', 0) > 0
        has_sessions = message_counts.get('session', 0) > 0
        has_activities = message_counts.get('activity', 0) > 0
        has_monitoring = message_counts.get('monitoring', 0) > 0

        is_activity_file = has_records or (has_sessions and message_counts.get('session', 0) > 0)

        return {
            'file_path': fit_file_path,
            'filename': os.path.basename(fit_file_path),
            'messages_read': messages_read,
            'message_counts': message_counts,
            'all_fields': all_fields,
            'sample_data': sample_data,
            'has_records': has_records,
            'has_sessions': has_sessions,
            'has_activities': has_activities,
            'has_monitoring': has_monitoring,
            'is_activity_file': is_activity_file,
            'is_monitoring_file': has_monitoring,
            'record_count': message_counts.get('record', 0),
            'deep_analysis': True
        }

    except Exception as e:
        return {
            'file_path': fit_file_path,
            'filename': os.path.basename(fit_file_path),
            'error': str(e),
            'deep_analysis': False
        }


class DiagnosticActivityParser:
    """
    Parser with extensive diagnostics and testing
    """

    def __init__(self, fit_file_path: str):
        self.fit_file_path = fit_file_path
        self.fitfile = fitparse.FitFile(fit_file_path)
        self.diagnostics = {
            'records_found': 0,
            'records_with_data': 0,
            'fields_extracted': {},
            'extraction_errors': [],
            'parsing_stages': {}
        }

    def diagnostic_extract(self) -> Dict:
        """
        Extract with full diagnostics
        """
        print(f"   🔬 DIAGNOSTIC EXTRACTION...")

        records = []

        # Stage 1: Record extraction with diagnostics
        print(f"   📊 Stage 1: Extracting records...")

        try:
            record_messages = list(self.fitfile.get_messages('record'))
            self.diagnostics['records_found'] = len(record_messages)
            print(f"      Found {len(record_messages)} record messages")

            if len(record_messages) == 0:
                print(f"      ❌ NO RECORD MESSAGES FOUND!")
                self.diagnostics['parsing_stages']['records'] = 'NO_RECORDS'
            else:
                print(f"      ✅ Found record messages, processing...")

                for i, record in enumerate(record_messages):
                    if i < 5:
                        print(f"         Record {i + 1} fields:")

                    record_data = {}
                    field_count = 0

                    for field in record:
                        field_name = field.name
                        field_value = field.value
                        field_count += 1

                        if i < 3 and field_count < 10:
                            print(f"            {field_name}: {field_value}")

                        if field_name not in self.diagnostics['fields_extracted']:
                            self.diagnostics['fields_extracted'][field_name] = 0
                        self.diagnostics['fields_extracted'][field_name] += 1

                        try:
                            if field_name == 'timestamp':
                                record_data['timestamp'] = field_value
                            elif field_name == 'heart_rate' and field_value is not None:
                                record_data['heart_rate'] = field_value
                            elif field_name == 'speed' and field_value is not None:
                                record_data['speed'] = field_value
                            elif field_name == 'enhanced_speed' and field_value is not None:
                                if 'speed' not in record_data:
                                    record_data['speed'] = field_value
                            elif field_name == 'position_lat' and field_value is not None:
                                record_data['latitude'] = field_value * (180.0 / (2 ** 31))
                            elif field_name == 'position_long' and field_value is not None:
                                record_data['longitude'] = field_value * (180.0 / (2 ** 31))
                            elif field_name == 'altitude' and field_value is not None:
                                record_data['altitude'] = field_value
                            elif field_name =='enhanced_altitude' and field_value is not None:
                                if 'altitude' not in record_data:
                                    record_data['altitude'] = field_value
                            elif field_name == 'distance' and field_value is not None:
                                record_data['distance'] = field_value
                            elif field_name == 'power' and field_value is not None:
                                record_data['power'] = field_value
                            elif field_name == 'cadence' and field_value is not None:
                                record_data['cadence'] = field_value
                            elif field_name == 'fractional_cadence' and field_value is not None:
                                record_data['fractional_cadence'] == field_value
                            elif field_name == 'temperature' and field_value is not None:
                                record_data['temperature'] = field_value
                        except Exception as e:
                            self.diagnostics['extraction_errors'].append(f"Field {field_name}: {str(e)}")

                    if record_data:
                        records.append(record_data)
                        self.diagnostics['records_with_data'] += 1

                    if len(records) >= 10000:
                        print(f"      📊 Limited to first 10,000 records for testing")
                        break

                self.diagnostics['parsing_stages']['records'] = 'SUCCESS'

        except Exception as e:
            error_msg = f"Record extraction failed: {str(e)}"
            print(f"      ❌ {error_msg}")
            self.diagnostics['extraction_errors'].append(error_msg)
            self.diagnostics['parsing_stages']['records'] = 'FAILED'

        # Stage 2: Session info extraction
        print(f"   📅 Stage 2: Extracting session info...")
        session_info = {}
        try:
            session_messages = list(self.fitfile.get_messages('session'))
            print(f"      Found {len(session_messages)} session messages")

            for session in session_messages:
                for field in session:
                    session_info[field.name] = field.value

            self.diagnostics['parsing_stages']['sessions'] = 'SUCCESS'
            print(f"      ✅ Session extraction complete")

        except Exception as e:
            error_msg = f"Session extraction failed: {str(e)}"
            print(f"      ❌ {error_msg}")
            self.diagnostics['extraction_errors'].append(error_msg)
            self.diagnostics['parsing_stages']['sessions'] = 'FAILED'

        # Stage 3: Create DataFrame
        print(f"   📊 Stage 3: Creating DataFrame...")
        df = pd.DataFrame()
        try:
            if records:
                df = pd.DataFrame(records)
                print(f"      ✅ DataFrame created: {df.shape}")
                print(f"      📋 Columns: {list(df.columns)}")
            else:
                print(f"      ❌ No records to create DataFrame")

            self.diagnostics['parsing_stages']['dataframe'] = 'SUCCESS' if not df.empty else 'EMPTY'

        except Exception as e:
            error_msg = f"DataFrame creation failed: {str(e)}"
            print(f"      ❌ {error_msg}")
            self.diagnostics['extraction_errors'].append(error_msg)
            self.diagnostics['parsing_stages']['dataframe'] = 'FAILED'

        return {
            'file_path': self.fit_file_path,
            'records': records,
            'session_info': session_info,
            'records_df': df,
            'record_count': len(records),
            'diagnostics': self.diagnostics
        }


def test_csv_export_capability():
    """
    Test CSV export functionality
    """
    print(f"🧪 TESTING CSV EXPORT CAPABILITY...")

    try:
        test_data = {
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c'],
            'col3': [1.1, 2.2, 3.3]
        }

        df = pd.DataFrame(test_data)
        test_file = "diagnostic_test.csv"

        df.to_csv(test_file, index=False)

        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            full_path = os.path.abspath(test_file)
            print(f"   ✅ CSV creation successful")
            print(f"   📁 File: {test_file}")
            print(f"   📊 Size: {file_size} bytes")
            print(f"   🗂️ Full path: {full_path}")

            os.remove(test_file)
            return True, full_path
        else:
            print(f"   ❌ CSV file not created")
            return False, None

    except Exception as e:
        print(f"   ❌ CSV test failed: {str(e)}")
        traceback.print_exc()
        return False, None


def diagnostic_export_csv(data: Dict, fit_file_path: str) -> Optional[str]:
    """
    CSV export with extensive diagnostics
    """
    print(f"   💾 DIAGNOSTIC CSV EXPORT...")

    try:
        df = data.get('records_df', pd.DataFrame())

        if df.empty:
            print(f"      ❌ DataFrame is empty - cannot export")
            return None

        print(f"      📊 DataFrame info:")
        print(f"         Shape: {df.shape}")
        print(f"         Columns: {list(df.columns)}")
        print(f"         Memory usage: {df.memory_usage().sum()} bytes")

        base_name = os.path.splitext(os.path.basename(fit_file_path))[0]
        csv_file = f"{base_name}_DIAGNOSTIC_export.csv"
        full_path = os.path.abspath(csv_file)

        print(f"      📁 Exporting to: {csv_file}")
        print(f"      🗂️ Full path: {full_path}")

        df.to_csv(csv_file, index=False)

        if os.path.exists(csv_file):
            file_size = os.path.getsize(csv_file)
            print(f"      ✅ Export successful!")
            print(f"      📊 File size: {file_size} bytes")

            test_df = pd.read_csv(csv_file, nrows=5)
            print(f"      ✅ File readable - first 5 rows loaded")

            return full_path
        else:
            print(f"      ❌ File not created after export attempt")
            return None

    except Exception as e:
        print(f"      ❌ Export failed: {str(e)}")
        traceback.print_exc()
        return None


def scan_and_test_directory(directory_path: str) -> Dict:
    """
    Comprehensive directory scan - scans ALL files with progress updates
    """
    print(f"🔍 COMPREHENSIVE DIRECTORY SCAN...")
    print(f"📂 Directory: {directory_path}")

    csv_works, csv_path = test_csv_export_capability()

    if not csv_works:
        print(f"❌ CSV export is broken - fixing this first!")
        return {'csv_broken': True}

    # Find all FIT files
    fit_files = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.fit'):
            fit_path = os.path.join(directory_path, filename)
            fit_files.append(fit_path)

    total_files = len(fit_files)
    print(f"📊 Found {total_files} FIT files - scanning ALL of them...")

    activity_files = []
    monitoring_files = []
    failed_files = []

    for i, fit_path in enumerate(fit_files):  # Scan ALL files - no limit
        # Progress update every 100 files
        if (i + 1) % 100 == 0 or (i + 1) == total_files:
            print(f"   Progress: {i + 1}/{total_files} files scanned | "
                  f"✅ Activity: {len(activity_files)} | "
                  f"⏰ Monitoring: {len(monitoring_files)} | "
                  f"❓ Other: {len(failed_files)}")

        analysis = deep_fit_file_analysis(fit_path)

        if 'error' in analysis:
            failed_files.append(analysis)
        elif analysis.get('is_activity_file', False):
            activity_files.append(analysis)
            print(f"   🎉 ACTIVITY FILE FOUND at position {i + 1}: {os.path.basename(fit_path)} "
                  f"({analysis.get('record_count', 0)} records)")
        elif analysis.get('is_monitoring_file', False):
            monitoring_files.append(analysis)
        else:
            failed_files.append(analysis)

    return {
        'csv_works': csv_works,
        'activity_files': activity_files,
        'monitoring_files': monitoring_files,
        'failed_files': failed_files,
        'total_fit_files': total_files
    }


def run_single_fit_test(fit_file_path: str):
    """Test with a specific FIT file"""

    print("🧪 TESTING SINGLE FIT FILE")
    print(f"📁 File: {os.path.basename(fit_file_path)}")
    print(f"📂 Full path: {fit_file_path}")
    print(f"📊 File exists: {os.path.exists(fit_file_path)}")

    if not os.path.exists(fit_file_path):
        print("❌ File doesn't exist! Check the path.")
        return

    analysis = deep_fit_file_analysis(fit_file_path)
    print(f"\n📊 Analysis results:")
    print(f"   Is activity file: {analysis.get('is_activity_file', 'Unknown')}")
    print(f"   Record count: {analysis.get('record_count', 0)}")
    print(f"   Message types: {list(analysis.get('message_counts', {}).keys())}")

    if analysis.get('is_activity_file', False):
        print(f"\n🔬 Processing as activity file...")
        parser = DiagnosticActivityParser(fit_file_path)
        data = parser.diagnostic_extract()

        csv_file = diagnostic_export_csv(data, fit_file_path)
        if csv_file:
            print(f"\n✅ SUCCESS! CSV created at: {csv_file}")
        else:
            print(f"\n❌ CSV export failed")
    else:
        print(f"\n⚠️ Not detected as activity file")


def main():
    """
    Main diagnostic function
    """
    directory_path = r"C:\Users\robin\PycharmProjects\rvo_garmin\DI_CONNECT\DI-Connect-Uploaded-Files\UploadedFiles_0-_Part1"

    print("🔬 COMPREHENSIVE DIAGNOSTIC ANALYZER")
    print("=" * 60)
    print("🎯 Goal: Find and export all activity FIT files to CSV")
    print("=" * 60)

    current_dir = os.getcwd()
    print(f"📂 Current working directory: {current_dir}")

    existing_csvs = glob.glob("*.csv") + glob.glob("**/*.csv", recursive=True)
    print(f"📄 Existing CSV files in project: {len(existing_csvs)}")
    for csv_file in existing_csvs[:5]:
        print(f"   📄 {csv_file}")

    try:
        # Full directory scan - ALL files
        print(f"\n🔍 FULL DIRECTORY SCAN (scanning ALL files)...")
        scan_results = scan_and_test_directory(directory_path)

        if scan_results.get('csv_broken', False):
            print(f"\n❌ CRITICAL: CSV functionality is broken!")
            return

        activity_files = scan_results['activity_files']

        print(f"\n" + "=" * 60)
        print(f"📊 SCAN COMPLETE:")
        print(f"   ✅ Activity files found: {len(activity_files)}")
        print(f"   ⏰ Monitoring files: {len(scan_results['monitoring_files'])}")
        print(f"   ❓ Other/Unknown: {len(scan_results['failed_files'])}")
        print(f"   📁 Total scanned: {scan_results['total_fit_files']}")
        print("=" * 60)

        if not activity_files:
            print(f"\n❌ NO ACTIVITY FILES FOUND IN ENTIRE DIRECTORY!")
            print(f"💡 Try looking in a different folder for workout files")
            return

        print(f"\n🎉 FOUND {len(activity_files)} ACTIVITY FILES! Processing first one...")

        # Process and export first activity file as test
        test_file = activity_files[0]
        print(f"\n🧪 PROCESSING: {test_file['filename']}")
        print(f"   Records: {test_file.get('record_count', 0)}")

        parser = DiagnosticActivityParser(test_file['file_path'])
        data = parser.diagnostic_extract()

        print(f"\n📊 EXTRACTION RESULTS:")
        print(f"   Records found: {data['diagnostics']['records_found']}")
        print(f"   Records with data: {data['diagnostics']['records_with_data']}")
        print(f"   DataFrame shape: {data['records_df'].shape}")
        print(f"   Parsing stages: {data['diagnostics']['parsing_stages']}")

        if data['diagnostics']['extraction_errors']:
            print(f"   ⚠️ Extraction errors: {len(data['diagnostics']['extraction_errors'])}")
            for error in data['diagnostics']['extraction_errors'][:3]:
                print(f"      - {error}")

        csv_file = diagnostic_export_csv(data, test_file['file_path'])

        if csv_file:
            print(f"\n✅ SUCCESS! CSV file created!")
            diagnostic_files = glob.glob("*DIAGNOSTIC*.csv")
            print(f"\n📄 CSV files created:")
            for file in diagnostic_files:
                full_path = os.path.abspath(file)
                size = os.path.getsize(file)
                print(f"   📄 {file} ({size} bytes)")
                print(f"      Full path: {full_path}")
        else:
            print(f"\n❌ CSV export failed!")

        print(f"\n" + "=" * 60)
        print("🔬 DIAGNOSTIC COMPLETE!")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Major error: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    main()