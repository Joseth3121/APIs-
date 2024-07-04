import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import json
from PyQt5 import QtWidgets, QtGui, QtCore

# Configuración de conexión al router
ROUTER_IP = '192.168.56.253'
USERNAME = 'cisco'
PASSWORD = 'cisco123!'
BASE_URL = f'https://{ROUTER_IP}/restconf'

# Desactivar las advertencias de SSL (no recomendable para producción)
requests.packages.urllib3.disable_warnings()


# Funciones para gestionar usuarios
def get_users():
    url = f'{BASE_URL}/data/Cisco-IOS-XE-native:native/username'
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD),
                            headers={'Accept': 'application/yang-data+json'}, verify=False)

    if response.status_code == 200:
        return response.json().get('Cisco-IOS-XE-native:username', [])
    else:
        return []


def create_user(username, password, privilege):
    url = f'{BASE_URL}/data/Cisco-IOS-XE-native:native/username={username}'
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }
    payload = {
        "Cisco-IOS-XE-native:username": {
            "name": username,
            "privilege": privilege,
            "secret": {
                "encryption": 0,
                "secret": password
            }
        }
    }

    response = requests.put(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, data=json.dumps(payload),
                            verify=False)
    return response.status_code


def delete_user(username):
    url = f'{BASE_URL}/data/Cisco-IOS-XE-native:native/username={username}'
    headers = {
        'Accept': 'application/yang-data+json'
    }

    response = requests.delete(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, verify=False)
    return response.status_code


# Funciones para la gestión del hostname
def get_hostname():
    url = f'{BASE_URL}/data/Cisco-IOS-XE-native:native/hostname'
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD),
                            headers={'Accept': 'application/yang-data+json'}, verify=False)

    if response.status_code == 200:
        return response.json().get('Cisco-IOS-XE-native:hostname', '')
    else:
        return ''


def set_hostname(hostname):
    url = f'{BASE_URL}/data/Cisco-IOS-XE-native:native/hostname'
    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }
    payload = {
        "Cisco-IOS-XE-native:hostname": hostname
    }

    response = requests.put(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, data=json.dumps(payload),
                            verify=False)
    return response.status_code


def delete_hostname():
    url = f'{BASE_URL}/data/Cisco-IOS-XE-native:native/hostname'
    headers = {
        'Accept': 'application/yang-data+json'
    }

    response = requests.delete(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers=headers, verify=False)
    return response.status_code


# Funciones para la gestión de ping
def ping_device(ip_address):
    command = f"ping {ip_address}"
    response = os.popen(command).read()
    return response


# Interfaz gráfica con PyQt5
class RouterManagementApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestión de Router')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QtWidgets.QVBoxLayout()

        # Logo y título
        logo_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('logo.png')  # Ajusta la ruta de la imagen según tu configuración
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        title_label = QtWidgets.QLabel('Interfaz de Gestión de Router', self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Pestañas para organización
        tabs = QtWidgets.QTabWidget()

        # Pestaña de Usuarios
        users_tab = QtWidgets.QWidget()
        self.setup_users_tab(users_tab)
        tabs.addTab(users_tab, 'Usuarios')

        # Pestaña de Hostname
        hostname_tab = QtWidgets.QWidget()
        self.setup_hostname_tab(hostname_tab)
        tabs.addTab(hostname_tab, 'Hostname')

        # Pestaña de Ping
        ping_tab = QtWidgets.QWidget()
        self.setup_ping_tab(ping_tab)
        tabs.addTab(ping_tab, 'Ping')

        main_layout.addWidget(tabs)

        # Botón de salida
        exit_button = QtWidgets.QPushButton('Salir')
        exit_button.clicked.connect(QtWidgets.qApp.quit)
        main_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignRight)

        self.setLayout(main_layout)

    def setup_users_tab(self, tab):
        layout = QtWidgets.QVBoxLayout(tab)

        # Contenido de la pestaña de Usuarios
        users_label = QtWidgets.QLabel('Usuarios', tab)
        users_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(users_label)

        users_list = QtWidgets.QListWidget()
        self.refresh_users(users_list)
        layout.addWidget(users_list)

        add_user_layout = QtWidgets.QHBoxLayout()

        self.username_entry = QtWidgets.QLineEdit()
        self.username_entry.setPlaceholderText('Nombre de Usuario')
        add_user_layout.addWidget(self.username_entry)

        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setPlaceholderText('Contraseña')
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        add_user_layout.addWidget(self.password_entry)

        self.privilege_entry = QtWidgets.QLineEdit()
        self.privilege_entry.setPlaceholderText('Privilegio')
        add_user_layout.addWidget(self.privilege_entry)

        add_user_button = QtWidgets.QPushButton('Agregar Usuario')
        add_user_button.clicked.connect(self.add_user)
        add_user_layout.addWidget(add_user_button)

        layout.addLayout(add_user_layout)

        delete_user_layout = QtWidgets.QHBoxLayout()

        self.delete_username_entry = QtWidgets.QLineEdit()
        self.delete_username_entry.setPlaceholderText('Nombre de Usuario a Eliminar')
        delete_user_layout.addWidget(self.delete_username_entry)

        delete_user_button = QtWidgets.QPushButton('Eliminar Usuario')
        delete_user_button.clicked.connect(self.remove_user)
        delete_user_layout.addWidget(delete_user_button)

        layout.addLayout(delete_user_layout)

    def setup_hostname_tab(self, tab):
        layout = QtWidgets.QVBoxLayout(tab)

        # Contenido de la pestaña de Hostname
        hostname_label = QtWidgets.QLabel('Hostname', tab)
        hostname_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(hostname_label)

        current_hostname_label = QtWidgets.QLabel(f'Hostname actual: {get_hostname()}', tab)
        current_hostname_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(current_hostname_label)

        change_hostname_layout = QtWidgets.QHBoxLayout()

        self.hostname_entry = QtWidgets.QLineEdit()
        self.hostname_entry.setPlaceholderText('Nuevo Hostname')
        change_hostname_layout.addWidget(self.hostname_entry)

        change_hostname_button = QtWidgets.QPushButton('Cambiar Hostname')
        change_hostname_button.clicked.connect(self.change_hostname)
        change_hostname_layout.addWidget(change_hostname_button)

        layout.addLayout(change_hostname_layout)

    def setup_ping_tab(self, tab):
        layout = QtWidgets.QVBoxLayout(tab)

        # Contenido de la pestaña de Ping
        ping_label = QtWidgets.QLabel('Ping', tab)
        ping_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(ping_label)

        self.ping_entry = QtWidgets.QLineEdit()
        self.ping_entry.setPlaceholderText('Ingrese la dirección IP para hacer ping')
        layout.addWidget(self.ping_entry)

        ping_button = QtWidgets.QPushButton('Enviar Ping')
        ping_button.clicked.connect(self.ping_device_dialog)
        layout.addWidget(ping_button)

        self.ping_result_text = QtWidgets.QTextEdit()
        self.ping_result_text.setReadOnly(True)
        layout.addWidget(self.ping_result_text)

        clear_ping_button = QtWidgets.QPushButton('Limpiar Resultados')
        clear_ping_button.clicked.connect(self.clear_ping_results)
        layout.addWidget(clear_ping_button)

    def refresh_users(self, users_list):
        users = get_users()
        users_list.clear()
        for user in users:
            users_list.addItem(f"Nombre: {user['name']}, Privilegio: {user.get('privilege', 'N/A')}")

    def add_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        privilege = self.privilege_entry.text()

        if username and password and privilege:
            status_code = create_user(username, password, privilege)
            if status_code == 201 or status_code == 204:
                self.refresh_users(self.findChild(QtWidgets.QListWidget))
            else:
                QtWidgets.QMessageBox.warning(self, 'Error',
                                              f"No se pudo agregar usuario {username}. Código de estado: {status_code}")
        else:
            QtWidgets.QMessageBox.warning(self, 'Campos Incompletos',
                                          'Por favor, complete todos los campos para agregar un usuario.')

    def remove_user(self):
        username = self.delete_username_entry.text()
        if username:
            status_code = delete_user(username)
            if status_code == 204:
                self.refresh_users(self.findChild(QtWidgets.QListWidget))
            else:
                QtWidgets.QMessageBox.warning(self, 'Error',
                                              f"No se pudo eliminar usuario {username}. Código de estado: {status_code}")
        else:
            QtWidgets.QMessageBox.warning(self, 'Campo Vacío', 'Por favor, ingrese el nombre de usuario a eliminar.')

    def change_hostname(self):
        hostname = self.hostname_entry.text()
        if hostname:
            status_code = set_hostname(hostname)
            if status_code == 204:
                QtWidgets.QMessageBox.information(self, 'Éxito', f"Hostname cambiado a {hostname}.")
                self.findChild(QtWidgets.QLabel).setText(f'Hostname actual: {get_hostname()}')
            else:
                QtWidgets.QMessageBox.warning(self, 'Error',
                                              f"No se pudo cambiar el hostname a {hostname}. Código de estado: {status_code}")
        else:
            QtWidgets.QMessageBox.warning(self, 'Campo Vacío', 'Por favor, ingrese el nuevo hostname.')

    def ping_device_dialog(self):
        ip_address = self.ping_entry.text()
        if ip_address:
            ping_result = ping_device(ip_address)
            self.ping_result_text.setText(ping_result)
        else:
            QtWidgets.QMessageBox.warning(self, 'Campo Vacío',
                                          'Por favor, ingrese la dirección IP para realizar el ping.')

    def clear_ping_results(self):
        self.ping_result_text.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = RouterManagementApp()
    window.show()
    sys.exit(app.exec_())
