import requests
from datetime import datetime


base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

api_url_telegram = "https://api.telegram.org/botenteryourbotidhere/sendMessage?chat_id=@__groupid__&text="
# Change "enteryourbotidhere" to your bot id.
# something like: https://api.telegram.org/botdjwjw1690snklnm3890j5j5k/sendMessage?chat_id=@__groupid__&text=


now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
group_id = ""       # Enter your telegram group id here


name_list = []


def fetch_data_from_cowin(district_id):
    querry_params = "?district_id={}&date={}".format(district_id, today_date)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'}
    # If this header is not working try changing the header to your personal header
    # If can be found at https://www.whatismybrowser.com/detect/what-is-my-user-agent
    final_url = base_cowin_url + querry_params
    response = requests.get(final_url, headers=headers)
    extract_availability_data(response)


def extract_availability_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        for session in center["sessions"]:

            if session["available_capacity"] > 0 and session["min_age_limit"] == 18:    # for 18+ vaccine
                if int(center["center_id"]) not in name_list:
                    message = "Vaccination centers for {}+ age group: \n{} ({})- Pin: {}. \nVaccine: {} \nFee Type: {} \nTotal  {} slots are available on {} \n(Dose 1: {}, Dose 2: {})".format(
                        session["min_age_limit"],
                        center["name"],
                        center["block_name"],
                        center["pincode"],
                        session["vaccine"],
                        center["fee_type"],
                        session["available_capacity"],
                        session["date"],
                        session["available_capacity_dose1"],
                        session["available_capacity_dose2"]
                    )

                    name_list.append(int(center["center_id"]))
                    print(name_list)
                    message = message + "\n\nCoWin: https://selfregistration.cowin.gov.in"
                    send_message_telegram(message)


def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)


while(True):
    fetch_data_from_cowin(296)

# 296 is of Trivandrum district
# Change it your prefered district
