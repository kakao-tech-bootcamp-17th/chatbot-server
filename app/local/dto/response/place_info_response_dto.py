from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PlaceInfoResponseDto:
    place_name: str
    phone: str
    place_url: str
    distance: float

    @classmethod
    def from_data(cls, data: dict) -> PlaceInfoResponseDto:
        return cls(
            place_name=data['place_name'],
            phone=data['phone'],
            place_url=data['place_url'],
            distance=data['distance']
        )