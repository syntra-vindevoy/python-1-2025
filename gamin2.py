import fitparse
import pandas as pd
from datetime import datetime, timezone
import numpy as np
from typing import Dict, List, Optional, Tuple
import os


class GarminFitParser:
    """
    A clean parser for Garmin FIT files that extracts meaningful data
    and provides activity-level aggregates.
    """

    def __init__(self, fit_file_path: str):
        self.fit_file_path = fit_file_path
        self.fitfile = fitparse.FitFile(fit_file_path)
        self.records = []
        self.session_info = {}
        self.activity_info = {}

    def parse_file(self) -> Dict:
        """
        Parse the FIT file and extract all relevant data.
        Returns a dictionary with records, session info, and activity info.
        """
        print(f"Parsing FIT file: {os.path.basename(self.fit_file_path)}")

        # Extract different message types
        self._extract_records()
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

    def _extract_records(self):
        """Extract record messages (the main data points during activity)"""
        print("Extracting record data...")

        for record in self.fitfile.get_messages('record'):
            record_data = {
                'timestamp': None,
                'latitude': None,
                'longitude': None,
                'altitude': None,
                'heart_rate': None,
                'cadence': None,
                'speed': None,
                'power': None,
                'distance': None,
                'temperature': None
            }

            for field in record:
                field_name = field.name
                field_value = field.value

                if field_name == 'timestamp':
                    # Convert to readable datetime
                    record_data['timestamp'] = field_value
                elif field_name == 'position_lat':
                    # Convert from semicircles to degrees
                    if field_value is not None:
                        record_data['latitude'] = field_value * (180.0 / (2 ** 31))
                elif field_name == 'position_long':
                    # Convert from semicircles to degrees
                    if field_value is not None:
                        record_data['longitude'] = field_value * (180.0 / (2 ** 31))
                elif field_name == 'altitude':
                    # Usually in meters
                    record_data['altitude'] = field_value
                elif field_name == 'heart_rate':
                    record_data['heart_rate'] = field_value
                elif field_name == 'cadence':
                    record_data['cadence'] = field_value
                elif field_name == 'speed':
                    # Convert from m/s to more readable units if needed
                    record_data['speed'] = field_value
                elif field_name == 'power':
                    record_data['power'] = field_value
                elif field_name == 'distance':
                    # Usually in meters
                    record_data['distance'] = field_value
                elif field_name == 'temperature':
                    record_data['temperature'] = field_value

            # Only add records with timestamp (valid data points)
            if record_data['timestamp']:
                self.records.append(record_data)

        print(f"Extracted {len(self.records)} data records")

    def _extract_session_info(self):
        """Extract session-level information"""
        print("Extracting session information...")

        for session in self.fitfile.get_messages('session'):
            for field in session:
                field_name = field.name
                field_value = field.value

                # Store all session fields
                self.session_info[field_name] = field_value

                # Convert specific fields for readability
                if field_name == 'start_time':
                    self.session_info['start_time_readable'] = field_value
                elif field_name == 'total_elapsed_time':
                    self.session_info['duration_minutes'] = field_value / 60 if field_value else None
                elif field_name == 'total_distance':
                    self.session_info['distance_km'] = field_value / 1000 if field_value else None
                elif field_name == 'sport':
                    self.session_info['sport_name'] = str(field_value)

    def _extract_activity_info(self):
        """Extract activity-level information"""
        print("Extracting activity information...")

        for activity in self.fitfile.get_messages('activity'):
            for field in activity:
                self.activity_info[field.name] = field.value

    def _calculate_aggregates(self) -> Dict:
        """Calculate useful aggregates from the records"""
        if not self.records:
            return {}

        df = pd.DataFrame(self.records)

        aggregates = {
            'total_records': len(self.records),
            'duration': None,
            'distance_stats': {},
            'speed_stats': {},
            'heart_rate_stats': {},
            'altitude_stats': {},
            'coordinate_bounds': {}
        }

        # Time-based calculations
        if 'timestamp' in df.columns and not df['timestamp'].isna().all():
            timestamps = df['timestamp'].dropna()
            if len(timestamps) > 1:
                duration_seconds = (timestamps.iloc[-1] - timestamps.iloc[0]).total_seconds()
                aggregates['duration'] = {
                    'seconds': duration_seconds,
                    'minutes': duration_seconds / 60,
                    'hours': duration_seconds / 3600
                }

        # Distance statistics
        if 'distance' in df.columns and not df['distance'].isna().all():
            distance_data = df['distance'].dropna()
            if len(distance_data) > 0:
                aggregates['distance_stats'] = {
                    'total_meters': distance_data.iloc[-1] if len(distance_data) > 0 else 0,
                    'total_km': distance_data.iloc[-1] / 1000 if len(distance_data) > 0 else 0,
                }

        # Speed statistics
        if 'speed' in df.columns and not df['speed'].isna().all():
            speed_data = df['speed'].dropna()
            aggregates['speed_stats'] = {
                'avg_mps': speed_data.mean(),
                'max_mps': speed_data.max(),
                'avg_kmh': speed_data.mean() * 3.6,
                'max_kmh': speed_data.max() * 3.6
            }

        # Heart rate statistics
        if 'heart_rate' in df.columns and not df['heart_rate'].isna().all():
            hr_data = df['heart_rate'].dropna()
            aggregates['heart_rate_stats'] = {
                'avg_bpm': hr_data.mean(),
                'max_bpm': hr_data.max(),
                'min_bpm': hr_data.min()
            }

        # Altitude statistics
        if 'altitude' in df.columns and not df['altitude'].isna().all():
            alt_data = df['altitude'].dropna()
            aggregates['altitude_stats'] = {
                'avg_meters': alt_data.mean(),
                'max_meters': alt_data.max(),
                'min_meters': alt_data.min(),
                'elevation_gain': self._calculate_elevation_gain(alt_data)
            }

        # Coordinate bounds (for mapping)
        lat_data = df['latitude'].dropna()
        lon_data = df['longitude'].dropna()
        if len(lat_data) > 0 and len(lon_data) > 0:
            aggregates['coordinate_bounds'] = {
                'north': lat_data.max(),
                'south': lat_data.min(),
                'east': lon_data.max(),
                'west': lon_data.min(),
                'center_lat': lat_data.mean(),
                'center_lon': lon_data.mean()
            }

        return aggregates

    def _calculate_elevation_gain(self, altitude_series) -> float:
        """Calculate total elevation gain"""
        if len(altitude_series) < 2:
            return 0

        gain = 0
        prev_alt = altitude_series.iloc[0]

        for alt in altitude_series.iloc[1:]:
            if alt > prev_alt:
                gain += (alt - prev_alt)
            prev_alt = alt

        return gain

    def export_to_csv(self, output_path: str = None):
        """Export records to CSV file"""
        if not self.records:
            print("No records to export")
            return

        if output_path is None:
            base_name = os.path.splitext(os.path.basename(self.fit_file_path))[0]
            output_path = f"{base_name}_parsed.csv"

        df = pd.DataFrame(self.records)
        df.to_csv(output_path, index=False)
        print(f"Exported {len(self.records)} records to {output_path}")

    def print_summary(self):
        """Print a human-readable summary of the activity"""
        print("\n" + "=" * 50)
        print("ACTIVITY SUMMARY")
        print("=" * 50)

        # Basic info
        print(f"File: {os.path.basename(self.fit_file_path)}")

        if self.session_info:
            sport = self.session_info.get('sport_name', 'Unknown')
            print(f"Sport: {sport}")

            if 'start_time_readable' in self.session_info:
                print(f"Start Time: {self.session_info['start_time_readable']}")

            if 'duration_minutes' in self.session_info:
                duration = self.session_info['duration_minutes']
                print(f"Duration: {duration:.1f} minutes ({duration / 60:.1f} hours)")

            if 'distance_km' in self.session_info:
                print(f"Distance: {self.session_info['distance_km']:.2f} km")

        # Print aggregates
        if hasattr(self, 'aggregates'):
            agg = self.aggregates if hasattr(self, 'aggregates') else {}

            if 'heart_rate_stats' in agg and agg['heart_rate_stats']:
                hr = agg['heart_rate_stats']
                print(f"Heart Rate: Avg {hr['avg_bpm']:.0f} bpm, Max {hr['max_bpm']:.0f} bpm")

            if 'speed_stats' in agg and agg['speed_stats']:
                speed = agg['speed_stats']
                print(f"Speed: Avg {speed['avg_kmh']:.1f} km/h, Max {speed['max_kmh']:.1f} km/h")

            if 'altitude_stats' in agg and agg['altitude_stats']:
                alt = agg['altitude_stats']
                print(
                    f"Altitude: {alt['min_meters']:.0f}m - {alt['max_meters']:.0f}m, Gain: {alt['elevation_gain']:.0f}m")

        print(f"Total Data Points: {len(self.records)}")


def parse_fit_file(fit_file_path: str) -> Dict:
    """
    Convenience function to parse a single FIT file.

    Args:
        fit_file_path: Path to the FIT file

    Returns:
        Dictionary with parsed data
    """
    parser = GarminFitParser(fit_file_path)
    result = parser.parse_file()
    parser.aggregates = result['aggregates']  # Store for summary
    parser.print_summary()
    return result


def parse_multiple_fit_files(directory_path: str) -> List[Dict]:
    """
    Parse all FIT files in a directory.

    Args:
        directory_path: Path to directory containing FIT files

    Returns:
        List of parsed data dictionaries
    """
    results = []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.fit'):
            fit_path = os.path.join(directory_path, filename)
            try:
                result = parse_fit_file(fit_path)
                results.append(result)
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    return results


# Example usage
if __name__ == "__main__":
    # Example: Parse a single FIT file
    fit_file_path = r"C:\Users\robin\PycharmProjects\rvo_garmin\DI_CONNECT\DI-Connect-Uploaded-Files\UploadedFiles_0-_Part1\robinvorsselmans1@hotmail.com_74724999004.fit"
    data = parse_fit_file(fit_file_path)

    # Access the data:
    records_df = data['records_df']  # Pandas DataFrame with all data points
    aggregates = data['aggregates']   # Summary statistics
    session_info = data['session_info']  # Session-level data

    # Example: Parse all FIT files in a directory
    # directory_path = "path/to/fit/files"
    # all_activities = parse_multiple_fit_files(directory_path)

    print("FIT file parser ready!")
    print("Usage examples:")
    print("1. data = parse_fit_file('activity.fit')")
    print("2. all_data = parse_multiple_fit_files('/path/to/fit/files/')")
