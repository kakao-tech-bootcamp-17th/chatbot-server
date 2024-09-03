# dto/response/weather_info_by_address_dto.py
from __future__ import annotations
from dataclasses import dataclass
from ....local.dto.response.place_coordinate_response_dto import PlaceCoordinateResponseDto
from .weather_info_response_dto import WeatherInfoResponseDto

@dataclass(frozen=True)
class WeatherInfoByAddressDto:
    address: str
    coordinates: PlaceCoordinateResponseDto
    weather: WeatherInfoResponseDto  # 추가: 날씨 정보 필드 추가
    
    @classmethod
    def from_data(cls, address: str, coordinates: dict, weather: WeatherInfoResponseDto) -> WeatherInfoByAddressDto:
        coordinate_dto = PlaceCoordinateResponseDto.from_data(coordinates)
        print("cls",cls)
        return cls(
            address=address,
            coordinates=coordinate_dto,
            weather=weather 
        )