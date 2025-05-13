import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
from config import Config
from main import WebAutomation

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.init_ui()
        self.load_saved_credentials()

    def init_ui(self):
        self.setWindowTitle('RPA Login Manager')
        self.setFixedSize(400, 300)

        # Widget y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Campos de entrada
        self.url_input = self._create_input_field('URL:', layout)
        self.username_input = self._create_input_field('Usuario:', layout)
        self.password_input = self._create_input_field('Contraseña:', layout, is_password=True)
        self.two_factor_input = self._create_input_field('Código 2FA (opcional):', layout)

        # Checkbox para modo headless
        self.headless_checkbox = QCheckBox('Modo headless (sin interfaz de navegador)', self)
        layout.addWidget(self.headless_checkbox)

        # Botones
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton('Guardar credenciales', self)
        self.save_button.clicked.connect(self.save_credentials)
        button_layout.addWidget(self.save_button)

        self.login_button = QPushButton('Iniciar automatización', self)
        self.login_button.clicked.connect(self.start_automation)
        button_layout.addWidget(self.login_button)

        layout.addLayout(button_layout)

    def _create_input_field(self, label_text: str, layout, is_password: bool = False) -> QLineEdit:
        """Crea un campo de entrada con su etiqueta"""
        container = QWidget()
        field_layout = QHBoxLayout(container)
        field_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        label.setFixedWidth(120)
        field_layout.addWidget(label)

        input_field = QLineEdit()
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        field_layout.addWidget(input_field)

        layout.addWidget(container)
        return input_field

    def load_saved_credentials(self):
        """Carga credenciales guardadas si existen"""
        try:
            credentials = self.config.load_credentials()
            self.url_input.setText(credentials['url'])
            self.username_input.setText(credentials['username'])
            self.password_input.setText(credentials['password'])
        except FileNotFoundError:
            pass

    def save_credentials(self):
        """Guarda las credenciales de forma segura"""
        try:
            self.config.save_credentials(
                url=self.url_input.text(),
                username=self.username_input.text(),
                password=self.password_input.text()
            )
            QMessageBox.information(self, 'Éxito', 'Credenciales guardadas correctamente')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al guardar credenciales: {str(e)}')

    def start_automation(self):
        """Inicia el proceso de automatización"""
        try:
            # Crear instancia de automatización
            bot = WebAutomation(headless=self.headless_checkbox.isChecked())
            
            # Intentar login
            success = bot.login(
                url=self.url_input.text(),
                username=self.username_input.text(),
                password=self.password_input.text(),
                two_factor_code=self.two_factor_input.text() or None
            )

            if success:
                QMessageBox.information(self, 'Éxito', 'Login realizado correctamente')
            else:
                QMessageBox.warning(self, 'Error', 'Error durante el proceso de login')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error en la automatización: {str(e)}')
        finally:
            bot.close()

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()