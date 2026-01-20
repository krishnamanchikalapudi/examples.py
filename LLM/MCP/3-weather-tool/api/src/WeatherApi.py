import logging
import ssl

import httpx
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app instance
app = FastAPI(title="Weather API", description="Weather information API using wttr.in")


class WeatherResponse(BaseModel):
    """Response model for weather data"""
    city: str = Field(default="San Francisco")
    temperature: float = Field(default=0.0)
    description: str = Field(default="")
    icon: str = Field(default="")


@app.get("/city/{city}", response_model=WeatherResponse)
async def get_city_weather(city: str) -> WeatherResponse:
    """Get weather information for a city using HTTP request"""
    logging.info("API: Processing weather request for %s", city)
    try:
        # Disable SSL verification for wttr.in to avoid certificate issues
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            # Using wttr.in as a free weather API
            url = f"https://wttr.in/{city}?format=j1"
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current_condition", [{}])[0]
                temp_c = float(current.get("temp_C", 0))
                desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
                icon = current.get("weatherIconUrl", [{}])[0].get("value", "")
                return WeatherResponse(
                    city=city,
                    temperature=temp_c,
                    description=desc,
                    icon=icon
                )
            return WeatherResponse(
                city=city,
                temperature=0.0,
                description=f"Unable to fetch weather for {city}",
                icon=""
            )
    except ssl.SSLError as e:
        logging.error("Weather SSL error: %s", e)
        return WeatherResponse(
            city=city,
            temperature=0.0,
            description=f"SSL error fetching weather for {city}: {str(e)}",
            icon=""
        )
    except Exception as e:
        logging.error("Weather HTTP request failed: %s", e)
        return WeatherResponse(
            city=city,
            temperature=0.0,
            description=f"Error fetching weather for {city}: {str(e)}",
            icon=""
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Weather API - Use /city/{city} to get weather information"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
