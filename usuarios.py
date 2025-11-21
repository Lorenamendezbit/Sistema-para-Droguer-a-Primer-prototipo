class Usuario:
    def __init__(self, nombre, cedula, telefono):
        self.nombre = nombre
        self.cedula = cedula
        self.telefono = telefono
    
    def __str__(self):
        return f"{self.nombre} - {self.cedula} - {self.telefono}"

class Cliente:
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
    
    def __str__(self):
        return f"{self.nombre} - {self.documento} - {self.telefono}"

class GestionUsuarios:
    def __init__(self):
        self.usuarios = []
    
    def registrar_usuario(self):
        print("||       Registro de Usuario      ||")
        print("------------------------------------")
        nombre = input("Ingrese el nombre del usuario: ")
        cedula = input("Ingrese la cedula: ")
        telefono = input("Ingrese el telefono: ")
        
        for u in self.usuarios:
            if u.cedula == cedula:
                print("Ya existe un usuario con esa cedula.")
                return False
        
        nuevo = Usuario(nombre, cedula, telefono)
        self.usuarios.append(nuevo)
        print("Usuario registrado correctamente.")
        return True
    
    def editar_usuario(self, cedula):
        for u in self.usuarios:
            if u.cedula == cedula:
                print("Deje en blanco para no cambiar el dato")
                nuevo_nombre = input("Nuevo nombre: ")
                nuevo_telefono = input("Nuevo telefono: ")
                
                if nuevo_nombre:
                    u.nombre = nuevo_nombre
                if nuevo_telefono:
                    u.telefono = nuevo_telefono
                
                print("Usuario actualizado correctamente.")
                return True
        
        print("No se encontro un usuario con esa cedula.")
        return False
    
    def eliminar_usuario(self, cedula):
        for u in self.usuarios:
            if u.cedula == cedula:
                self.usuarios.remove(u)
                print("Usuario eliminado correctamente.")
                return True
        
        print("No existe usuario con esa cedula.")
        return False
    
    def listar_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return
        
        print("\n--- LISTA DE USUARIOS ---")
        for u in self.usuarios:
            print(u)
        print("----------------------------\n")

class GestionClientes:
    def __init__(self):
        self.clientes = []
    
    def registrar_cliente(self):
        print("||       Registro de Cliente      ||")
        print("------------------------------------")
        nombre = input("Ingrese el nombre del cliente: ")
        documento = input("Ingrese el numero de documento: ")
        telefono = input("Ingrese el telefono: ")
        
        for c in self.clientes:
            if c.documento == documento:
                print("Ya existe un cliente con ese documento.")
                return False
        
        nuevo = Cliente(nombre, documento, telefono)
        self.clientes.append(nuevo)
        print("Cliente registrado correctamente.")
        return True
    
    def editar_cliente(self, documento):
        for c in self.clientes:
            if c.documento == documento:
                print("Deje en blanco para no cambiar el dato")
                nuevo_nombre = input("Nuevo nombre: ")
                nuevo_telefono = input("Nuevo telefono: ")
                
                if nuevo_nombre:
                    c.nombre = nuevo_nombre
                if nuevo_telefono:
                    c.telefono = nuevo_telefono
                
                print("Cliente actualizado correctamente.")
                return True
        
        print("No se encontro un cliente con ese documento.")
        return False
    
    def eliminar_cliente(self, documento):
        for c in self.clientes:
            if c.documento == documento:
                self.clientes.remove(c)
                print("Cliente eliminado correctamente.")
                return True
        
        print("No existe cliente con ese documento.")
        return False
    
    def listar_clientes(self):
        if not self.clientes:
            print("No hay clientes registrados.")
            return
        
        print("\n--- LISTA DE CLIENTES ---")
        for c in self.clientes:
            print(c)
        print("----------------------------\n")

def menu_principal():
    gestion_usuarios = GestionUsuarios()
    gestion_clientes = GestionClientes()
    
    while True:
        print("\x1b[;34m"+"\n=== MENU PRINCIPAL - SISTEMA DE GESTION DROGUERIA ===")
        print("1. Gestion de Usuarios")
        print("2. Gestion de Clientes")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            menu_usuarios(gestion_usuarios)
        elif opcion == "2":
            menu_clientes(gestion_clientes)
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida.")

def menu_usuarios(gestion):
    while True:
        print("\x1b[;34m"+"=== MENU USUARIOS ===")
        print("1. Registrar usuario")
        print("2. Editar usuario")
        print("3. Eliminar usuario")
        print("4. Listar usuarios")
        print("5. Volver al menu principal")
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            gestion.registrar_usuario()
        elif opcion == "2":
            cedula = input("Ingrese la cedula del usuario a editar: ")
            gestion.editar_usuario(cedula)
        elif opcion == "3":
            cedula = input("Ingrese la cedula del usuario a eliminar: ")
            gestion.eliminar_usuario(cedula)
        elif opcion == "4":
            gestion.listar_usuarios()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")

def menu_clientes(gestion):
    while True:
        print("\x1b[;34m"+"=== MENU CLIENTES ===")
        print("1. Registrar cliente")
        print("2. Editar cliente")
        print("3. Eliminar cliente")
        print("4. Listar clientes")
        print("5. Volver al menu principal")
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            gestion.registrar_cliente()
        elif opcion == "2":
            documento = input("Ingrese el documento del cliente a editar: ")
            gestion.editar_cliente(documento)
        elif opcion == "3":
            documento = input("Ingrese el documento del cliente a eliminar: ")
            gestion.eliminar_cliente(documento)
        elif opcion == "4":
            gestion.listar_clientes()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    menu_principal()