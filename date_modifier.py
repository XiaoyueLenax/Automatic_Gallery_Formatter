import os
import ctypes
from datetime import datetime

def set_file_dates_windows(file_path, creation_time, modification_time):
    # Convert datetime objects to Windows filetime
    creation_filetime = int((creation_time - datetime(1601, 1, 1)).total_seconds() * 1e7)
    modification_filetime = int((modification_time - datetime(1601, 1, 1)).total_seconds() * 1e7)

    # Set file creation and modification times
    ctypes.windll.kernel32.SetFileTime(
        ctypes.windll.kernel32.CreateFileW(file_path, 0x10000000, 0, 0, 3, 0x80, 0),
        ctypes.byref(ctypes.c_int64(creation_filetime)),
        None,
        ctypes.byref(ctypes.c_int64(modification_filetime))
    )

# Example usage
file_path = "C:\Users\coruf\OneDrive\Documents\Random_Projects\test_gallery\chibi_isdris___glint_uwu_by_corufang_dcfhq3c-fullview.png"
new_creation_time = datetime(2021, 1, 1, 12, 0, 0)
new_modification_time = datetime(2021, 1, 2, 12, 0, 0)

set_file_dates_windows(file_path, new_creation_time, new_modification_time)
