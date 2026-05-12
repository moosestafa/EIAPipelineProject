import requests
import os
from dotenv import load_dotenv

load_dotenv()
#fetches api key
eia_key = os.getenv("EIA_API_KEY")


#makes api request, checks for any errors with the request, returns json data
def fetch_data(state, start_month, end_month):
    url = f"https://api.eia.gov/v2/petroleum/crd/crpdn/data/?frequency=monthly&data[0]=value&facets[duoarea][]=S{state}&start={start_month}&end={end_month}&sort[0][column]=duoarea&sort[0][direction]=desc&offset=0&length=5000&api_key={eia_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
""""
data = fetch_data("TX","2026-01","2026-01")
print(data)
print(len(data["response"]["data"]))
"""