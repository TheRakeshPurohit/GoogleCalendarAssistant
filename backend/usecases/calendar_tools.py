from typing import Type
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from usecases import get_calendar_events


class CalendarEventSearchInput(BaseModel):
    """Inputs for get_calendar_events"""

    user_email: str = Field(description="email of the user")
    calendar_id: str = Field(description="Calendar id of the calendar")
    start_date: str = Field(
        description="Start date of the events to search. Must be an RFC3339 timestamp with mandatory time zone offset, for example, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. "
    )
    end_date: str = Field(
        description="End date of the events to search. Must be an RFC3339 timestamp with mandatory time zone offset, for example, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z."
    )


class GetCalendarEventsTool(BaseTool):
    name = "get_calendar_events"
    description = """
        Useful when you want to get calendar events in a particular date or time range after you have retrieved the current time.
        """
    args_schema: Type[BaseModel] = CalendarEventSearchInput

    def _run(self, user_email: str, calendar_id: str, start_date: str, end_date: str):
        events_response = get_calendar_events(
            user_email, calendar_id, start_date, end_date
        )
        return events_response

    def _arun(self):
        raise NotImplementedError("get_calendar_events does not support async")


class CurrentTimeInput(BaseModel):
    """Inputs for getting the current time"""

    pass


class CurrentTimeTool(BaseTool):
    name = "get_current_time"
    description = """
    Useful when you want to get the current time in an RFC3339 timestamp with mandatory time zone offset, for example, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z.
    """
    args_schema: Type[BaseModel] = CurrentTimeInput

    def _run(self):
        # Return the current time in a format google calendar api can understand
        return (datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),)

    def _arun(self):
        raise NotImplementedError("convert_time does not support async")


class TimeDeltaInput(BaseModel):
    """Inputs for getting time deltas"""

    delta_days: int = Field(
        description="Number of days to add to the current time. Must be an integer."
    )
    delta_hours: int = Field(
        description="Number of hours to add to the current time. Must be an integer."
    )
    delta_minutes: int = Field(
        description="Number of minutes to add to the current time. Must be an integer."
    )
    delta_seconds: int = Field(
        description="Number of seconds to add to the current time. Must be an integer."
    )


class TimeDeltaTool(BaseTool):
    name = "get_future_time"
    description = """
    Useful when you want to get a future time in an RFC3339 timestamp, given a time delta such as 1 day, 2 hours, 3 minutes, 4 seconds. 
    """
    args_schema: Type[BaseModel] = TimeDeltaInput

    def _run(
        self, delta_days: int, delta_hours: int, delta_minutes: int, delta_seconds: int
    ):
        # Return the current time in a format google calendar api can understand
        return (
            datetime.utcnow()
            + timedelta(
                days=delta_days,
                hours=delta_hours,
                minutes=delta_minutes,
                seconds=delta_seconds,
            )
        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _arun(self):
        raise NotImplementedError("get_future_time does not support async")


# TODO: Set up a tool to convert natural language time to a datetime accepted by the google calendar api