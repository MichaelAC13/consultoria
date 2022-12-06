from datetime import datetime
import re
import pandas as pd
from conection import connection
import mysql.connector
import jwt

def connectmysql():
  mydb = mysql.connector.connect(
            host="database-consultoria.ccxoiodaf5ni.us-east-1.rds.amazonaws.com",
            user="admin",
            password="12345678",
            database="consultoria",
            charset="utf8",
            # connect_timeout=28800,
            buffered=True,
            port=3306
        )
  return mydb
        
class interactions():
  def criarmercadorias():
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    try:
      mycursor.execute(connection.createmercadorias())
    except:
      mycursor.execute(connection.createmercadorias(),multi=True)
    return {"message":"criarmercadorias Iniciado"}
   
  def criarusers():
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    try:
      mycursor.execute(connection.createusers())
    except:
      mycursor.execute(connection.createusers(),multi=True)
    mycursor.execute('ALTER TABLE `consulctoria`.`users` CHARACTER SET = utf8 ;')
    return {"message":"users Iniciado"}
  
  def criarfornecedores():
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    try:
      mycursor.execute(connection.createfornecedores())
    except:
      mycursor.execute(connection.createfornecedores(),multi=True)
    mycursor.execute('ALTER TABLE `consulctoria`.`fornecedores` CHARACTER SET = utf8 ;')
    return {"message":"users Iniciado"}

  def Incluirdadosmercadorias():
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    df = pd.read_csv("bases//a2.csv", delimiter="|", encoding='utf-8', dtype='string').drop(columns=['cnpjDest','nomeDest','qCom','vUnCom','situacao']).reset_index()
    df['nomeEmitente'] = df['cnpjEmitente']
    df = df.groupby(["NCM"])['nomeEmitente'].apply(list).reset_index()

    def droplist(nomes):
        df = []
        for list in nomes:
            uniques = []
            for i in list:
                if i not in uniques:
                    uniques.append(str(i))
            df.append(uniques)
        return df

    df['nomeEmitente'] = droplist(df['nomeEmitente'])
    df1 = pd.read_csv("bases//Base.txt", delimiter='|', encoding="utf-8", low_memory=False)

    def setncm(ncm):
        a = []
        for i in ncm:
            list =  df.loc[df['NCM'].astype(str) == str(i)]
            list = list['nomeEmitente'].tolist()
            try:
                a.append(list[0])
            except:
                a.append([])
        return a

    df1['fornecedores'] = setncm(df1['ncm'])
    # print(df1.index.values)
    a = 0
    for i in range(0,int(df1.index.values[-1]/50000)+1):
        dfpart = df1[a:a+50001]
        a+=50000
        sql  = "INSERT INTO mercadorias (id, descricao, ncm, pisecofins, setor, icms, status, dtupdate, fornecedores) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in dfpart.values:
          val = ("0",  str(i[0]), str(i[1]), str(i[3]), str(i[5]), str(i[2]), str(i[4]), str(i[6]), str(i[7]))
          # print(val)
          mycursor.execute(sql, val)
          mydb.commit()
    print('pronto')

  def Incluirdadosusers(user):
    mydb  = ''
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    user = {"email":user['email'], "password":user['password'], "hashcode":"", "name":user['name'], "status":0, "master":1 , "dtupdate":datetime.now() }
    payload = {}
    payload['password'] = user['password']
    key= '1234'
    encoded_jwt = jwt.encode(payload=payload, key=key, algorithm="HS256")
    user['hashcode'] = encoded_jwt
    sql = "INSERT INTO consultoria.users (id, email, hashcode, name, status, master, dtupdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = ('0', user['email'], user['hashcode'], user['name'], user['status'], user['master'], user['dtupdate'])
    try:
      mycursor.execute(sql, val)
      mydb.commit()
    except:
      pass
    return user
  
  def Incluirdadosfornecedores():
    mydb  = ''
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    df = pd.read_csv("bases//fornecedoresmercadorias.txt", delimiter="|", encoding='utf-8', dtype='string')
    sql = "INSERT INTO consultoria.fornecedor (id, fornecedor, atacado, cnpj, ie, estado, cidade, logradouro, numero, bairro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for d in df.values:
      val = ('0', d[0], d[1], d[2], d[3], d[5], d[6], d[7], d[8], d[9])
      try:
        mycursor.execute(sql, val)
        mydb.commit()
      except:
        pass
    return d

  def authenticate(user):
    mydb  = ''
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM users WHERE email ='{user['email']}'"
    try:
      mycursor.execute(sql)
      a = mycursor.fetchall()
      token = jwt.decode(a[0][2], algorithms='HS256', verify=True, key='1234')
      if token['password'] == user['password']:
        chave = str(a[0][2]).split('.')[2] 
        return {"message": "Usuário Logado" , "token": chave }
    except Exception as e:
      return {"message": e}

  def contarpaginas():
      mydb  = connectmysql()
      mycursor = mydb.cursor()
      def selection():
        sql = "SELECT MAX(mercadorias.id) FROM consultoria.mercadorias"
        mycursor.execute(sql)
        a = mycursor.fetchall()
        return a
      while (not mydb.is_connected):
        print(mycursor)      
      else:
        try:
            a = selection()
        except:
            mydb.cursor() 
            a= 7000
      return {"pages": round(a[0][0]/1000)}

  def selecionarpaginas(limit, page):
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    def selection():
      sql = f"SELECT * FROM mercadorias WHERE id LIMIT {limit} OFFSET {(page-1)*limit}"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      df = pd.DataFrame()
      for x in myresult:
        val ={"id":f"{x[0]}","descricao":f"{x[1]}","ncm":f"{x[2]}","pisecofins":f"{x[3]}","icms":f"{x[5]}","setor":f"{x[4]}","status":f"{x[6]}","data":f"{x[7]}","fornecedores":f"{x[8]}"}
        df1 = pd.DataFrame(val,index=[0])
        df = pd.concat([df,df1])
      df = str(df.to_json(orient="records", force_ascii=False))
      return df
    while (not mydb.is_connected):
      mycursor = mydb.cursor()
      # print(mycursor)
    else:
      try:
        df = selection()
      except:
        df= ''
        df = selection()
    return df
    
  def downloads(paginaatual):
    path = 'downloads/paginaatual.xlsx'
    df = pd.DataFrame(paginaatual).to_excel(path)
    return path

  def filtraropcoes(options):
    # print(options)
    mydb  = connectmysql()
    mycursor = mydb.cursor()

    def selectionpisecofins():
      option = re.sub('[^0-9]', '', options['pisecofins'])
      sql = f"SELECT * FROM mercadorias WHERE pisecofins LIKE '%{option}%' LIMIT 1000"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      df = pd.DataFrame([{"id":f"{x[0]}","descricao":f"{x[1]}","ncm":f"{x[2]}","pisecofins":f"{x[3]}","icms":f"{x[5]}","setor":f"{x[4]}","status":f"{x[6]}","data":f"{x[7]}","fornecedores":f"{x[8]}"} for x in myresult])
      # df= df.loc[options['pisecofins'] in df['pisecofins']]
      df = str(df.to_json(orient="records", force_ascii=False))
      return df

    def selectionicms():
      # option = re.sub('[^0-9]', '', options['icms'])
      sql = f"SELECT * FROM mercadorias WHERE icms LIKE '%{options['icms']}%' LIMIT 1000"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      df = pd.DataFrame([{"id":f"{x[0]}","descricao":f"{x[1]}","ncm":f"{x[2]}","pisecofins":f"{x[3]}","icms":f"{x[5]}","setor":f"{x[4]}","status":f"{x[6]}","data":f"{x[7]}","fornecedores":f"{x[8]}"} for x in myresult]).to_json(orient="records", force_ascii=False)
      return df

    def selectionsetor():
      sql = f"SELECT * FROM mercadorias WHERE setor LIKE '%{options['setor']}%' LIMIT 20000"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      df = pd.DataFrame([{"id":f"{x[0]}","descricao":f"{x[1]}","ncm":f"{x[2]}","pisecofins":f"{x[3]}","icms":f"{x[5]}","setor":f"{x[4]}","status":f"{x[6]}","data":f"{x[7]}","fornecedores":f"{x[8]}" } for x in myresult]).to_json(orient="records", force_ascii=False)
      return df
    
    if options['pisecofins'] != "Todos":
      df = selectionpisecofins()

    if options['icms'] != "Todos":
      df = selectionicms()

    if options['setor'] != "Todos":
      df = selectionsetor()
    return df

  def searchone(search):
    mydb  = connectmysql()
    mycursor = mydb.cursor()

    def searchonesql():
      sql = f"SELECT * FROM mercadorias WHERE descricao LIKE '%{search['search']}%'"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      df = pd.DataFrame([{"id":f"{x[0]}","descricao":f"{x[1]}","ncm":f"{x[2]}","pisecofins":f"{x[3]}","icms":f"{x[5]}","setor":f"{x[4]}","status":f"{x[6]}","data":f"{x[7]}","fornecedores":f"{x[8]}"} for x in myresult])
      df = str(df.to_json(orient="records", force_ascii=False))
      return df
    df = searchonesql()
    return df

  def getfornecedores(fornecedores):
    mydb  = connectmysql()
    mycursor = mydb.cursor()
    df = pd.DataFrame()
    for x in fornecedores['fornecedores'][1:-1].split(','):
      x = x.replace("'","").replace(" ","")
      sql = f"SELECT * FROM fornecedor WHERE cnpj = '{x}'"
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      df1 = pd.DataFrame([{"id":f"{x[0]}","cnpj":f"{x[1]}","fornecedor":f"{x[2]}", "atacado":f"{x[3]}", "ie":f"{x[4]}", "estado":f"{x[5]}", "logradouro":f"{x[7]}", "cidade":f"{x[6]}","numero":f"{x[8]}", "bairro":f"{x[9]}" } for x in myresult])
      df = pd.concat([df,df1])
    df = str(df.to_json(orient="records", force_ascii=False))
    return df

  # criarmercadorias()
  # Incluirdados()
  # criarfornecedores()
  # Incluirdadosfornecedores()
  # Incluirdadosmercadorias()