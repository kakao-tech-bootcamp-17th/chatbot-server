from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class WeatherInfoResponseDto:
    temperature: float
    description: str
    city: str

    @classmethod
    def from_data(cls, data: dict) -> WeatherInfoResponseDto:
        temperature = data.get('main', {}).get('temp')
        description = data.get('weather', [{}])[0].get('description')
        city = data.get('name')
        return cls(
            temperature=temperature,
            description=description,
            city=city
        )