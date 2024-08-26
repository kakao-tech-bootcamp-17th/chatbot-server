class PlacesResponseDTO:
    def __init__(self, ext_response):
        self._id = ext_response['id']
        self._place_name = ext_response['place_name']
        self._phone = ext_response['phone']
        self._place_url = ext_response['place_url']
        self._distance = ext_response['distance']

    def to_dict(self):
        return {
            'id': self._id,
            'place_name': self._place_name,
            'phone': self._phone,
            'place_url': self._place_url,
            'distance': self._distance
        }