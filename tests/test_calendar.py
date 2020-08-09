from logic.calendar import CalendarImpl
import json

sample_command = "testtitle -d 10/10 -l japan"


def test_command_parse():
    result = CalendarImpl.command_parse(text=sample_command)
    obj = {"value1": "10/10", "value2": "testtitle", "value3": "japan"}
    json_data = json.dumps(obj).encode("utf-8")
    assert result == json_data
