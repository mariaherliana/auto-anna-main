from datetime import datetime, timedelta, timezone
from typing import Optional

from src.idn_area_codes import EMERGENCY_NUMBERS, PHONE_PREFIXES, INTERNATIONAL_PHONE_PREFIXES


def call_hash(call_from: int, call_to: int, dial_start_at: datetime) -> str:
    return f"{call_from}_{call_to}_{dial_start_at}".replace(" ", "_")


def convert_to_jakarta_time_iso(original_date_str: str, region: str) -> datetime:
    if region != "jkt":
        raise Exception(
            "Timezone not supported. Only Jakarta time is supported for now."
        )

    # Parse the original date string in UTC time
    original_date = datetime.strptime(original_date_str, "%Y-%m-%d %H:%M:%S")
    utc_timezone = timezone.utc
    original_date_utc = original_date.replace(tzinfo=utc_timezone)

    # Add 7 hours to the original date to convert it to Jakarta time
    jakarta_offset = timedelta(hours=7)
    jakarta_date = original_date_utc + jakarta_offset
    jakarta_date = jakarta_date.replace(tzinfo=timezone(timedelta(hours=7)))
    return jakarta_date


def classify_number(phone_number: int, call_type: str) -> str:
    phone_number_str = str(phone_number)
    if call_type == "Internal Call":
        return "Internal Call"
    if call_type == "Internal Call (No answer)":
        return "Internal Call (No answer)"


    if len(phone_number_str) == 5:
        classification = EMERGENCY_NUMBERS.get(phone_number)
        if classification is not None:
            return classification

    if len(phone_number_str) == 3 or len(phone_number_str) == 4:
        classification = EMERGENCY_NUMBERS.get(phone_number)
        if classification is not None:
            return classification

     # Sort prefixes by length in descending order
    sorted_prefixes = sorted(map(str, PHONE_PREFIXES.keys()), key=len, reverse=True)

    for prefix in sorted_prefixes:
        if phone_number_str.startswith(prefix):
            return PHONE_PREFIXES.get(int(prefix))

    SPECIAL_PREFIXES = [211500, 211400, 21150, 21140, 1500, 1400, 800, 84, 31, 21, 8]
    for prefix in SPECIAL_PREFIXES:
        if phone_number_str.startswith(str(prefix)):
            return PHONE_PREFIXES.get(prefix)

    # Check against international prefixes
    for prefix, country in INTERNATIONAL_PHONE_PREFIXES.items():
        if phone_number_str.startswith(str(prefix).replace("+", "")):
            return f"International - {country}"

    return "Unknown number type"


def format_datetime_as_human_readable(datetime_object: Optional[datetime]) -> str:
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S") if datetime_object else "-"


def format_datetime_as_iso(datetime_object: datetime) -> str: # to be deleted
    return str(datetime_object).replace(" ", "T")


def format_timedelta(time_duration: timedelta) -> str:
    time_duration_str = str(time_duration)
    time_parts = time_duration_str.split(", ")
    time_str = time_parts[-1]
    return time_str


def format_username(user_name: str) -> str:
    return user_name if user_name else "-"


def parse_call_memo(memo: str) -> str:
    if memo == "" or memo == "nan":
        return "-"
    return memo


def parse_iso_datetime(datetime_str: str) -> datetime:
    return datetime.fromisoformat(datetime_str)


def parse_jakarta_datetime(datetime_str: str, region: str) -> str:
    if datetime_str == "nan":
        return "-"
    jakarta_iso_date = convert_to_jakarta_time_iso(datetime_str, region)
    return format_datetime_as_iso(jakarta_iso_date)


import phonenumbers

def parse_phone_number(phone_number: str) -> int | str:
    if phone_number == "scancall":
        return "scancall"
    try:
        cleaned_number = phone_number.replace("-", "")
        return int(float(cleaned_number))
    except:
        # print(f"Warning: {phone_number} is not a valid phone number.")
        return 0


def parse_time_duration(time_duration_string: str) -> timedelta:
    hours, minutes, seconds = time_duration_string.split(":")
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))