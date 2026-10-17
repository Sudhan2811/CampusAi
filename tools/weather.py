
import requests


def get_weather(location: str):
    try:
        location = location.strip()

        if not location:
            return {
                "success": False,
                "error": "Please provide a city or location."
            }

        # Step 1: Find the location anywhere in the world
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "success": False,
                "error": f"Location '{location}' was not found."
            }

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Step 2: Fetch current weather for that location
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "is_day,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        return {
            "success": True,
            "location": place["name"],
            "country": place.get("country", "Unknown"),
            "temperature_c": current["temperature_2m"],
            "feels_like_c": current["apparent_temperature"],
            "humidity_percent": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "precipitation_mm": current["precipitation"],
            "is_day": bool(current["is_day"]),
            "weather_code": current["weather_code"],
            "timezone": weather_data.get("timezone")
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Weather API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_weather_forecast(location: str):
    try:
        location = location.strip()

        if not location:
            return {
                "success": False,
                "error": "Please provide a city or location."
            }

        # Find the location
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "success": False,
                "error": f"Location '{location}' was not found."
            }

        place = geo_data["results"][0]

        # Fetch a 7-day forecast
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_probability_max,"
                    "precipitation_sum"
                ),
                "timezone": "auto",
                "forecast_days": 7
            },
            timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        daily = weather_data["daily"]

        forecast = []

        for i in range(len(daily["time"])):
            forecast.append({
                "date": daily["time"][i],
                "weather_code": daily["weather_code"][i],
                "max_temp_c": daily["temperature_2m_max"][i],
                "min_temp_c": daily["temperature_2m_min"][i],
                "precipitation_probability_percent":
                    daily["precipitation_probability_max"][i],
                "precipitation_mm": daily["precipitation_sum"][i]
            })

        return {
            "success": True,
            "location": place["name"],
            "country": place.get("country", "Unknown"),
            "timezone": weather_data.get("timezone"),
            "forecast": forecast
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Weather API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

