import datetime
import json
import urllib.request
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from os import getenv

from google.oauth2 import service_account
from googleapiclient.discovery import build


@dataclass
class Event:
    title: str
    date: str
    starttime: str
    endtime: str
    location: str

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
        datetime = Event._get_datetime(self.date, self.starttime)

        return datetime

    @property
    def get_endtime(self) -> str:
        datetime = Event._get_datetime(self.date, self.endtime)

        return datetime


class ICalendar(metaclass=ABCMeta):
    @abstractmethod
    def _get_service():
        pass

    @abstractmethod
    def _create_event_obj(newevent: Event) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def add_event(cls, newevent: Event) -> None:
        pass


class GoogleCalendarImpl(ICalendar):
    def _get_service():
        credentials = service_account.Credentials.from_service_account_file("key.json")
        scoped_credentials = credentials.with_scopes(
            ["https://www.googleapis.com/auth/calendar"]
        )
        service = build("calendar", "v3", credentials=scoped_credentials)

        return service

    def _create_event_obj(newevent) -> dict:
        body = {
            "summary": newevent.title,
            "location": newevent.location,
            "start": {"dateTime": newevent.get_starttime, "timeZone": "Japan",},
            "end": {"dateTime": newevent.get_endtime, "timeZone": "Japan"},
        }

        return body

    @classmethod
    def add_event(cls, newevent) -> None:
        body = GoogleCalendarImpl._create_event_obj(newevent)
        service = GoogleCalendarImpl._get_service()

        event = (
            service.events()
            .insert(calendarId=getenv("CALENDAR_ID"), body=body)
            .execute()
        )


class CalendarImpl:
    def _create_post_data(newevent) -> bytes:

        obj = {
            "title": newevent.title,
            "date": newevent.date,
            "starttime": newevent.starttime,
            "endtime": newevent.endtime,
            "location": newevent.location,
        }
        json_data = json.dumps(obj).encode("utf-8")

        return json_data

    @classmethod
    def add_event(cls, newevent) -> None:
        # set up POST data
        url = getenv("CALENDAR_WEBHOOK_URL")
        method = "POST"
        headers = {"Content-Type": "application/json"}
        json_data = CalendarImpl._create_post_data(newevent)

        # http request
        request = urllib.request.Request(
            url, data=json_data, method=method, headers=headers
        )
        urllib.request.urlopen(request)
