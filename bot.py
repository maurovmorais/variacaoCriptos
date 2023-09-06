from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyodbc import Error
import sql
import time
from datetime import date, datetime
import conecta

# Inicio Execução
started = datetime.now()
print("Inicio Execução: ",started)

# Data Sistema
data = str(date.today())

# Criar objeto Navegador
navegador = webdriver.Chrome()

# Declarar variaveis
cotacao_bitcoin = ''
cotacao_ethereum = ''
Litecoin = ''
Cardano = ''
Binance_Coin = ''
lista = []

#Lista de criptos
criptos = ['cotacao_bitcoin','cotacao ethereum','Litecoin','Cardano','Binance_Coin']

for i,moedas in enumerate(criptos):
    def cripto(navegador_cripto):
        navegador.get(navegador_cripto)
        # Fazer a Pesquisa Cripto
        navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea').send_keys(moedas)
        navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea').send_keys(Keys.ENTER)
        # Pegar o valor da cotação do dolar
        variacao=navegador.find_element('xpath','//*[@id="crypto-updatable_2"]/div[3]/div[5]/div[2]/input').get_attribute('value')
        return variacao
    # Chama as funções
    variacao = cripto('https://google.com.br')
    print(moedas,'R$ ',variacao)

    # Apende de valores na lista
    lista.append(variacao)


# Inserir dados na Tabela do Banco de Dados
vcon=conecta.ConexaoBanco()

# Query
vsql  = f"""insert into criptos(data,bitcoin,ether,litecoin,cardano,binance) 
    values('{data}','{lista[0]}','{lista[1]}','{lista[2]}','{lista[3]}','{lista[4]}')"""

def inserte(conexao,sql):  
    try: 
        cursor = conexao.cursor()
        cursor.execute(sql)
        conexao.commit()
        print("Dado inserido !!!")
    except Error as ex:
        print(f"Erro encontrado !!!!",ex)

inserte(vcon,vsql)

# Fechar Conexão
if True:
    vcon.close()
    print("Conexão fechada")

# # Fechar o Browser
navegador.quit()

# # Fim Execução
finished = datetime.now()
print("Fim Execução: ",finished)