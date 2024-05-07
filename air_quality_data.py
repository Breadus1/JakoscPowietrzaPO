import requests

class AirQualityAPI:
    def __init__(self, api_token: str):
        self.token = api_token
        self.base_endpoint = "http://api.airvisual.com/v2"

    def get_city_air_quality(self, city: str, region: str, country: str) -> dict:
        url = f"{self.base_endpoint}/city?city={city}&state={region}&country={country}&key={self.token}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        return response.json()

if __name__ == "__main__":
    client = AirQualityAPI("9f6dc684-6e16-44b5-8d78-40f208b4a000")
    try:
        warsaw_data = client.get_city_air_quality("Warsaw", "Mazovia", "Poland")
        print(warsaw_data)
    except Exception as err:
        print(f"Error: {err}")
