from logic.calendar import Event, GoogleCalendarMockImpl


def test_command_parse():
    calendar = GoogleCalendarMockImpl()
    newevent = Event("testtitle", "10/10", "10:00", "11:00", "japan")
    result = calendar.add_event(newevent)
    obj = {
        "summary": "testtitle",
        "location": "japan",
        "start": {"dateTime": "2020-10-10T10:00:00", "timeZone": "Japan"},
        "end": {"dateTime": "2020-10-10T11:00:00", "timeZone": "Japan"},
    }
    assert result == obj
