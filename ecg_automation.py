import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

def automate_ecg_analysis(file_path, ecg_type="standard", headless=False):
    """
    Automatiza la subida y análisis de un ECG en la interfaz web.
    
    :param file_path: Ruta al archivo de ECG (ej: "ecg_data.csv").
    :param ecg_type: Tipo de ECG (debe coincidir con las opciones de la página).
    :param headless: Ejecución sin abrir el navegador (True/False).
    """
    # Configurar Selenium (usando Chrome)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")  # Modo sin interfaz gráfica
    driver = webdriver.Chrome(options=options)

    try:
        # Abrir la página
        driver.get("https://max100.free.nf/diagnosis/index.html")
        print("Página cargada.")

        # 1. Subir archivo de ECG
        upload_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        upload_input.send_keys(file_path)
        print(f"Archivo subido: {file_path}")

        # 2. Seleccionar tipo de ECG (si existe un dropdown)
        try:
            ecg_type_dropdown = driver.find_element(By.ID, "ecg-type")  # Ajusta el selector según la página
            ecg_type_dropdown.send_keys(ecg_type)
            print(f"Tipo de ECG seleccionado: {ecg_type}")
        except:
            print("No se encontró el selector de tipo de ECG. Continuando...")

        # 3. Iniciar análisis (botón "Analizar ECG")
        analyze_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Analizar ECG')]"))
        )
        analyze_button.click()
        print("Análisis iniciado...")

        # 4. Esperar y capturar resultados
        time.sleep(10)  # Ajusta según el tiempo de procesamiento
        results = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "results"))  # Ajusta el selector según la página
        )
        print("\nResultados del análisis:")
        print(results.text)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI para automatizar el análisis de ECG en la interfaz web.")
    parser.add_argument("--file", type=str, required=True, help="Ruta al archivo de ECG (ej: 'ecg_data.csv').")
    parser.add_argument("--type", type=str, default="standard", help="Tipo de ECG (ej: 'standard').")
    parser.add_argument("--headless", action="store_true", help="Ejecutar en modo headless (sin navegador visible).")

    args = parser.parse_args()
    automate_ecg_analysis(args.file, args.type, args.headless)