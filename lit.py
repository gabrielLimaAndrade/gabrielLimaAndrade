import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine 
st.title('Trabalho Web: Celulares Magazine') 

#requisicao1 = requests.get("http://localhost:5000/dados")
#requisicao2 = requests.get("http://127.0.0.1:5000/dados_brutos")
#requisicao3 = requests.get("http://127.0.0.1:5000/precos")
#requisicao4 = requests.get("http://127.0.0.1:5000/marcas")
#requisicao5 = requests.get("http://127.0.0.1:5000/dinheiro")
st.button('Tela inicial',type='primary')
if st.button("Graficos univariados"):
   
   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   resposta = pd.DataFrame(df_lido)
   media = resposta['Precos'].mean()
   mediana = resposta['Precos'].median()
   dp = resposta['Precos'].std()
   st.write(resposta)
   plt.figure(figsize=(10,6))
   sns.boxplot(data=resposta,x='Precos')
   plt.title('Boxplot dos Preços')
   plt.xlabel('Preço')
   st.pyplot(plt.gcf())
   q1 = resposta['Precos'].quantile(0.25)
   q3 = resposta['Precos'].quantile(0.75)
   i = q3 - q1 
   baixo = q1 - 1.5 * i 
   alto = q3 + 1.5 * i 
   outliers = resposta[(resposta['Precos'] < baixo) | (resposta['Precos'] > alto)]
   st.write('Este e um grafico boxplot com os preços dos celulares da magazine')
   st.write('Media de preço:',media)
   st.write('Mediana de preço:',mediana)
   st.write('Desvio Padrão de preço:',dp)
   if outliers.empty:
      st.write('Sem Outliers')
   else:
      st.write('Outliers:',outliers)

   st.write('Histograma dos Preços')
   plt.figure(figsize=(10,6))
   plt.hist(resposta['Precos'],bins=20, color='red',edgecolor='black')
   plt.title('Distribuição dos preços')
   plt.xlabel('Preço')
   plt.ylabel('Frequencia')
   st.pyplot(plt.gcf())
   moda = resposta['Precos'].mode().iloc[0]
   menosfrequente = resposta['Precos'].value_counts().idxmin()
   st.write('Este e um Histograma dos Preços dos celulares e frequencia que eles aparecem')
   st.write('Valor mais frequente', moda)
   st.write('Valor menos frequente',menosfrequente)


   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   sam = df_lido[df_lido['marca'] == 'Samsung'].shape[0]
   apple = df_lido[df_lido['marca']=='iPhone'].shape[0]
   moto = df_lido[df_lido['marca']=='Motorola'].shape[0]
   marc = {'Apple':apple, 'Samsung': sam, 'Motorola':moto}
   total = apple + sam + moto
   df = pd.DataFrame(list(marc.items()), columns =['Marca','Quantidade'])
   st.write(df)
   fig2 = px.pie(df,names='Marca', values='Quantidade', title='Quantidade de aparelhos por marca')
   st.plotly_chart(fig2)
   st.write('Este e um grafico em setores da quantidade de aparelhos por marca')
   st.write('Total de Aparelhos:',total)
   if apple > sam and apple > moto:
      st.write('A Marca mais presente: Apple')
   elif sam > apple and sam > moto:
      st.write('A Marca mais presente: Samsung')
   elif moto > apple and moto > sam:
      st.write('A Marca mais presente: Motorola')
   else:
      st.write('Não tem marca mais presente')
   
   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   quatro = df_lido[df_lido['Precos'] >=4000].shape[0]
   tres = df_lido[df_lido['Precos']>=3000].shape[0]
   dois = df_lido[df_lido['Precos']>=2000].shape[0]
   um  = df_lido[df_lido['Precos']>=1000].shape[0]
   menos = df_lido[df_lido['Precos']<1000].shape[0]
   din = {'4k':quatro,'3k':tres,'2K':dois,'1k':um,'menos':menos}
   v2 = pd.DataFrame(list(din.items()), columns=['Custo','Quantidade'])
   st.write(v2)
   fig3 = px.bar(v2, x='Custo',y = 'Quantidade', title = 'quantidade de celulares por preco')
   st.plotly_chart(fig3)
   st.write('Este grafico em barras mostra a quantidade de aparelhos por preço que vai de 0 a 4000 reais')
   if quatro > tres and quatro > dois and quatro > um and quatro > menos:
      st.write('A maioria dos preços são de 4000 para cima')
   elif tres >quatro  and tres > dois and tres > um and tres > menos:
      st.write('A maioria dos preços são de 3000 ate 3999')
   elif dois >quatro  and dois > tres and dois > um and dois > menos:
      st.write('A maioria dos preços são de 2000 ate 2999')
   elif um >quatro  and um > tres and um > dois and um > menos:
      st.write('A maioria dos preços são de 1000 ate 1999')
   elif menos >quatro  and menos > tres and menos > dois and menos > um:
      st.write('A maioria dos preços são de ate 999')

elif st.button("Graficos multivariados"):
   engine = create_engine('sqlite:///banco.db', echo=True)
   df_lido = pd.read_sql('SELECT * FROM dados', con=engine)
   resposta = pd.DataFrame(df_lido)
   f1 = px.bar(resposta, x = 'aparelho', y='Precos', title='Grafico de Preços por Aparelho', labels ={'aparelho'
   :'Modelo do Aparelho','Precos':'Preço (R$)'}, color='Precos', height=600)
   st.plotly_chart(f1)
   st.write('Este e um grafico de barras onde ele pega os valores conforme os aparelhos')
   maior=resposta['Precos'].max()
   menos=resposta['Precos'].min()
   aparelhomaiscaros = resposta[resposta['Precos'] == maior]['aparelho'].unique()
   aparelhomaisbaratos = resposta[resposta['Precos'] == menos]['aparelho'].unique()
   st.write(f"*Aparelho mais caro:* {', '.join(aparelhomaiscaros)} (R$ {maior:.2f})")
   st.write(f"*Aparelho mais barato:* {', '.join(aparelhomaisbaratos)} (R$ {menos:.2f})")
   


   f2 = px.bar(resposta, x = 'marca', y='Precos', title='Grafico de Preços por marca', labels ={'marca'
   :'marca','Precos':'Preço (R$)'}, color='Precos', height=600)
   st.plotly_chart(f2)
   st.write('Ja este e um grafico de barras onde ele pega os valores conforme as marca')
   marcamaiscaros = resposta[resposta['Precos'] == maior]['marca'].unique()
   marcamaisbaratos = resposta[resposta['Precos'] == menos]['marca'].unique()
   st.write(f"*Marca mais caro:* {', '.join(marcamaiscaros)} (R$ {maior:.2f})")
   st.write(f"*Marca mais barato:* {', '.join(marcamaisbaratos)} (R$ {menos:.2f})")

   f3 = px.bar(resposta, x = 'modelo', y='Precos', title='Grafico de Preços por modelo', labels ={'modelo'
   :'Modelo','Precos':'Preço (R$)'}, color='Precos', height=600)
   st.plotly_chart(f3)
   st.write('Ja este e um grafico de barras onde ele pega os valores conforme os modelos')
   modelomaiscaros = resposta[resposta['Precos'] == maior]['modelo'].unique()
   modelomaisbaratos = resposta[resposta['Precos'] == menos]['modelo'].unique()
   st.write(f"*Modelo mais caro:* {', '.join(modelomaiscaros)} (R$ {maior:.2f})")
   st.write(f"*Modelo mais barato:* {', '.join(modelomaisbaratos)} (R$ {menos:.2f})")
