import json

from logic.calendar import CalendarImpl, Event


def test_command_parse():
    newevent = Event("testtitle", "10/10", "10:00", "11:00", "japan")
    result = CalendarImpl._create_post_data(newevent)
    obj = {
        "title": "testtitle",
        "date": "10/10",
        "starttime": "10:00",
        "endtime": "11:00",
        "location": "japan",
    }
    json_data = json.dumps(obj).encode("utf-8")
    assert result == json_data
