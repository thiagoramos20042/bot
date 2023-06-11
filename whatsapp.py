import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib

# Streamlit app title
st.markdown(
    '<h1 style="text-align: center;">WhatsApp Automation</h1>',
    unsafe_allow_html=True
)

# Image display
image_path = "THIAGO OLIVEIRA.png"

st.image(image_path, caption="Image Caption", use_column_width=True)

# CSV file upload
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Check if file is uploaded
if uploaded_file is not None:
    # Read the CSV file
    contatos_df = pd.read_csv(uploaded_file, thousands=',', decimal='.')
    
    # Webdriver initialization
    navegador = webdriver.Edge()
    navegador.get("https://web.whatsapp.com/")
    xpath_value = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p/span'
    wait = WebDriverWait(navegador, 10)
    
    # Wait until WhatsApp web is loaded
    while len(navegador.find_elements(By.ID, "side")) < 1:
        time.sleep(1)
    
    # Iterate through the contacts and send messages
    for i, mensagem in enumerate(contatos_df['mensagem']):
        pessoa = contatos_df.loc[i, "nome"]
        numero = contatos_df.loc[i, "numero_tel"]
        texto = urllib.parse.quote(f"Oi {pessoa}! {mensagem}")
        link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
        navegador.get(link)
        
        # Wait until chat is loaded
        while len(navegador.find_elements(By.ID, "side")) < 1:
            time.sleep(1)
        
        # Send the message
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_value))).send_keys(Keys.ENTER)
        time.sleep(10)
    
    # Close the webdriver
    navegador.quit()
st.markdown(
    '''
    ## Instruções de uso:
1. Crie 3 colunas no excel  ou google planilhas ( nome, numero_tel, mensagem) 
2. Baixe esse arquivo no formato csv
3. Insira essa planilha clicando no botâo browse files 
4. Siga o passo a passo da tela do seu computador 
    '''
)