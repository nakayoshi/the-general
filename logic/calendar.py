import json
import urllib.request
from os import getenv
from dataclasses import dataclass


@dataclass
class Event:
    title: str
    date: str
    starttime: str
    endtime: str
    location: str


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
