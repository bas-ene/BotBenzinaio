import requests
class ors_service:
    def __init__(self, token):
            self.directions_url = 'https://api.openrouteservice.org/v2/directions/driving-car'
            self.headers = {
                'Accept': 'application/json; charset=utf-8',
                'Authorization': f'{token}',
                'Content-Type': 'application/json; charset=utf-8'
            }       


    def getDirections(self, start = {'longitude': 8.681495, 'longitude': 49.41461}, end = {'longitude': 8.681495, 'longitude': 49.41461}):
        body = {
            'coordinates': [
                [start['longitude'], start['latitude']],
                [end['longitude'], end['latitude']]
            ],
        }
        response = requests.post(self.directions_url, json=body, headers=self.headers)
        return response.json()

    def getDistance(self, jsondata):
        return jsondata['routes'][0]['summary']['distance']
