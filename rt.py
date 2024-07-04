import tkinter as tk
from tkinter import messagebox, simpledialog
import paramiko
import time  # Importar la librería time

# Configuración de conexión SSH
ROUTER_IP = '192.168.56.253'  # Dirección IP del router en VirtualBox
ROUTER_USERNAME = 'jos'  # Nombre de usuario del router
ROUTER_PASSWORD = 'jos123'  # Contraseña del router


# Función para ejecutar comandos en el router
def ejecutar_comando(comando):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ROUTER_IP, username=ROUTER_USERNAME, password=ROUTER_PASSWORD)

        shell = ssh.invoke_shell()
        shell.send(comando + '\n')
        time.sleep(1)  # Usar time.sleep para pausar la ejecución
        salida = shell.recv(10000).decode()

        ssh.close()

        return salida
    except Exception as e:
        return f"Error al conectar: {e}"


# Funciones específicas del router
def crear_loopback(interface):
    comando = f"configure terminal\ninterface loopback {interface}\nend"
    return ejecutar_comando(comando)


def eliminar_loopback(interface):
    comando = f"configure terminal\nno interface loopback {interface}\nend"
    return ejecutar_comando(comando)


def editar_banner(banner):
    comando = f"configure terminal\nbanner motd ^C{banner}^C\nend"
    return ejecutar_comando(comando)


def mostrar_configuracion():
    comando = "show running-config"
    return ejecutar_comando(comando)


def reiniciar_router():
    comando = "reload\n"
    return ejecutar_comando(comando)


def cambiar_contrasena(usuario, nueva_contrasena):
    comando = f"configure terminal\nusername {usuario} password {nueva_contrasena}\nend"
    return ejecutar_comando(comando)


def agregar_vlan(vlan_id, nombre_vlan):
    comando = f"configure terminal\nvlan {vlan_id}\nname {nombre_vlan}\nend"
    return ejecutar_comando(comando)


# Funciones de la interfaz gráfica
def crear_loopback_interfaz():
    interface = simpledialog.askstring("Crear Loopback", "Nombre de la interfaz loopback:")
    if interface:
        resultado = crear_loopback(interface)
        messagebox.showinfo("Resultado", resultado)


def eliminar_loopback_interfaz():
    interface = simpledialog.askstring("Eliminar Loopback", "Nombre de la interfaz loopback:")
    if interface:
        resultado = eliminar_loopback(interface)
        messagebox.showinfo("Resultado", resultado)


def editar_banner_interfaz():
    banner = simpledialog.askstring("Editar Banner", "Nuevo banner:")
    if banner:
        resultado = editar_banner(banner)
        messagebox.showinfo("Resultado", resultado)


def mostrar_configuracion_interfaz():
    configuracion = mostrar_configuracion()
    messagebox.showinfo("Configuración del Router", configuracion)


def reiniciar_router_interfaz():
    resultado = reiniciar_router()
    messagebox.showinfo("Resultado", resultado)


def cambiar_contrasena_interfaz():
    usuario = simpledialog.askstring("Cambiar Contraseña", "Nombre de usuario:")
    if usuario:
        nueva_contrasena = simpledialog.askstring("Cambiar Contraseña", "Nueva contraseña:", show='*')
        if nueva_contrasena:
            resultado = cambiar_contrasena(usuario, nueva_contrasena)
            messagebox.showinfo("Resultado", resultado)


def agregar_vlan_interfaz():
    vlan_id = simpledialog.askstring("Agregar VLAN", "ID de la VLAN:")
    if vlan_id:
        nombre_vlan = simpledialog.askstring("Agregar VLAN", "Nombre de la VLAN:")
        if nombre_vlan:
            resultado = agregar_vlan(vlan_id, nombre_vlan)
            messagebox.showinfo("Resultado", resultado)


# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Router Virtual")

# Crear los botones y asignar las funciones
btn_crear_loopback = tk.Button(root, text="Crear Loopback", command=crear_loopback_interfaz)
btn_eliminar_loopback = tk.Button(root, text="Eliminar Loopback", command=eliminar_loopback_interfaz)
btn_editar_banner = tk.Button(root, text="Editar Banner", command=editar_banner_interfaz)
btn_mostrar_configuracion = tk.Button(root, text="Mostrar Configuración", command=mostrar_configuracion_interfaz)
btn_reiniciar_router = tk.Button(root, text="Reiniciar Router", command=reiniciar_router_interfaz)
btn_cambiar_contrasena = tk.Button(root, text="Cambiar Contraseña", command=cambiar_contrasena_interfaz)
btn_agregar_vlan = tk.Button(root, text="Agregar VLAN", command=agregar_vlan_interfaz)

# Organizar los botones en la ventana
btn_crear_loopback.pack(pady=5)
btn_eliminar_loopback.pack(pady=5)
btn_editar_banner.pack(pady=5)
btn_mostrar_configuracion.pack(pady=5)
btn_reiniciar_router.pack(pady=5)
btn_cambiar_contrasena.pack(pady=5)
btn_agregar_vlan.pack(pady=5)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
