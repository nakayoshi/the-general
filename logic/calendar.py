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

    def get_datetime_starttime(self) -> str:
        today = datetime.date.today()
        splitteddate = self.date.split("/")
        stime = self.starttime.split(":")

        return datetime.datetime(
            today.year,
            int(splitteddate[0]),
            int(splitteddate[1]),
            int(stime[0]),
            int(stime[1]),
        ).isoformat()

    def get_datetime_endtime(self) -> str:
        today = datetime.date.today()
        splitteddate = self.date.split("/")
        etime = self.endtime.split(":")

        return datetime.datetime(
            today.year,
            int(splitteddate[0]),
            int(splitteddate[1]),
            int(etime[0]),
            int(etime[1]),
        ).isoformat()


class ISheduleRepository(metaclass=ABCMeta):
    @abstractmethod
    def _get_service():
        pass

    @abstractmethod
    def _create_shedule_obj(newevent: Event) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def add_schedule(cls, newevent: Event) -> None:
        pass


class GoogleCalendarImpl(ISheduleRepository):
    def _get_service():
        credentials = service_account.Credentials.from_service_account_file("key.json")
        scoped_credentials = credentials.with_scopes(
            ["https://www.googleapis.com/auth/calendar"]
        )
        service = build("calendar", "v3", credentials=scoped_credentials)

        return service

    def _create_shedule_obj(newevent) -> bytes:
        body = {
            "summary": newevent.title,
            "location": newevent.location,
            "start": {
                "dateTime": newevent.get_datetime_starttime(),
                "timeZone": "Japan",
            },
            "end": {"dateTime": newevent.get_datetime_endtime(), "timeZone": "Japan"},
        }

        return body

    @classmethod
    def add_schedule(cls, newevent) -> None:
        body = GoogleCalendarImpl._create_shedule_obj(newevent)
        service = GoogleCalendarImpl._get_service()

        event = (
            service.events()
            .insert(calendarId=getenv("CALENDAR_ID"), body=body,)
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
