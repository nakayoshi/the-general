from logic.calendar import CalendarImpl
import json


def test_command_parse():
    result = CalendarImpl._create_post_data("testtitle", "10/10", "japan")
    obj = {"value1": "10/10", "value2": "testtitle", "value3": "japan"}
    json_data = json.dumps(obj).encode("utf-8")
    assert result == json_data
