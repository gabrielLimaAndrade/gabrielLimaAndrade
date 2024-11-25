from flask import Flask, jsonify
import pandas as pd 
app = Flask(__name__)

@app.route('/dados')

def site():  
    info = pd.read_csv('../1_Bases_Tratadas/MagazineTratada.csv')

    media_preco = info['Precos'].mean()
    media = {'Media dos precos dos celulares: R$': media_preco}
    
    mediana_preco = info['Precos'].median()
    mediana = {'mediana dos Precos dos celulares: R$': mediana_preco}
     
    dp_preco = info ['Precos'].std()
    dp = {'Desvio padrao dos precos: R$': dp_preco}
    
    resposta = {'media': media_preco, 'mediana': mediana_preco, 'Desviopadrao': dp_preco}
    return jsonify(resposta)
@app.route('/valores')

def marca():
    info = pd.read_csv('../1_Bases_Tratadas/MagazineTratada.csv')
    produtos_acima_4k = info[info['Precos'] > 4000]
    quatro = {'Produtos 4k': produtos_acima_4k}
    produtos_entre_1k_3k = info[(info['Precos'] >= 1000) & (info['Precos'] <= 3000)]
    produtos_ate_1k = info[info['Precos'] < 1000]
    produtos = {'4k':produtos_acima_4k.to_dict(orient='records'), '3k': produtos_entre_1k_3k.to_dict(orient='records'),
                 '1k': produtos_ate_1k.to_dict(orient='records') }
    produtos3 = {'produtos': pd.concat([produtos_acima_4k, produtos_entre_1k_3k, produtos_ate_1k], ignore_index=True).to_dict(orient='records')}
    return jsonify(produtos3)
@app.route('/dados_brutos')

def bruto():  
    info = pd.read_csv('../1_Bases_Tratadas/MagazineTratada.csv')
    brutos = {'Dados Brutos': info.to_dict(orient='records')}
    return jsonify(brutos)
@app.route('/precos')
def pre():
    info = pd.read_csv('../1_Bases_Tratadas/MagazineTratada.csv')
    marca = info['marca'].tolist()
    modelos = info['modelo'].tolist()
    preco = info['Precos'].tolist()
    aparelho = info['aparelho'].tolist()
    prec = {"Preco":preco,"Marca":marca,"Modelo":modelos,"aparelho":aparelho}
    return jsonify(prec)
@app.route('/marcas')
def marcas():
    info = pd.read_csv('../1_Bases_Tratadas/MagazineTratada.csv')
    sam = info[info['marca'] == 'Samsung'].shape[0]
    apple = info[info['marca']=='iPhone'].shape[0]
    moto = info[info['marca']=='Motorola'].shape[0]
    marc = {'Apple':apple, 'Samsung': sam, 'Motorola':moto}
    return jsonify(marc)
@app.route('/dinheiro')
def di():
    info = pd.read_csv('../1_Bases_Tratadas/MagazineTratada.csv')
    quatro = info[info['Precos'] >=4000].shape[0]
    tres = info[info['Precos']>=3000].shape[0]
    dois = info[info['Precos']>=2000].shape[0]
    um  = info[info['Precos']>=1000].shape[0]
    menos = info[info['Precos']<1000].shape[0]
    din = {'4k':quatro,'3k':tres,'2K':dois,'1k':um,'menos':menos}
    return jsonify(din)
app.run(debug = True)
