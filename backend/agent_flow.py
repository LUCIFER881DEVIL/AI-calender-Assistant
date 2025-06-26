# backend/agent_flow.py

from datetime import datetime, timedelta
from backend.google_calendar import get_upcoming_events, create_event
from dateutil.parser import parse
import re

async def run_agent_flow(message: str) -> str:
    # Step 1: Extract time/date info
    lower_msg = message.lower()
    
    # Basic keyword match
    if "tomorrow" in lower_msg:
        date = datetime.now() + timedelta(days=1)
    elif "today" in lower_msg:
        date = datetime.now()
    else:
        # fallback: no date = can't proceed
        return "Please specify a valid date (e.g., today, tomorrow, Friday)."

    # Step 2: Extract time window from message
    match = re.search(r'(\d{1,2})(?:\s*-\s*|\s*to\s*)(\d{1,2})', message)
    if not match:
        return "Please specify a time range (like '3 to 5 PM') to book the meeting."

    start_hour = int(match.group(1))
    end_hour = int(match.group(2))
    if "pm" in lower_msg and start_hour < 12:
        start_hour += 12
        end_hour += 12

    start_time = date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end_time = date.replace(hour=end_hour, minute=0, second=0, microsecond=0)

    # Step 3: Check calendar events
    events = get_upcoming_events()
    available_slot = None

    # Naive check for conflicts
    for hour in range(start_hour, end_hour):
        slot_start = date.replace(hour=hour, minute=0)
        slot_end = date.replace(hour=hour+1, minute=0)
        conflict = False
        for event in events:
            event_start_str = event['start'].get('dateTime', '')
            if event_start_str:
                event_start = parse(event_start_str)
                if event_start.hour == hour:
                    conflict = True
                    break
        if not conflict:
            available_slot = (slot_start, slot_end)
            break

    if not available_slot:
        return "No free slots available in that time window."

    # Step 4: Book the slot
    create_event(
        start=available_slot[0].isoformat(),
        end=available_slot[1].isoformat(),
        summary="Booked via AI Assistant"
    )
    return f"Meeting booked on {available_slot[0].strftime('%A %I:%M %p')}!"

