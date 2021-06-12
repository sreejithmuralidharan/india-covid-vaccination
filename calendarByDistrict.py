import requests
from datetime import datetime, timedelta

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
telegram_base_url = 'https://api.telegram.org/bot'
telegram_token = r"" # Get token from telegram
telegram_chat_id = "" # Get chat id from telegram
api_url_telegram = telegram_base_url+telegram_token+"/sendMessage?chat_id="+telegram_chat_id+"&text="


# get district codes from https://cdn-api.co-vin.in/api/v2/admin/location/districts/17  where 17 is the state code, e.g. Kerala = 17.
preferred_districts = [304, 307]

def request_api(district_id, date_range):
    query_params = "?district_id={}&date={}".format(district_id, date_range)
    url = base_cowin_url + query_params
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        parse_api_response(response)
    else:
        telegram_message = f"API responded with status code {response.status_code}"
        send_telegram_message(telegram_message)

def preferred_districts_availability(preferred_districts):
    for day in range(7):
        now = datetime.now() +  timedelta(days=day)
        date_range = now.strftime("%d-%m-%Y")
        for district in preferred_districts:
            request_api(district, date_range)

def parse_api_response(response):
    response_json = response.json()
    for center in response_json['centers']:
        for session in center['sessions']:
            if session['available_capacity_dose1']>1 and session['min_age_limit']==45:
                telegram_message = f"{center['district_name']} District - {center['name']} ( {center['address']}) have {session['available_capacity_dose1']} doses available for age {session['min_age_limit']}"
                print(telegram_message)
                send_telegram_message(telegram_message)

def send_telegram_message(telegram_message):
    url = api_url_telegram+telegram_message
    response = requests.get(url)
    print(response)

if __name__ == "__main__":
    preferred_districts_availability(preferred_districts)
