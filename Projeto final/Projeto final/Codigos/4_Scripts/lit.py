import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sqlalchemy import create_engine 
st.title('Trabalho Web: Celulares Magazine')

#requisicao1 = requests.get("http://localhost:5000/dados")
#requisicao2 = requests.get("http://127.0.0.1:5000/dados_brutos")
#requisicao3 = requests.get("http://127.0.0.1:5000/precos")
#requisicao4 = requests.get("http://127.0.0.1:5000/marcas")
#requisicao5 = requests.get("http://127.0.0.1:5000/dinheiro")
st.button('Tela inicial',type='primary')
if st.button("Media, Mediana e Desvio Padrão"):
   #resposta = requisicao3.json()
   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   resposta = pd.DataFrame(df_lido)
   st.write(resposta.columns)
   media = resposta['Precos'].mean()
   mediana = resposta['Precos'].median()
   dp = resposta['Precos'].std()
   st.write(resposta)
   estatisticas = pd.DataFrame({'estatistica':['Media','Mediana','Desvio Padrão'],'valor':[media,mediana,dp]})
   fig = px.bar(estatisticas, x='estatistica',y = 'valor', title = 'Media, Mediana, Desvio Padrão',labels = {
    'valor':'Valores','estatistica':'Metricas'},text='valor')

   fig.update_traces(texttemplate='%{text:.2f}',textposition ='outside')
   
   st.plotly_chart(fig)

elif st.button("Quantidades de aparelhos por marca"):
   #r = requisicao4.json()
   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   sam = df_lido[df_lido['marca'] == 'Samsung'].shape[0]
   apple = df_lido[df_lido['marca']=='iPhone'].shape[0]
   moto = df_lido[df_lido['marca']=='Motorola'].shape[0]
   marc = {'Apple':apple, 'Samsung': sam, 'Motorola':moto}
   df = pd.DataFrame(list(marc.items()), columns =['Marca','Quantidade'])
   st.write(df.columns)
   st.write(df)
   fig2 = px.pie(df,names='Marca', values='Quantidade', title='Quantidade de aparelhos por marca')
   st.plotly_chart(fig2)

elif st.button('Valores'):
   #v = requisicao5.json()
   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   quatro = df_lido[df_lido['Precos'] >=4000].shape[0]
   tres = df_lido[df_lido['Precos']>=3000].shape[0]
   dois = df_lido[df_lido['Precos']>=2000].shape[0]
   um  = df_lido[df_lido['Precos']>=1000].shape[0]
   menos = df_lido[df_lido['Precos']<1000].shape[0]
   din = {'4k':quatro,'3k':tres,'2K':dois,'1k':um,'menos':menos}
   v2 = pd.DataFrame(list(din.items()), columns=['Custo','Quantidade'])
   st.write(v2.columns)
   st.write(v2)
   fig3 = px.bar(v2, x='Custo',y = 'Quantidade', title = 'quantidade de celulares por preco')

 
   st.plotly_chart(fig3)
