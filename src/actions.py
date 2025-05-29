import requests 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import datetime


def def_vol(value, inc:bool = False):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_vol = volume.GetMasterVolumeLevelScalar()
    
    value = float(value)
    set_vol = current_vol + value if inc else value / 100
    set_vol = max(0.0, min(set_vol, 1.0)) # Aceita valores entre 0 e 1
    
    volume.SetMasterVolumeLevelScalar(set_vol, None)
    
    print(f"Volume anterior: {current_vol}")
    get_vol()

def get_vol():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_vol = volume.GetMasterVolumeLevelScalar()
    
    print(f"Atualmente o volume esta em {(current_vol*100):.2f}%")

def get_time():
    full_datetime = datetime.datetime.now()
    
    hour = full_datetime.hour
    minute = full_datetime.minute
    second = full_datetime.second
    microsecond = full_datetime.microsecond
    
    print(f"São {hour}:{minute}:{second}")
    # print("HORAS: ", full_datetime)
    
# Precisão Razoavel
def open_weather(city: str) -> dict:
    weather_response = dict()
    api_key = "17160d89448d96a62bbb0b1223f48bea"
    
    # iranduba,am,br
    city = city.lower()
    
    weather = "weather" # Temperatura
    
    # https://api.openweathermap.org/data/2.5/onecall?
    # lat=-3.2847&
    # lon=-60.1861&
    # appid=YOUR_API_KEY&
    # units=metric&
    # lang=pt_br

    
    url = f"http://api.openweathermap.org/data/2.5/{weather}"
    
    params = {
        "q": city,
        "appid": api_key,
        "lang": "pt_br",
        "units": "metric"
    }
    
    response = requests.get(url, params)
    
    
    if response.status_code == 200:
        data = response.json()
        
        weather_response = {
            "weather": {
                "description": data["weather"][0]["description"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
            }, 
            "cord": {
                "lat": data["coord"]["lat"],
                "lon": data["coord"]["lon"],   
            },
            "city_name": data["name"],
        }
        
        # print(weather_response["weather_des"], weather_response["temp"], weather_response["city_name"], weather_response["feels_like"], weather_response["lat"], weather_response["lon"])
        # print(data)
    else:
        print(f"Erro ao buscar o clima: {response.status_code} - {response.text}")
        
    
    # print(weather_response)
    return weather_response

# Precisão Alta
def tommorow_weather(city: str) -> dict:
    weather_response = dict()
    result_op_w = open_weather(city)
    
    lat = result_op_w["cord"]["lat"]
    lon = result_op_w["cord"]["lon"]
    
    api_key = "3Wp0bmAHHVNp7Pu6jUNr4woQAQ2nutFD"
    
    
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={api_key}"
    
    response = requests.get(url)
    
    # print(response.json())
    
    if response.status_code == 200:
        data = response.json()
        weather_response = {
            "weather": {
                "temp": data["data"]["values"]["temperature"], 
                "feels_like": data["data"]["values"]["temperatureApparent"],
                "precipitation_probability": data["data"]["values"]["precipitationProbability"]
            }, 
            "cord": {
                "lat": data["location"]["lat"],
                "lon": data["location"]["lon"],   
            }
        }
    else:
        print(f"Erro ao buscar o clima: {response.status_code} - {response.text}")
    
    # https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={API_KEY}
    # https://api.tomorrow.io/v4/weather/forecast?location=-3.2847,-60.1861&apikey=3Wp0bmAHHVNp7Pu6jUNr4woQAQ2nutFD&timesteps=1h
    # https://api.tomorrow.io/v4/weather/realtime?location=-3.2847,-60.1861&apikey=3Wp0bmAHHVNp7Pu6jUNr4woQAQ2nutFD
    
    """ 
    {
        "data": {
            "time": "2025-05-27T01:51:00Z",
            "values": {
                "cloudBase": 9.1,
                "cloudCeiling": 12.6,
                "cloudCover": 95,
                "dewPoint": 25.1,
                "freezingRainIntensity": 0,
                "humidity": 91,
                "precipitationProbability": 0,
                "pressureSeaLevel": 1013.32,
                "pressureSurfaceLevel": 1009.99,
                "rainIntensity": 0,
                "sleetIntensity": 0,
                "snowIntensity": 0,
                "temperature": 26.8,
                "temperatureApparent": 30.2,
                "uvHealthConcern": 0,
                "uvIndex": 0,
                "visibility": 16,
                "weatherCode": 1001,
                "windDirection": 217,
                "windGust": 0.9,
                "windSpeed": 0.2
            }
        },
        "location": {
            "lat": -3.2847,
            "lon": -60.1861
        }
    }
    """
    
    # print(weather_response)
    
    return weather_response

# alta precisão tw
# razoavel precisão ow
# duas precisão
def get_weather(city, api="all"):
    match api:
        case "ow":
            return {
                "open_weather": open_weather(city)
            }
        case "tw":
            return {
                "tommorow_weather": tommorow_weather(city)
            }
        case "all":
            return {
                "open_weather": open_weather(city),
                "tommorow_weather": tommorow_weather(city)
            }
    

def nlu_fallback(_): print("Comando irreconhecivel ou não exista")
def aumentar_vol(value): def_vol(value if value != None else 0.05, inc= not value)
def diminuir_vol(value): def_vol(value if value != None else -0.05, inc= not value)
def definir_vol(value): def_vol(value)
def max_vol(_): def_vol(100)
def mutar_vol(_): def_vol(0)
def get_time_now(_): get_time()
def ac_get_vol(_): get_vol()
def ac_get_weather(value): get_weather(value)


vol_actions = {
    "nlu_fallback": nlu_fallback,
    "aumentar_volume": aumentar_vol,
    "diminuir_volume": diminuir_vol,
    "definir_volume": definir_vol,
    "max_volume": max_vol,
    "mutar": mutar_vol,
    "time_now": get_time_now,
    "get_vol": ac_get_vol,
    "get_weather": None #ac_get_weather
}


def start():
    while True:
        message:str = str(input(">>>"))
        
        answer = {
            "text": message
        }

        response = requests.post(
            "http://127.0.0.1:5005/model/parse",
            json=answer
        )

        data = response.json();

        
        print(data)
        action:str  = data["intent"]["name"]
        value = data["entities"][0]["value"] if len(data["entities"]) else None
        
        # print(data)
        print("Ação: ", action) # nome intent
        print("Valor: ", value) # nome entities
        
        handler = vol_actions[action]
        
        if handler: 
            handler(value)
        else:
            print("Ação não reconhecida")


# start()

# def get_city_names():
#     url = "https://raw.githubusercontent.com/felipefdl/cidades-estados-brasil-json/master/Cidades.json"
#     response = requests.get(url)
#     # cidades = [cidade["nome"] for cidade in response.json()]
    
#     for c in response.json():
#         print(c)

# get_city_names()



