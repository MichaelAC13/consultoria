
import pandas as pd
import json
# df = pd.read_csv("Base.txt", delimiter='|', encoding="utf-8", low_memory=False)
# # df = pd.DataFrame(base)
# df.to_json('b.json', orient='records', force_ascii=False)
# # print(str(df['descricao']).split())
df = pd.read_csv("bases//a1.csv", delimiter="|", encoding='utf-8', dtype='string').drop(columns=['cnpjDest','nomeDest','qCom','vUnCom','situacao']).reset_index()
# base = pd.read_json(r'bases//Novo Documento de Texto.json', lines=True, orient='records', encoding='utf-8')

# datafile =  str(open('bases//Novabasecomfornecedores0.json',encoding='utf8').read())

# data = json.loads(datafile)

# print(data)