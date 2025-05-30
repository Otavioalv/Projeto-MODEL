from tools.practial_tools import Practical_tools
import requests

practical_tools = Practical_tools()

def nlu_fallback(_): print("Comando irreconhecivel ou não exista")
def aumentar_vol(value): practical_tools.pc_def_vol(value if value != None else 0.05, inc= not value)
def diminuir_vol(value): practical_tools.pc_def_vol(value if value != None else -0.05, inc= not value)
def definir_vol(value): practical_tools.pc_def_vol(value)
def max_vol(_): practical_tools.pc_def_vol(100)
def mutar_vol(_): practical_tools.pc_def_vol(0)
def get_vol(_): practical_tools.pc_get_vol()
def get_time_now(_): practical_tools.pc_get_time_now()
def get_weather(city): practical_tools.api_open_weather(city)



actions = {
    "nlu_fallback": nlu_fallback,
    "pc_aumentar_volume": aumentar_vol,
    "pc_diminuir_volume": diminuir_vol,
    "pc_definir_volume": definir_vol,
    "pc_max_volume": max_vol,
    "pc_mutar": mutar_vol,
    "pc_get_vol": get_vol,
    "time_now": get_time_now,
    "api_get_weather": get_weather
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

        
        # print(data)
        action:str  = data["intent"]["name"]
        value = data["entities"][0]["value"] if len(data["entities"]) else None
        
        # print(data)
        print("Ação: ", action) # nome intent
        print("Valor: ", value) # nome entities
        
        # handler = actions[action]
        
        # if handler: 
        #     handler(value)
        # else:
        #     print("Ação não reconhecida")

start()

""" 
python -m spacy download pt_core_news_md


pipeline:
  - name: SpacyNLP
    model: pt_core_news_md
  - name: SpacyTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  ...

"""


