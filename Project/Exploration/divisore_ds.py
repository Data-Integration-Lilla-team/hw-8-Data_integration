#suddivisione dei dataset per nome.
#raggruppiamo i dataset della stessa sorgente
import pandas as pd
[Ieri 22:39] PAOLO DI SIMONE
with open("datasets.json", 'r', encoding='utf-8') as f:
    json_object = json.loads(f.read())
    f.close()
df = pd.read_json(json_object[i]["dataset"], encoding="utf-8")

