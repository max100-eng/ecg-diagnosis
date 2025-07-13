from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def upload_ecg_via_ui(file_path):
    driver = webdriver.Chrome()
    driver.get("https://max100.free.nf/diagnosis/index.html")

    # Simular subida de archivo (ajusta los selectores según la página)
    upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload_input.send_keys(file_path)

    # Esperar análisis (ajusta el tiempo o lógica de espera)
    time.sleep(10)
    results = driver.find_element(By.ID, "results").text
    print("Resultados:", results)

    driver.quit()

# Uso
upload_ecg_via_ui("ruta/a/tu_ecg.csv")