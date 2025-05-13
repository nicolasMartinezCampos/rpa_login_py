import time
import random
from pathlib import Path
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import Config

class WebAutomation:
    def __init__(self, headless: bool = False, timeout: int = 10):
        self.timeout = timeout
        self.driver = self._setup_driver(headless)
        self.wait = WebDriverWait(self.driver, timeout)

    def _setup_driver(self, headless: bool) -> webdriver.Chrome:
        """Configura el driver de Chrome con opciones anti-detección"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # Opciones anti-detección de bot
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Eliminar webdriver de window.navigator
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver

    def _human_like_type(self, element, text: str):
        """Simula escritura humana con delays aleatorios"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    def _wait_and_find_element(self, by: By, value: str):
        """Espera y encuentra un elemento con manejo de errores"""
        try:
            return self.wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            raise Exception(f"Elemento no encontrado después de {self.timeout} segundos: {value}")

    def login(self, url: str, username: str, password: str, two_factor_code: Optional[str] = None):
        """Realiza el proceso de login con soporte para 2FA"""
        try:
            # Navegar a la página
            self.driver.get(url)
            time.sleep(random.uniform(1, 2))

            # Llenar credenciales
            username_field = self._wait_and_find_element(By.ID, 'username')
            self._human_like_type(username_field, username)
            
            password_field = self._wait_and_find_element(By.ID, 'password')
            self._human_like_type(password_field, password)
            
            # Simular delay humano antes de hacer click
            time.sleep(random.uniform(0.5, 1.5))
            
            # Buscar y hacer click en el botón de login
            login_button = self._wait_and_find_element(
                By.XPATH, "//button[@type='submit'] | //input[@type='submit']")
            login_button.click()

            # Manejar 2FA si está habilitado
            if two_factor_code:
                self._handle_2fa(two_factor_code)

            # Verificar login exitoso
            time.sleep(random.uniform(2, 3))
            if 'login' in self.driver.current_url.lower():
                raise Exception("Error: Login fallido - Credenciales incorrectas")

            print("Login exitoso!")
            return True

        except Exception as e:
            print(f"Error durante el login: {str(e)}")
            return False

    def _handle_2fa(self, code: str):
        """Maneja el proceso de autenticación de dos factores"""
        try:
            # Esperar por el campo de 2FA
            two_factor_field = self._wait_and_find_element(By.ID, '2fa-code')
            self._human_like_type(two_factor_field, code)
            
            # Buscar y hacer click en el botón de verificación
            verify_button = self._wait_and_find_element(
                By.XPATH, "//button[contains(text(), 'Verify')] | //input[@type='submit']")
            verify_button.click()
            
        except TimeoutException:
            raise Exception("Error: Campo de 2FA no encontrado")

    def close(self):
        """Cierra el navegador y libera recursos"""
        if self.driver:
            self.driver.quit()

def main():
    # Cargar configuración
    config = Config()
    try:
        credentials = config.load_credentials()
    except FileNotFoundError:
        print("Archivo de configuración no encontrado. Usando credenciales de ejemplo...")
        credentials = {
            'url': 'https://ejemplo.com/login',
            'username': 'usuario_test',
            'password': '123456'
        }

    # Iniciar automatización
    bot = WebAutomation(headless=False)
    try:
        bot.login(
            url=credentials['url'],
            username=credentials['username'],
            password=credentials['password']
        )
    finally:
        bot.close()

if __name__ == "__main__":
    main()