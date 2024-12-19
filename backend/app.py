from flask import Flask, jsonify, request
from flask_cors import CORS

from utilidades import isSolvable
from definicoes import Tabuleiro
import numpy as np
from algotimos_busca import exec_algoritmos

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route("/executar_algoritmos", methods=["POST"])
def executar_algoritmos():
    data = request.get_json()
    
    casas = np.array(data["tabuleiro"])

    if not isSolvable(casas):
        return jsonify({"message": "Tabuleiro inválido!"}), 400
    
    tabuleiro = Tabuleiro(casas=casas)
    
    resultado = exec_algoritmos(tabuleiro)

    return jsonify(resultado)

@app.route("/gerar_tabuleiro", methods=["GET"])
def gerar_tabuleiro():
    tabuleiro = Tabuleiro(generate=True)
    return jsonify({"tabuleiro": tabuleiro.serialize()})

if __name__ == "__main__":
    app.run(debug=True)