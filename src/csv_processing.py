from typing import Optional

import pandas as pd

from src.CallDetail import CallDetail
from src.utils import parse_jakarta_datetime, convert_to_jakarta_time_iso, parse_phone_number


def process_dashboard_csv(
    file_path: str, call_details: Optional[dict[str, CallDetail]] = None
) -> dict[str, CallDetail]:
    if call_details is None:
        call_details = {}

    print(f"- Reading dashboard file {file_path}...")
    df1 = pd.read_csv(file_path, low_memory=False).astype(str)
    for index, row in df1.iterrows():
        if row["Call type"] in ["OUTGOING_CALL", "OUTGOING_CALL_ABSENCE"]:
            continue
        call_detail = CallDetail(
            user_name=row["User name"],
            call_from=row["Call from"],
            call_to=row["Call to"],
            call_type=row["Call type"],
            dial_start_at=row["Dial begin time"],
            dial_answered_at=row["Call begin time"],
            dial_end_at=row["Call end time"],
            ringing_time=row["Ringing time"],
            call_duration=row["Call duration"],
            call_memo=row["Call memo"],
            call_charge="0",
        )
        key = call_detail.hash_key()
        if key in call_details:
            continue
        call_details[call_detail.hash_key()] = call_detail
    return call_details


def process_console_csv(
    file_path: str, call_details: dict[str, CallDetail]
) -> dict[str, CallDetail]:
    print(f"- Reading console file {file_path}...")
    df2 = pd.read_csv(file_path, low_memory=False).astype(str)
    for index, row in df2.iterrows():
        if row['call_type'] in ["OUTGOING_CALL", "OUTGOING_CALL_ABSENCE"]:
            continue
            # Normalize phone numbers before processing
            normalized_call_from = parse_phone_number(row["used_number"])
            normalized_call_to = parse_phone_number(row["number"])
        else:
            # If no match is found, add the call with its original type
            call_detail = CallDetail(
                user_name="",
                call_from=row["used_number"],
                call_to=row["number"],
                call_type=row["call_type"],
                dial_start_at=parse_jakarta_datetime(row["dial_starts_at"], row["pbx_region"]),
                dial_answered_at=parse_jakarta_datetime(row["dial_answered_at"], row["pbx_region"]),
                dial_end_at=parse_jakarta_datetime(row["dial_ends_at"], row["pbx_region"]),
                ringing_time=row["all_duration_of_call_sec_str"],
                call_duration=row["duration_of_call_sec_str"],
                call_memo="",
                call_charge=row["discount"],
            )
            key = call_detail.hash_key()
            if key not in call_details:
                print(f"Adding new call detail with call type: {call_detail.call_type}")
                call_details[key] = call_detail
    return call_details


def process_merged_csv(
    file_path: str, call_details: dict[str, CallDetail]
) -> dict[str, CallDetail]:
    """Reads a merged file and loads it to memory.
    Username, Call from, Call to, Call type, Dial starts at, Dial answered at, Dial ends at,
    Ringing time, Call duration,Call memo,Call charge
    """
    print(f"- Reading {file_path} file...")
    df3 = pd.read_csv(file_path, low_memory=False).astype(str)
    print("- Processing merged CSV file...")
    for index, row in df3.iterrows():
        call_detail = CallDetail(
            user_name=row["User name"],
            call_from=row["Call from"],
            call_to=row["Call to"],
            call_type=row["Call type"],
            dial_start_at=row["Dial starts at"],
            dial_answered_at=row["Dial answered at"],
            dial_end_at=row["Dial ends at"],
            ringing_time=row["Ringing time"],
            call_duration=row["Call duration"],
            call_memo=row["Call memo"],
            call_charge=row["Call charge"],
        )
        call_details[call_detail.hash_key()] = call_detail
    return call_details


def save_merged_csv(call_details: dict[str, CallDetail], output_path: str) -> None:
    print("- Saving merged CSV file...")
    call_details_list = []
    for key, value in call_details.items():
        call_details_list.append(value.to_dict())

    df = pd.DataFrame(call_details_list)
    df.to_csv(output_path, index=False)
