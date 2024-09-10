from dataclasses import dataclass

METER_TO_KILOMETER = 1000.0
MILLIS_TO_MINUTES = 60000

@dataclass(frozen=True)
class TrafficInfoResponseDto:
    distance: float
    duration: int
    fuel_price: int
    taxi_fare: int
    toll_fare: int
    start_location: str
    goal_location: str

    @classmethod
    def from_data(cls, data, start_location, goal_location):
        return cls(
            distance=data['distance'] / METER_TO_KILOMETER,
            duration=data['duration'] // MILLIS_TO_MINUTES,
            fuel_price=data['fuelPrice'],
            taxi_fare=data['taxiFare'],
            toll_fare=data['tollFare'],
            start_location=start_location,
            goal_location=goal_location
        )