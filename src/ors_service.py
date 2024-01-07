import requests
class ors_service:
    def __init__(self, token):
            self.directions_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
            self.headers = {
                'Accept': 'application/json; charset=utf-8',
                'Authorization': f'{token}',
                'Content-Type': 'application/json; charset=utf-8'
            }       


    def get_directions(self, start = [8.681495,49.41461], end = [8.687872,49.420318]):
        body = {
            'coordinates': [
                start,
                end
            ],
        }
        response = requests.post(self.directions_url, json=body, headers=self.headers)
        return response.json()
