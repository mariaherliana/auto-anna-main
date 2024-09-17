from src.utils import parse_phone_number, parse_iso_datetime, parse_time_duration, parse_call_memo, classify_number
from src.idn_area_codes import EMERGENCY_NUMBERS
import math
from src.utils import call_hash, classify_number, format_datetime_as_human_readable, format_timedelta, format_username, parse_call_memo, parse_iso_datetime, parse_phone_number

class CallDetail:
    def __init__(
        self,
        user_name: str,
        call_from: str,
        call_to: str,
        call_type: str,
        dial_start_at: str,
        dial_answered_at: str,
        dial_end_at: str,
        ringing_time: str,
        call_duration: str,
        call_memo: str,
        call_charge: str,
    ):
        self.user_name = user_name
        self.call_from = parse_phone_number(call_from)  # Normalizing here
        self.call_to = parse_phone_number(call_to)      # Normalizing here
        self.call_type = call_type
        self.dial_start_at = parse_iso_datetime(dial_start_at)
        self.dial_answered_at = (
            parse_iso_datetime(dial_answered_at) if dial_answered_at != "-" else None
        )
        self.dial_end_at = parse_iso_datetime(dial_end_at)
        self.ringing_time = parse_time_duration(ringing_time)
        self.call_duration = parse_time_duration(call_duration)
        self.call_memo = parse_call_memo(call_memo)
        self.call_charge = self.calculate_call_charge()
        self.number_type = classify_number(self.call_to, self.call_type)

    def calculate_call_charge(self) -> str:
        number_type = classify_number(self.call_to, self.call_type)
        if self.call_type in ["Internal Call", "Internal Call (No answer)"]:
            return "0"
        elif self.call_type not in ["OUTGOING_CALL", "Outbound call", "PREDICTIVE_DIAL"]: # Delete this part for those need inbound calculation
            return "0" # or some other default value
        else:
            if number_type in ["Premium Call", "Toll-Free", "Split Charge"] or number_type in EMERGENCY_NUMBERS.values():
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 1700
            elif number_type in {"International - USA", "International - SGP", "International - THAI", "International - JPN", "International - GER", "International - NZL"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 1250
            elif number_type in {"International - MY", "International - SK"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 1750
            elif number_type in {"International - LAO", "International - CRI"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 2500
            elif number_type in {"International - IND", "International - UK", "International - MXC"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 3000
            elif number_type in {"International - AUS", "International - BRZ"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 3500
            elif number_type in {"International - PHP", "International - UAE"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 4000
            elif number_type == "International - DOM":
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 5000
            elif number_type in {"International - MMR", "International - CAM"}:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 6500
            else:
                duration_in_minutes = self.call_duration.total_seconds() / 60
                rounded_duration = math.ceil(duration_in_minutes)
                call_charge = rounded_duration * 720
            return str(call_charge)

    def to_dict(self) -> dict:
        return {
            "User name": format_username(self.user_name),
            "Call from": self.call_from,
            "Call to": self.call_to,
            "Call type": self.call_type,
            "Number type": classify_number(self.call_to, self.call_type),
            "Dial starts at": format_datetime_as_human_readable(self.dial_start_at),
            "Dial answered at": format_datetime_as_human_readable(
                self.dial_answered_at
            ),
            "Dial ends at": format_datetime_as_human_readable(self.dial_end_at),
            "Ringing time": format_timedelta(self.ringing_time),
            "Call duration": format_timedelta(self.call_duration),
            "Call memo": self.call_memo,
            "Call charge": self.call_charge,
        }

    def hash_key(self) -> str:
        return call_hash(self.call_from, self.call_to, self.dial_start_at)
