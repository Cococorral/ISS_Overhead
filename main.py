import requests
from datetime import datetime
import smtplib

my_email = "write your email here"
password = "write your password here"

MY_LAT = 64.126518
MY_LONG = -21.817438

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


def overhead():
    if 69 >= iss_latitude >= 59:
        if -27 <= iss_longitude <= -17:
            return True
        else:
            return False
    else:
        return False


# and if it is currently dark

time_now = str(datetime.now())
time_now = time_now.split(" ")[1].split(":")[0]
time_now = int(time_now)


def daylight():
    if sunset >= time_now >= sunrise:
        return True
    else:
        return False


# Then email me to tell me to look up.
if overhead() == True and daylight() == False:
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs="write the email receipt here",
                        msg="Subject:LOOK UP! \n\nISS is overhead!")
    connection.close()

