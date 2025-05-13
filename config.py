import json
import base64
from cryptography.fernet import Fernet
from pathlib import Path

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = Path(config_file)
        self.key = None
        self.fernet = None
        self._initialize_encryption()

    def _initialize_encryption(self):
        """Inicializa o carga la clave de encriptación"""
        key_file = Path('encryption.key')
        if not key_file.exists():
            self.key = Fernet.generate_key()
            key_file.write_bytes(self.key)
        else:
            self.key = key_file.read_bytes()
        self.fernet = Fernet(self.key)

    def save_credentials(self, url: str, username: str, password: str):
        """Guarda las credenciales encriptadas en el archivo de configuración"""
        config = {
            'url': self.fernet.encrypt(url.encode()).decode(),
            'username': self.fernet.encrypt(username.encode()).decode(),
            'password': self.fernet.encrypt(password.encode()).decode()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def load_credentials(self):
        """Carga y desencripta las credenciales"""
        if not self.config_file.exists():
            raise FileNotFoundError(f'Archivo de configuración no encontrado: {self.config_file}')

        with open(self.config_file) as f:
            config = json.load(f)

        return {
            'url': self.fernet.decrypt(config['url'].encode()).decode(),
            'username': self.fernet.decrypt(config['username'].encode()).decode(),
            'password': self.fernet.decrypt(config['password'].encode()).decode()
        }