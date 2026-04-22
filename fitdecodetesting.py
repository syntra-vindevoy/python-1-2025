import fitdecode
import pandas as pd
import os
from typing import Dict


# FIT file type codes (from the FIT protocol spec)
FIT_FILE_TYPES = {
    4: 'activity',
    8: 'workout',
    11: 'course',
    15: 'schedules',
    20: 'weight',
    28: 'totals',
    32: 'goals',
    34: 'blood_pressure',
    35: 'monitoring_daily',
    40: 'monitoring',
    41: 'sport_settings',
    49: 'segment',
}


class UnsupportedFitFileError(Exception):
    """Raised when the FIT file is not an activity file."""
    pass


def get_fit_file_type(fit_file_path: str) -> str:
    """
    Reads the file_id message to determine the FIT file type.
    Returns the type as a string (e.g. 'activity', 'monitoring', 'sport_settings').
    """
    with fitdecode.FitReader(fit_file_path) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage) and frame.name == 'file_id':
                raw_type = frame.get_value('type', fallback=None)
                if raw_type is not None:
                    # fitdecode may return the raw int or already-decoded string
                    if isinstance(raw_type, int):
                        return FIT_FILE_TYPES.get(raw_type, f'unknown_{raw_type}')
                    return str(raw_type)
    return 'unknown'


def assert_activity_file(fit_file_path: str) -> None:
    """
    Checks if the FIT file is an activity file.
    Raises UnsupportedFitFileError if it is not.
    """
    file_type = get_fit_file_type(fit_file_path)
    if file_type != 'activity':
        raise UnsupportedFitFileError(
            f"This is a '{file_type}' file and is not supported. Only 'activity' files are accepted."
        )


def extract_activity_data(fit_file_path: str) -> Dict:
    """
    Extracts all meaningful data from an activity FIT file:
      - device_info  : device/hardware info (manufacturer, product, serial, software version)
      - user_profile : user data (age, weight, height, gender)
      - sport        : type of activity (sport, sub_sport, name)
      - records_df   : time-series monitoring data (heart rate, speed, GPS, altitude, etc.)
      - session      : session summary (start time, duration, distance, avg/max metrics)

    Raises UnsupportedFitFileError if the file is not an activity.
    """
    assert_activity_file(fit_file_path)

    device_info = {}
    user_profile = {}
    sport_info = {}
    session_info = {}
    records = []

    with fitdecode.FitReader(fit_file_path) as fit:
        for frame in fit:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue

            # --- Device info ---
            if frame.name == 'device_info' and not device_info:
                for field in frame.fields:
                    if not field.name.startswith('unknown_'):
                        device_info[field.name] = field.value

            # --- User profile ---
            elif frame.name == 'user_profile' and not user_profile:
                for field in frame.fields:
                    if not field.name.startswith('unknown_'):
                        user_profile[field.name] = field.value

            # --- Sport / activity type ---
            elif frame.name == 'sport' and not sport_info:
                for field in frame.fields:
                    if not field.name.startswith('unknown_'):
                        sport_info[field.name] = field.value

            # --- Session summary ---
            elif frame.name == 'session' and not session_info:
                for field in frame.fields:
                    if not field.name.startswith('unknown_'):
                        session_info[field.name] = field.value

            # --- Per-second monitoring records ---
            elif frame.name == 'record':
                record = {}
                for field in frame.fields:
                    if field.name == 'position_lat' and field.value is not None:
                        record['latitude'] = field.value * (180.0 / (2 ** 31))
                    elif field.name == 'position_long' and field.value is not None:
                        record['longitude'] = field.value * (180.0 / (2 ** 31))
                    elif field.name.startswith('unknown_'):
                        pass  # skip undocumented Garmin-internal fields
                    else:
                        record[field.name] = field.value
                if record:
                    records.append(record)

    return {
        'filename': os.path.basename(fit_file_path),
        'device_info': device_info,
        'user_profile': user_profile,
        'sport_info': sport_info,
        'session_info': session_info,
        'records_df': pd.DataFrame(records) if records else pd.DataFrame(),
    }


# --- Example usage ---
if __name__ == '__main__':
    path = r"C:\Users\robin\PycharmProjects\rvo_garmin\DI_CONNECT\DI-Connect-Uploaded-Files\UploadedFiles_0-_Part1\robinvorsselmans1@hotmail.com_101616206648.fit"

    try:
        data = extract_activity_data(path)
        print(f"Sport    : {data['sport_info']}")
        print(f"Device   : {data['device_info']}")
        print(f"User     : {data['user_profile']}")
        print(f"Session  : {data['session_info']}")
        print(f"Records  : {data['records_df'].shape}")
        print("\n--- Records columns ---")
        print(list(data['records_df'].columns))
        print("\n--- Data types ---")
        print(data['records_df'].dtypes)
        print(data['records_df'].head())

    except UnsupportedFitFileError as e:
        print(f"❌ {e}")