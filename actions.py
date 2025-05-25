import requests 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


# volume
def aumentar_vol(value): def_vol(value if value >= 0 else 0.05, inc= value < 0)
def diminuir_vol(value): def_vol(value if value >= 0 else -0.05, inc= value < 0)
def definir_vol(value): def_vol(value)
def mutar_vol(_): def_vol(0)


vol_actions = {
    "aumentar_volume": aumentar_vol,
    "diminuir_volume": diminuir_vol,
    "definir_volume": definir_vol,
    "mutar": mutar_vol
}


def def_vol(value:float, inc:bool = False):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetMasterVolumeLevelScalar()
    
    print(f"Current volume: {current_volume}")
    
    # se value for menor q 0, -10
    set_vol = (value / 100) if (value / 100) <= 1 else 1
    if inc:
        set_vol = current_volume + value  
    if set_vol > 1:
        set_vol = 1
    elif set_vol < 0:
        set_vol = 0
        
        
    print("SET VOL: ", set_vol)
    volume.SetMasterVolumeLevelScalar(set_vol, None)




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
    
    print(data)
    print("ação: ", action) # nome intent
    print("valor: ", value) # nome entities
    
    handler = vol_actions[action]
    
    if handler: 
        handler(value)
    else:
        print("Ação não reconhecida")
    
    # match action:
    #     case "aumentar_volume":
    #         def_vol(value, value <= 0)
    #     case"diminuir_volume":
    #         def_vol(value, value <= 0)
    #     case "definir_volume":
    #         def_vol(value, value <= 0)
    #     case "mutar":
    #         def_vol(0)
    
    # if action == "aumentar_volume":
    #     if value >= 0:
    #         def_vol(value)
    #     else:
    #         def_vol(0.05, True)
    # elif action == "diminuir_volume":
    #     if value >= 0:
    #         def_vol(value)
    #     else:
    #         def_vol(-0.05, True)
    # elif action == "definir_volume":
    #     def_vol(value)
    # elif action == "mutar":
    #     def_vol(0)
    
    
    """ 
        nlu_fallback
        se der fallback, mandar ele realizar a pergunta novamente
        aumenta o 
        
        
        aumenta o volume pra -12
    """
    
    
    # intent name
    # entities value



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

