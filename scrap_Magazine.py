import time
import random
import gspread
import pyautogui
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from oauth2client.service_account import ServiceAccountCredentials


login="" #coloque o seu login
senha="" #coloque a sua senha 


scope = ['', ''] #coloque os dado aqui
creds = ServiceAccountCredentials.from_json_keyfile_name('', scope) #coloque os dados de forma adequada
client = gspread.authorize(creds)

# Abrir a planilha do Google Sheets
sheet = client.open('').sheet1 #coloque os dados aqui
sheet.clear()

Numero_random = random.randint(5, 10)
msg=f"({Numero_random}% de desconto)"
urls = []
desconto = []
images = [] 
precos = [] 
titulo = [] 
desconto_real = [] 

options = Options()
#options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

url_magazine = 'https://www.magazinevoce.com.br/login/'

driver.get(url_magazine)

#efeutando o login
login_element=driver.find_element(By.XPATH,"//*[@id='email']")
login_element.click()
pyautogui.typewrite(login)

senha_element=driver.find_element(By.XPATH,"//*[@id='password']")
senha_element.click()
pyautogui.typewrite(senha)
#--------------------------------------------------------------------------


#clikando no botão de login
entrar_btn_element=driver.find_element(By.XPATH,"//button[@class='btn btn-primary']")
entrar_btn_element.click()
#--------------------------------------------------------------------------

time.sleep(3)
#entrando na minha loja e procurando a tag ofertas do dia
minhaLoja_btn_element=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[2]/a[2]")
minhaLoja_btn_element.click()


input("digite qualquer tecla para continuar ...")

container_pais = driver.find_elements(By.XPATH, "//ul[@class='sc-fjvvzt ehuxpX sc-ERObt hywYGY sc-APcvf cHnkDp']")

for container_pai in container_pais:

    nome_elements = container_pai.find_elements(By.XPATH, "//h2[@class='sc-gZfzYS dGFAGZ']")
    for titulo_element in nome_elements:
        titulo.append(titulo_element.text)
    print(titulo)

    precoDesconto_elements = container_pai.find_elements(By.XPATH, "//p[@class='sc-jXbUNg fXGDSl sc-gEkIjz iXukPA']")
    for preco_desconto in precoDesconto_elements:
        precos.append(preco_desconto.text)
    print(precos)


    img_elements = container_pai.find_elements(By.XPATH, "//img[@class='sc-dtInlm bpdQmX']")
    for imagem_element in img_elements:
        images.append(imagem_element.get_attribute('src'))
    print(images)



link_produtos = []
links_afiliado = []

for container_pai in container_pais:
    link_produto_elements = container_pai.find_elements(By.XPATH, ".//a[@class='sc-kOPcWz dSFUBN sc-AHTeh jHPdWz sc-AHTeh jHPdWz']")
    for link_produto_element in link_produto_elements:
        link_produtos.append(link_produto_element.get_attribute("href"))
print("Links brutos coletados:")

for i, link_produto in enumerate(link_produtos):
    driver.get(link_produto)
    sleep(1)

    #btn_link_curto_element = driver.find_element(By.XPATH,"//input[@class='sc-kdBSHD kWiCZR']")
    #btn_link_curto_element.click()

    try:
        desconto_elements =driver.find_element(By.XPATH,"//span[@class='sc-hYmls fnoFMk']")
        desconto.append(desconto_elements.text)
    except Exception as e:
        desconto.append(msg)
    try:
        desconto_real_element=driver.find_element(By.XPATH,"//p[@class='sc-jXbUNg gDZNmk sc-bOQTJJ hqBGTQ']")
        desconto_real.append(desconto_real_element.text)
    except Exception as e:
        desconto_real.append("nullo")

    link_afiliado_elements = driver.find_elements(By.XPATH, "//input[@class='sc-jnOGJG fyfAwh sc-kWtpeL ehXIRz']")
    for link_afiliado_element in link_afiliado_elements:
        urls.append(link_afiliado_element.get_attribute("value"))


print("Links afiliados coletados:")
for i, link_afiliado in enumerate(urls):
    print(f"Link afiliado {i + 1}: {link_afiliado}")



print(f"Tamanho da lista 'titulo': {len(titulo)}")
print(f"Tamanho da lista 'images': {len(images)}")
print(f"Tamanho da lista 'desconto': {len(desconto)}")
print(f"Tamanho da lista 'precos': {len(precos)}")
print(f"Tamanho da lista 'urls': {len(urls)}")
print(f"Tamanho da lista 'desconto_real': {len(desconto_real)}")



if len(titulo) == len(images)  == len(precos) == len(urls) == len(desconto_real):
    data = {
        'Product': titulo,
        'Image URL': images,
        'url': urls,
        'Discount': desconto,
        'Price': precos,
        'Desconto Real': desconto_real,
    }

    df = pd.DataFrame(data)

    try:
        header = df.columns.values.tolist()
        sheet.insert_rows([header], 1)

        # Adicionar os valores
        values = df.values.tolist()
        sheet.insert_rows(values, 2)

        print("Dados Enviados com Sucesso!")
    except Exception as e:
        print(f"Erro no Envio de Dados: {e}")
else:
    print("As listas têm tamanhos diferentes. Corrija isso antes de criar o DataFrame.")













