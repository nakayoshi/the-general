import json

from logic.calendar import GoogleCalendarImpl, Event


def test_command_parse():
    calendar = GoogleCalendarImpl()
    newevent = Event("testtitle", "10/10", "10:00", "11:00", "japan")
    result = calendar._create_event_obj(newevent)
    obj = {
        "summary": "testtitle",
        "location": "japan",
        "start": {"dateTime": "2020-10-10T10:00:00", "timeZone": "Japan"},
        "end": {"dateTime": "2020-10-10T11:00:00", "timeZone": "Japan"},
    }
    assert result == obj
