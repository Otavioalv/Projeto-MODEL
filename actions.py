import requests 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import datetime


def def_vol(value:float, inc:bool = False):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_vol = volume.GetMasterVolumeLevelScalar()
    
    
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
    
def nlu_fallback(_): print("Comando irreconhecivel ou não exista")
def aumentar_vol(value): def_vol(value if value >= 0 else 0.05, inc= value < 0)
def diminuir_vol(value): def_vol(value if value >= 0 else -0.05, inc= value < 0)
def definir_vol(value): def_vol(value)
def max_vol(_): def_vol(100)
def mutar_vol(_): def_vol(0)
def get_time_now(_): get_time()
def ac_get_vol(_): get_vol()


vol_actions = {
    "nlu_fallback": nlu_fallback,
    "aumentar_volume": aumentar_vol,
    "diminuir_volume": diminuir_vol,
    "definir_volume": definir_vol,
    "max_volume": max_vol,
    "mutar": mutar_vol,
    "time_now": get_time_now,
    "get_vol": ac_get_vol
}


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

    
    action:str  = data["intent"]["name"]
    value:float = float(data["entities"][0]["value"]) if len(data["entities"]) else -1
    
    # print(data)
    print("Ação: ", action) # nome intent
    print("Valor: ", value) # nome entities
    
    handler = vol_actions[action]
    
    if handler: 
        handler(value)
    else:
        print("Ação não reconhecida")



    """ 
    {
        'text': 'almenta o som em 30', 
        'intent': {
            'name': 'aumentar_volume', 
            'confidence': 0.9999929666519165
        }, 
        'entities': [
            {
                'entity': 'value', 
                'start': 17, 
                'end': 19, 
                'confidence_entity': 0.9999445676803589, 
                'value': '30', 
                'extractor': 'DIETClassifier', 
                'processors': [ 'EntitySynonymMapper']
            }
        ], 
        'text_tokens': [[0, 7], [8, 9], [10, 13], [14, 16], [17, 19]], 
        'intent_ranking': [
            {
                'name': 'aumentar_volume', 
                'confidence': 0.9999929666519165}, 
                {
                    'name': 'definir_volume', 
                    'confidence': 6.442897756642196e-06
                }, 
                {
                    'name': 'diminuir_volume', 
                    'confidence': 5.449787749967072e-07
                }, 
                {
                    'name': 'mutar', 
                    'confidence': 1.4307222961917887e-08
                }
        ], 
        'response_selector': {
            'all_retrieval_intents': [], 
            'default': {
                'response': {
                    'responses': None, 
                    'confidence': 0.0, 
                    'intent_response_key': None, 
                    'utter_action': 'utter_None'
                }, 
                'ranking': []
                }
            }
    }
    """

