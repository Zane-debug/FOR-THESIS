class ApiClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def send_transcript(self, transcript):
        import requests

        response = requests.post(f"{self.base_url}/process", json={"transcript": transcript})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_recommendations(self, topic):
        import requests

        response = requests.get(f"{self.base_url}/recommendations", params={"topic": topic})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()