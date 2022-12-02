
from flask import Flask,request,jsonify, jsonify, send_file
from flask_cors import CORS, cross_origin
import json
from banco import interactions
import datetime

app = Flask(__name__) 
cors = CORS(app, resources={r"/": {"origins": "*.*"}})
version = '1'

# ROTAS
@app.route("/",  methods=['POST'])
@cross_origin()
def home():
    return jsonify({
        "api": "API FLASK",
        "version": "1"
    })

@app.route(f"/api/v{version}/mercadorias/criarmercadorias", methods=['POST'])
@cross_origin()
def criarmercadorias():
    res = interactions.criarmercadorias()
    return res

@app.route(f"/api/v{version}/mercadorias/iniciarbanco", methods=['POST'])
@cross_origin()
def iniciarbanco():
    res = interactions.Incluirdados()
    return {"message":"Banco Iniciado"}

@app.route(f"/api/v{version}/mercadorias/page", methods=['POST'])
@cross_origin()
def page():
    res = json.loads(request.get_data().decode())
    try:
        res = interactions.selecionarpaginas(int(res['limit']),int(res['page']))
    except:
        res = interactions.selecionarpaginas(int(res['limit']),int(res['page']))
        pass
    return str(res)

@app.route(f"/api/v{version}/mercadorias/menuselectoptions", methods=['POST'])
@cross_origin()

def menuselectoptions():
    options = json.loads(request.get_data())
    res = interactions.filtraropcoes(options)
    return res
    
@app.route(f"/api/v{version}/mercadorias/countpage", methods=['GET'])
@cross_origin()
def countpage():
    res = interactions.contarpaginas()
    print(res)
    return res

@app.route(f"/api/v{version}/mercadorias/searchone", methods=['POST'])
@cross_origin()
def searchone():
    search = json.loads(request.get_data())
    res = interactions.searchone(search)
    print(res)
    return res

@app.route(f"/api/v{version}/mercadorias/users", methods=['POST'])
@cross_origin()
def users():
    user = json.loads(request.get_data())
    res = interactions.Incluirdadosusers(user)
    return res

@app.route(f"/api/v{version}/mercadorias/authenticate", methods=['POST'])
@cross_origin()
def authenticate():
    user = json.loads(request.get_data())
    res = interactions.authenticate(user)
    return res

@app.route(f"/api/v{version}/mercadorias/downloads", methods=['POST'])
@cross_origin()
def downloads():
    res = json.loads(request.get_data())
    res = interactions.downloads(res)
    return  send_file(res, mimetype='application/zip')

@app.route(f"/api/v{version}/mercadorias/uploads", methods=['POST'])
@cross_origin()
def uploads():
    res = request.get_data()
    now = str(datetime.datetime.now()).replace(':',"").replace(' ',"")
    open(f"uploads/{now}paginatual.xlsx", "a").write(res)
    return res

@app.route(f"/api/v{version}/fornecedores", methods=['POST'])
@cross_origin()
def fornecedores():
    fornecedores = json.loads(request.get_data())
    res = interactions.getfornecedores(fornecedores)
    # print(res)
    return res

if __name__ == '__main__':
    app.run(debug=True, port=5001)