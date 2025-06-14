# Projeto-MODEL

## INTRODUÇÃO
- Inspiração no jarvis
- Resposta por voz ou texto
- Mexer em tudo no pc
- Entrada de texto ou por voz
- Abrir aplicações especificas
- Fechar aplicações especificas
- Pesquisar coisas e me mandar resposta
- Pesquisar na web
- Varias apis uteis internamente
- +- volume 
- desligar pc
- desligar sistema
- informar as horas
- Temperatura em cidade


## Ferramentas

* Python - Versão 3.10
* tkinter: Para a interface gráfica.
* pyttsx3: Para a síntese de voz.
* speech_recognition: Para o reconhecimento de voz.
* Google API (Gemini): Para buscas e respostas avançadas.
* (Mistral (Mixtral ou Mistral-7B) - atribuir trabalhos para ias especificas)
* Sistema robusto, previsível e treinável → Rasa NLU + saída em JSON.
* OpenWeather API/Tomorrow.io: Para previsão do tempo.

## Bibliotecas 
* os
* random
* time
* webbrowser
* threading.Thread
* datetime
* requests
* speech_recognition
* pyttsx3
* google.generativeai
* tkinter
* pycaw



## Funcionalidades
- [x] Almentar/Diminuir volume (inplementar com RASA)
- [X] Pedir a quantidade de volume
- [x] Informar as horas
- [ ] Pedir previsão do tempo aqui, ou em alguma cidade



## Comentarios

* "Usar **Python** na versa **3.10**"
* "Atualizar a variavel de ambiente **PYTHONIOENCODING** do **VENV** antes de instalar as dependencias com o seguinte codigo:"
```
$env:PYTHONIOENCODING="utf-8"
```

* Treinar RASA
```
rasa train
```

* Iniciar RASA (terminal)
```
rasa shell
```

* Iniciar RASA (servidor)
```
rasa run
```

* Iniciar API RASA
```
rasa run --enable-api
```

* Iniciar API RASA com configurações especificas
```
rasa run --enable-api --cors "*" --debug
```

* Mostra onde DIET erra no RASA
```
rasa test nlu --errors
```

* **--cors "*"**: Libera chamadas de qualquer origem
* **--debug**: log detalhado para debugar

* Possivel organização da intenção
```
<tipo>-<comando/ação>

volume-aumentar
volume-diminuir
volume-mudo
```

* Tomorrow.io (api weather)
```
curl --request GET --url 'https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466 apikey=3Wp0bmAHHVNp7Pu6jUNr4woQAQ2nutFD'
```

```
import requests

lat = -23.55052
lon = -46.633308
api_key = "SUA_API_KEY"

url = f"https://api.tomorrow.io/v4/weather/forecast?location={lat},{lon}&apikey={api_key}"

res = requests.get(url)
print(res.json())
```

* OpenWeather (api weather)
```
17160d89448d96a62bbb0b1223f48bea

def pegar_clima_por_cidade(cidade, api_key):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": cidade,
        "appid": api_key,
        "lang": "pt",
        "units": "metric"
    }

    resposta = requests.get(url, params=params)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        clima = dados["weather"][0]["description"]
        temp = dados["main"]["temp"]
        cidade_nome = dados["name"]
        return f"O clima em {cidade_nome} é '{clima}' com temperatura de {temp}°C"
    else:
        return f"Erro ao buscar o clima: {resposta.status_code} - {resposta.text}"

# Exemplo de uso:
api_key = "SUA_API_KEY_AQUI"
cidade = "São Paulo"
print(pegar_clima_por_cidade(cidade, api_key))

```

* Geocoding (pega latitude longitude pelo nome)
```
GET https://api.opencagedata.com/geocode/v1/json?q=São+Paulo&key=SUA_API_KEY

```

* IA que interpreta erros de codigo e transforma em respostas casuais

* Pesquisar por lat e lon no google maps

```
https://www.google.com/maps?q=-3.2847,-60.1861
``` 



<!-- 
sobre Perfeito. Então vamos montar o sistema com Rasa NLU + saída JSON, passo a passo, com foco em:

Intents como: aumentar_volume, diminuir_volume, mutar, definir_volume.

Saída em JSON, pronta pra ser lida por um script Python, Node, etc. da conversa aciama


- intent: mutar
  examples: |
    - mano, deixa no mínimo que tá muito alto
    - corta tudo aí, som tá insuportável
    - deixa sem som, tá explodindo aqui
    - silencia total, pelo amor
    - cala esse som aí, tá horrível
    - deixa mudo, tá gritando aqui
    - mano, muta isso logo
    - some com esse som
    - tira todo o som agora
    - por mim pode desligar o áudio todo
    - som tá um inferno, corta logo
    - tá estourando, silencia isso
    - pode cortar o som, tá péssimo
    - não quero ouvir mais nada, muta
    - silêncio completo, mano
    - volume zero urgente
    - deixa mudo que tá doendo o ouvido
    - desliga o volume inteiro agora
    - sem nenhum som, por favor
    - bota no silencioso total

 -->