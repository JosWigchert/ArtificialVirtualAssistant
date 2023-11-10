import json


def get_current_weather(location: str, unit: ["celsius", "fahrenheit"] = "celsius"):
    """
    Get the current weather in a given location.

    Parameters:
        location (str): The location for which to retrieve the weather information.
        unit (["celsius", "fahrenheit"], optional): The unit of temperature to return (default is "celsius").

    Returns:
        str: A JSON string containing the weather information.
    """
    weather_info = {
        "location": location,
        "temperature": "17",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)
