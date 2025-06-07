from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from requests import RequestException

import datetime
import requests

""" 
try:
	print(a/b)

except ZeroDivisionError as error:
	print(error)

else:
	print( ' Sem erros')

finally:
	print('Aqui sempre vai printar')

"""

class Practical_tools:
    """ 
    Classe que contem ferramentas diversas para uso das IA's.
    
    Atributes:
        nome (str): Nome completo do usuário.
        email (str): Endereço de e-mail do usuário.
    """
    
    def __init__(self):
        self.__pc_volume = AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None).QueryInterface(IAudioEndpointVolume)
        self._pc_current_vol:float = self.__pc_volume.GetMasterVolumeLevelScalar()
        self.__k_open_weather:str = "17160d89448d96a62bbb0b1223f48bea"
        self.__k_tommorow_weather:str = "3Wp0bmAHHVNp7Pu6jUNr4woQAQ2nutFD"

    
    def pc_def_vol(self, value:str, inc:bool = False):
        
        value = float(value)
        """ 
            Define volume do Windows
        
            
            Args:
                value: Quantidade numerica para definir o volume
                inc: Se vai incrementar com o volume atual, ou definir volume exatamente com value
            
            Returns:
                bool: True
        """
        
        value = value/100
        
        set_vol = self._pc_current_vol + value if inc else value
        set_vol = max(0.0, min(set_vol, 1.0)) # Aceita valores entre 0 e 1
        
        
        print(f"Volume anterior: {self._pc_current_vol}")
        
        try: 
            self.__pc_volume.SetMasterVolumeLevelScalar(set_vol, None)
            self._pc_current_vol = set_vol
            
            print(f"Volume atual: {self._pc_current_vol}")
            
            self.pc_get_vol()
        except Exception as e:
            print(f"Erro ao aumentar o volume do computador: {e}")
        
    def pc_get_vol(self):        
        """ 
            Retorna o atributo pc_get_vol Windows
        """    
        print(f"Volume atual: {self._pc_current_vol}")
        return self._pc_current_vol
      
    def pc_get_time_now(self):  
        """ 
            Mostra a hora atual do dispositivo
        """
        
        full_datetime = datetime.datetime.now()
    
        hour = full_datetime.hour
        minute = full_datetime.minute
        second = full_datetime.second
        microsecond = full_datetime.microsecond
        
        print(f"São {hour}:{minute}:{second}")
        
    def api_open_weather(self, city: str):
        """ 
            API que mostra a previsão do tempo, com precisão razoavel porem confiavel
            
            Função mostra a previsão do tempo
        """
        
        weather_response = dict()
        
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
            "appid": self.__k_open_weather,
            "lang": "pt_br",
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params)
            response.raise_for_status()
            
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
            
            print(weather_response)
            return weather_response
            
        except RequestException as e:
            print(f"Erro {e}")
            return {}
        
        
        # if response.status_code == 200:
        # else:
        #     print(f"Erro ao buscar o clima: {response.status_code} - {response.text}")
            
        
        # print(weather_response)
            
    def api_tommorow_weather(self, city: str):
        """ 
            API que mostra a previsão do tempo, com alta precisão
            
            Função mostra a previsão do tempo
        """
        
        weather_response = {}
        result_op_w = self.api_open_weather(city)
        
        lat = result_op_w["cord"]["lat"]
        lon = result_op_w["cord"]["lon"]
        
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={self.__k_tommorow_weather}"
        
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
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

            
            return weather_response
        except RequestException as e:
            print(f"Error: {e}")
            return {}
        
        
        # print(response.json())
        
        # if response.status_code == 200:
        # else:
        #     print(f"Erro ao buscar o clima: {response.status_code} - {response.text}")
        
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
         
    
         
         
         
         
         
         
            
        
        
        
        
        