from __future__ import annotations
from dataclasses import dataclass



@dataclass(frozen=True)
class PlaceCoordinateResponseDto:
    lat: float
    lon: float
        
    @classmethod
    def from_data(cls, data:dict) -> PlaceCoordinateResponseDto:
        return cls(
            lon=data['x'], 
            lat=data['y']
        )

