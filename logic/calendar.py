import urllib.request, json
from os import getenv

class CalendarImpl:
    def _create_post_data(title: str, date: str, location: str) -> bytes:

        obj = {"value1" : date, "value2" : title, "value3" : location} 
        json_data = json.dumps(obj).encode("utf-8")

        return json_data

    @classmethod
    def add_event(cls, text: str):
        message = "Success!"        

        # set up POST data
        url = getenv("CALENDAR_WEBHOOK")
        method = "POST"
        headers = {"Content-Type": "application/json"}

        json_data= command_parse(text)

        # http request
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        urllib.request.urlopen(request)

        return message