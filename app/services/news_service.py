import requests
import os

API_KEY = os.getenv('NEWS_API_KEY', '1e642381fe9d49ae8a5554db83d01aa1')
BASE = 'https://newsapi.org/v2'

def top_headlines(country='us', category=None):
    params = {'apiKey': API_KEY, 'country': country}
    if category:
        params['category'] = category
    r = requests.get(f'{BASE}/top-headlines', params=params, timeout=10)
    r.raise_for_status()
    return r.json()
