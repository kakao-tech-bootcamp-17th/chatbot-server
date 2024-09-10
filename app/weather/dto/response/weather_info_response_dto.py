from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class WeatherInfoResponseDto:
    address: str
    coordinate: dict
    weather: WeatherInfoResponseDto.WeatherInfo

    @classmethod
    def from_data(cls, address: str, data: dict) -> WeatherInfoResponseDto:
        print(data['coord'])
        return cls (
            address=address,
            coordinate=data['coord'],
            weather=cls.WeatherInfo.from_data(data)
        )

    # weather inner class
    @dataclass(frozen=True)
    class WeatherInfo:
        temperature: float
        description: str
        feels_like: float
        humidity: int
        city: str

        @classmethod
        def from_data(cls, data: dict):
            return cls(
                temperature=data['main']['temp'],
                feels_like=data['main']['feels_like'],
                humidity=data['main']['humidity'],
                description=data['weather'][0]['description'],
                city=data['name']
            )

    
    