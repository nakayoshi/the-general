import json
import urllib.request
from os import getenv


class CalendarImpl:
    def _create_post_data(
        title: str, date: str, starttime: str, endtime: str, location: str
    ) -> bytes:

        obj = {
            "title": title,
            "date": date,
            "starttime": starttime,
            "endtime": endtime,
            "location": location,
        }
        json_data = json.dumps(obj).encode("utf-8")

        return json_data

    @classmethod
    def add_event(
        cls, title: str, date: str, starttime: str, endtime: str, location: str
    ) -> None:
        # set up POST data
        url = getenv("CALENDAR_WEBHOOK_URL")
        method = "POST"
        headers = {"Content-Type": "application/json"}
        json_data = CalendarImpl._create_post_data(
            title, date, starttime, endtime, location
        )

        # http request
        request = urllib.request.Request(
            url, data=json_data, method=method, headers=headers
        )
        urllib.request.urlopen(request)
