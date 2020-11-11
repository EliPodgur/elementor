import requests
import base64
from collections import Counter


bad_codes = ['malicious','phishing','malware']



class UrlData:
    def __init__(self, api_key):
        self._headers = {'x-apikey': api_key}

    def get_data(self, url: str) -> dict:
        url_id = base64.urlsafe_b64encode(f"{url}".encode()).decode().strip("=")
        requests.post(f'https://www.virustotal.com/api/v3/urls/{url_id}/analyse', headers=self._headers)

        r = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=self._headers)
        return r.json()


class ResponseAnalyzer:
    @staticmethod
    def get_categories(json: dict) -> Counter:
        categories = json['data']['attributes']['categories']
        return Counter(categories.values())

    @staticmethod
    def get_votes_and_verdict(json: dict) -> (Counter, bool):
        votes = json['data']['attributes']['last_analysis_results']
        votes = [vote['result'] for vote in votes.values()]
        votes = Counter(votes)
        check = any(item in votes.keys() for item in bad_codes)
        verdict = 'risk' if check else 'safe'
        return votes, verdict

    @staticmethod
    def get_utc_time(json):
        return json['data']['attributes']['last_analysis_date']