from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET

# Constantes
URL = "https://www.saucedemo.com/"
CAMINHO_ARQUIVO_XML = r'C:\Users\carlo\OneDrive\Documentos1\automação xml\automação xml\informacoes_login.xml'
TIMEOUT = 10

def fazer_login(driver, username, password):
    """Realiza login no sistema."""
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def adicionar_ao_carrinho(driver, *produtos):
    """Adiciona produtos ao carrinho."""
    for produto in produtos:
        driver.find_element(By.XPATH, f"//*[text()='{produto}']/../../..//button").click()

def mapear_produtos(driver):
    """Mapeia e lista todos os produtos na página."""
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'inventory_item')))
    produtos = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    for produto in produtos:
        nome = produto.find_element(By.CLASS_NAME, 'inventory_item_name').text
        preco = produto.find_element(By.CLASS_NAME, 'inventory_item_price').text
        print(f'Produto: {nome}, Preço: {preco}')

def preencher_checkout(driver, first_name, last_name, postal_code):
    """Preenche as informações de checkout e continua."""
    driver.find_element(By.ID, "first-name").send_keys(first_name)
    driver.find_element(By.ID, "last-name").send_keys(last_name)
    driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    driver.find_element(By.ID, "continue").click()

def main():
    """Função principal para executar a automação."""
    driver = webdriver.Firefox()
    driver.get(URL)

    try:
        tree = ET.parse(CAMINHO_ARQUIVO_XML)
        root = tree.getroot()
        username = root.find('username').text
        password = root.find('password').text

        # Realizar o login
        fazer_login(driver, username, password)

        # Mapear e imprimir os produtos disponíveis
        mapear_produtos(driver)

        # Adicionar itens ao carrinho
        adicionar_ao_carrinho(driver, "Test.allTheThings() T-Shirt (Red)", "Sauce Labs Bolt T-Shirt", "Sauce Labs Bike Light")

        # Visualizar carrinho / Finalizar
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.ID, "checkout").click()

        # Aguardar a página de checkout carregar
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "checkout_info_container")))
        
        # Preencher as informações de checkout e continuar
        preencher_checkout(driver, "David", "Junio", "781234")

        # Aguardar a página de resumo do pedido carregar
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "checkout_summary_container")))

        # Obter o valor total e imprimir
        total_value = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        print("Valor total:", total_value)

    except FileNotFoundError:
        print(f"O arquivo XML não foi encontrado no caminho: {CAMINHO_ARQUIVO_XML}")
    except ET.ParseError:
        print("Erro ao analisar o arquivo XML.")
    except PermissionError:
        print(f"Permissão negada ao tentar acessar o arquivo: {CAMINHO_ARQUIVO_XML}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
