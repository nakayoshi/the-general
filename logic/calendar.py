import datetime
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from os import getenv
from typing import Dict, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build


@dataclass
class Event:
    title: str
    date: str
    start_time: str
    end_time: str
    location: str

    @staticmethod
    def _get_datetime(date, time) -> str:
        today = datetime.datetime.today()
        splitted_date = date.split("/")
        splitted_time = time.split(":")

        return datetime.datetime(
            today.year,
            int(splitted_date[0]),
            int(splitted_date[1]),
            int(splitted_time[0]),
            int(splitted_time[1]),
        ).isoformat()

    @property
    def get_start_time(self) -> str:
        start_datetime = Event._get_datetime(self.date, self.start_time)

        return start_datetime

    @property
    def get_end_time(self) -> str:
        end_datetime = Event._get_datetime(self.date, self.end_time)

        return end_datetime


class ICalendar(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def _get_service():
        pass

    @staticmethod
    @abstractmethod
    def _create_event_obj(new_event: Event) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def add_event(cls, new_event: Event) -> Optional[Dict]:
        pass


class GoogleCalendarImpl(ICalendar):
    @staticmethod
    def _get_service():
        credentials = service_account.Credentials.from_service_account_file("key.json")
        scoped_credentials = credentials.with_scopes(
            ["https://www.googleapis.com/auth/calendar"]
        )
        service = build("calendar", "v3", credentials=scoped_credentials)

        return service

    @staticmethod
    def _create_event_obj(new_event: Event) -> Dict:
        body = {
            "summary": new_event.title,
            "location": new_event.location,
            "start": {"dateTime": new_event.get_start_time, "timeZone": "Japan",},
            "end": {"dateTime": new_event.get_end_time, "timeZone": "Japan"},
        }

        return body

    @classmethod
    def add_event(cls, new_event: Event) -> None:
        body = GoogleCalendarImpl._create_event_obj(new_event)
        service = GoogleCalendarImpl._get_service()

        service.events().insert(calendarId=getenv("CALENDAR_ID"), body=body).execute()


class GoogleCalendarMockImpl(ICalendar):
    @staticmethod
    def _get_service():
        pass

    @staticmethod
    def _create_event_obj(new_event: Event) -> Dict:
        body = {
            "summary": new_event.title,
            "location": new_event.location,
            "start": {"dateTime": new_event.get_start_time, "timeZone": "Japan",},
            "end": {"dateTime": new_event.get_end_time, "timeZone": "Japan"},
        }

        return body

    @classmethod
    def add_event(cls, new_event: Event) -> Dict:
        body = GoogleCalendarMockImpl._create_event_obj(new_event)

        return body
