from datetime import datetime

# ========================================
#           MODULO DE USUARIOS
# ========================================

class Usuario:
    def _init_(self, nombre, cedula, telefono, password=None):
        self.nombre = nombre
        self.cedula = cedula
        self.telefono = telefono
        self.password = password
    
    def _str_(self):
        return f"{self.nombre} | {self.cedula} | {self.telefono}"


class Cliente:
    def _init_(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
    
    def _str_(self):
        return f"{self.nombre} | {self.documento} | {self.telefono}"


class SistemaLogin:
    def _init_(self):
        self.usuario_actual = None
        self.es_admin = False
        self.usuarios_sistema = {}
        # Admin predeterminado
        self.usuarios_sistema["2521"] = {
            "nombre": "Administrador",
            "Telefono": "0000000000",
            "password": "admin123", 
            "tipo": "admin"
        }
    
    def registrar_usuario_sistema(self):
        print("\n==============================================")
        print("      REGISTRO DE USUARIO DEL SISTEMA")
        print("==============================================")
        
        nombre = input("Ingrese su nombre: ")
        
        while True:
            cedula = input("Ingrese la cedula: ")
            if not cedula.isdigit():
                print("\033[;31mLa cedula debe ser un numero valido\033[0;m")
            else:
                break
        
        if cedula in self.usuarios_sistema:
            print("\033[;31mYa existe un usuario registrado con esa cedula.\033[0;m")
            return False
        
        while True:
            telefono = input("Ingrese numero de celular: ")
            if not telefono.isdigit():
                print("\033[;31mDebe ser un numero valido\033[0;m")
            else:
                break
        
        password = input("Establezca su contraseña: ")
        
        while True:
            confirmar = input("Confirme su contraseña: ")
            if password != confirmar:
                print("\033[;31mLas contraseñas no coinciden.\033[0;m")
            else:
                break
        
        self.usuarios_sistema[cedula] = {
            "nombre": nombre,
            "Telefono": telefono,
            "password": password,
            "tipo": "usuario"
        }
        
        print("\033[;32mUsuario registrado correctamente en el sistema.\033[0;m")
        return True
    
    def iniciar_sesion(self):
        print("\n==============================================")
        print("             INICIO DE SESION")
        print("==============================================")
        cedula = input("Cedula: ")
        password = input("Contraseña: ")
        
        if cedula in self.usuarios_sistema and self.usuarios_sistema[cedula]["password"] == password:
            self.usuario_actual = cedula
            self.es_admin = self.usuarios_sistema[cedula]["tipo"] == "admin"
            
            if self.es_admin:
                print("\033[;35;47m  Bienvenido Administrador  \033[0;m")
            else:
                print("\033[;32;47m  Bienvenido Usuario  \033[0;m")
            return True
        else:
            print("\033[;31mCedula o contraseña incorrectos.\033[0;m")
            return False
    
    def cerrar_sesion(self):
        if self.usuario_actual:
            print("\033[;33mSesion cerrada correctamente.\033[0;m")
            self.usuario_actual = None
            self.es_admin = False
        else:
            print("No hay sesion activa.")
    
    def esta_autenticado(self):
        return self.usuario_actual is not None
    
    def obtener_nombre_usuario(self):
        if self.usuario_actual and self.usuario_actual in self.usuarios_sistema:
            return self.usuarios_sistema[self.usuario_actual].get("nombre", "Usuario")
        return "Usuario"


class GestionUsuarios:
    def _init_(self):
        self.usuarios = []
    
    def registrar_usuario(self):
        print("\n==============================================")
        print("         REGISTRO DE USUARIO")
        print("==============================================")
        nombre = input("Ingrese el nombre del usuario: ")
        cedula = input("Ingrese la cedula: ")
        telefono = input("Ingrese el telefono: ")
        
        for u in self.usuarios:
            if u.cedula == cedula:
                print("\033[;31mYa existe un usuario con esa cedula.\033[0;m")
                return False
        
        nuevo = Usuario(nombre, cedula, telefono)
        self.usuarios.append(nuevo)
        print("\033[;32mUsuario registrado correctamente.\033[0;m")
        return True
    
    def editar_usuario(self):
        cedula = input("Ingrese la cedula del usuario a editar: ")
        for u in self.usuarios:
            if u.cedula == cedula:
                print("Deje en blanco para no cambiar el dato")
                nuevo_nombre = input(f"Nuevo nombre [{u.nombre}]: ")
                nuevo_telefono = input(f"Nuevo telefono [{u.telefono}]: ")
                
                if nuevo_nombre:
                    u.nombre = nuevo_nombre
                if nuevo_telefono:
                    u.telefono = nuevo_telefono
                
                print("\033[;32mUsuario actualizado correctamente.\033[0;m")
                return True
        
        print("\033[;31mNo se encontro un usuario con esa cedula.\033[0;m")
        return False
    
    def eliminar_usuario(self, cedula):
        for u in self.usuarios:
            if u.cedula == cedula:
                self.usuarios.remove(u)
                print("\033[;32mUsuario eliminado correctamente.\033[0;m")
                return True
        
        print("\033[;31mNo existe usuario con esa cedula.\033[0;m")
        return False
    
    def listar_usuarios(self):
        if not self.usuarios:
            print("\n--- LISTA DE USUARIOS ---")
            print("No hay usuarios registrados.")
            print("---------------------------")
            return
        
        print("\n--- LISTA DE USUARIOS ---")
        for u in self.usuarios:
            print(u)
        print("---------------------------")


class GestionClientes:
    def _init_(self):
        self.clientes = []
    
    def registrar_cliente(self):
        print("\n==============================================")
        print("         REGISTRO DE CLIENTE")
        print("==============================================")
        nombre = input("Ingrese el nombre del cliente: ")
        documento = input("Ingrese el numero de documento: ")
        telefono = input("Ingrese el telefono: ")
        
        for c in self.clientes:
            if c.documento == documento:
                print("\033[;31mYa existe un cliente con ese documento.\033[0;m")
                return False
        
        nuevo = Cliente(nombre, documento, telefono)
        self.clientes.append(nuevo)
        print("\033[;32mCliente registrado correctamente.\033[0;m")
        return True
    
    def editar_cliente(self, documento):
        for c in self.clientes:
            if c.documento == documento:
                print("Deje en blanco para no cambiar el dato")
                nuevo_nombre = input(f"Nuevo nombre [{c.nombre}]: ")
                nuevo_telefono = input(f"Nuevo telefono [{c.telefono}]: ")
                
                if nuevo_nombre:
                    c.nombre = nuevo_nombre
                if nuevo_telefono:
                    c.telefono = nuevo_telefono
                
                print("\033[;32mCliente actualizado correctamente.\033[0;m")
                return True
        
        print("\033[;31mNo se encontro un cliente con ese documento.\033[0;m")
        return False
    
    def eliminar_cliente(self, documento):
        for c in self.clientes:
            if c.documento == documento:
                self.clientes.remove(c)
                print("\033[;32mCliente eliminado correctamente.\033[0;m")
                return True
        
        print("\033[;31mNo existe cliente con ese documento.\033[0;m")
        return False
    
    def listar_clientes(self):
        if not self.clientes:
            print("\n--- LISTA DE CLIENTES ---")
            print("No hay clientes registrados.")
            print("---------------------------")
            return
        
        print("\n--- LISTA DE CLIENTES ---")
        for c in self.clientes:
            print(c)
        print("---------------------------")
    
    def buscar_cliente(self, documento):
        for c in self.clientes:
            if c.documento == documento:
                return c
        return None
