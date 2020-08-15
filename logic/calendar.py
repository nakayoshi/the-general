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
    starttime: str
    endtime: str
    location: str

    @staticmethod
    def _get_datetime(date, time) -> str:
        today = datetime.datetime.today()
        splitteddate = date.split("/")
        splittedtime = time.split(":")

        return datetime.datetime(
            today.year,
            int(splitteddate[0]),
            int(splitteddate[1]),
            int(splittedtime[0]),
            int(splittedtime[1]),
        ).isoformat()

    @property
    def get_starttime(self) -> str:
        startdatetime = Event._get_datetime(self.date, self.starttime)

        return startdatetime

    @property
    def get_endtime(self) -> str:
        enddatetime = Event._get_datetime(self.date, self.endtime)

        return enddatetime


class ICalendar(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def _get_service():
        pass

    @staticmethod
    @abstractmethod
    def _create_event_obj(newevent: Event) -> Dict:
        pass

    @classmethod
    @abstractmethod
    def add_event(cls, newevent: Event) -> Optional[Dict]:
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
    def _create_event_obj(newevent: Event) -> Dict:
        body = {
            "summary": newevent.title,
            "location": newevent.location,
            "start": {"dateTime": newevent.get_starttime, "timeZone": "Japan",},
            "end": {"dateTime": newevent.get_endtime, "timeZone": "Japan"},
        }

        return body

    @classmethod
    def add_event(cls, newevent: Event) -> None:
        body = GoogleCalendarImpl._create_event_obj(newevent)
        service = GoogleCalendarImpl._get_service()

        service.events().insert(calendarId=getenv("CALENDAR_ID"), body=body).execute()


class GoogleCalendarMockImpl(ICalendar):
    @staticmethod
    def _get_service():
        pass

    @staticmethod
    def _create_event_obj(newevent: Event) -> Dict:
        body = {
            "summary": newevent.title,
            "location": newevent.location,
            "start": {"dateTime": newevent.get_starttime, "timeZone": "Japan",},
            "end": {"dateTime": newevent.get_endtime, "timeZone": "Japan"},
        }

        return body

    @classmethod
    def add_event(cls, newevent: Event) -> Dict:
        body = GoogleCalendarMockImpl._create_event_obj(newevent)

        return body

