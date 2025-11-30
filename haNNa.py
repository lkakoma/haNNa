from flask import Flask, request, render_template, redirect, url_for
import requests
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')

app = Flask(__name__)
dados_do_jogador_pesquisado = {}

class PesquisoPlayer:
    def __init__(self, tag):
        self.tag = tag

    def porcura_jogador(self):
        url = f"https://api.clashroyale.com/v1/players/%23{self.tag}"
        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }

        response = requests.get(url, headers=headers)
        return response.json()

@app.route('/', methods=['GET', 'POST'])
def root():
    global dados_do_jogador_pesquisado

    if request.method == "POST":
        tag = request.form["TAG-PLAYER"].replace("#", "").upper()
        print(tag)
        dados_do_player = PesquisoPlayer(tag).porcura_jogador()
        dados_do_jogador_pesquisado = dados_do_player
        print(f'{dados_do_player} enviados')   
        return redirect(url_for('dados'))    
    return render_template('index.html')

@app.route('/dados', methods = ['GET', 'POST'])
def dados():
    if request.method == 'POST':
        
        tag = request.form["TAG-PLAYER"].replace("#", "")
        dadosColetados = PesquisoPlayer(tag)
        Respostas = dadosColetados.porcura_jogador()

        nome = Respostas.get('name')
        nivel = Respostas.get('expLevel')
        trofeus = Respostas.get('trophies')
        nome_clan = Respostas.get('clan', {}).get('name', 'Sem clã')

    return render_template( 'dados.html', nome=dados_do_jogador_pesquisado.get('name'), nivel=dados_do_jogador_pesquisado.get('expLevel'),
trofeus=dados_do_jogador_pesquisado.get('trophies'), nome_clan=dados_do_jogador_pesquisado.get('clan', {}).get('name'))
    return render_template('dados.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=3139)


