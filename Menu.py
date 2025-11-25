from usuarios import SistemaLogin,GestionUsuarios,GestionClientes
from inventario import Inventario, Producto, Notificaciones
from ventas import SistemaVentas

class SistemaDrogueria:
    def __init__(self):
        self.sistema_login = SistemaLogin()
        self.gestion_usuarios = GestionUsuarios()
        self.gestion_clientes = GestionClientes()
        self.inventario = Inventario()
        self.notificaciones = Notificaciones(self.inventario)
        self.sistema_ventas = SistemaVentas(self.inventario, self.gestion_clientes)
    
    def menu_autenticacion(self):
        while True:
            print("\n" + "="*70)
            print(" "*22 + "SISTEMA DE DROGUERIA")
            print(" "*27 + "Bienvenido")
            print("="*70)
            print("\n\033[;34m1.\033[0;m Registrarse")
            print("\033[;34m2.\033[0;m Iniciar sesion")
            print("\033[;34m3.\033[0;m Salir")
            print("-"*70)
            
            opcion = input("Seleccione una opcion: ").strip()
            
            if opcion == "1":
                self.sistema_login.registrar_usuario_sistema()
            elif opcion == "2":
                if self.sistema_login.iniciar_sesion():
                    return True
            elif opcion == "3":
                print("\nHasta pronto!")
                return False
            else:
                print("\033[;31mOpcion invalida.\033[0;m")
    
    def menu_principal(self):
        while True:
            if self.notificaciones.hay_alertas():
                print("\n\033[;33m HAY ALERTAS PENDIENTES \033[0;m")
            
            print("\n" + "="*70)
            nombre_usuario = self.sistema_login.obtener_nombre_usuario()
            rol = "ADMINISTRADOR" if self.sistema_login.es_admin else "USUARIO"
            print(f" "*15 + f"MENU PRINCIPAL - {rol}")
            print(f" "*20 + f"Usuario: {nombre_usuario}")
            print("="*70)
            
            print("\n\033[;36mINVENTARIO\033[0;m")
            print("  1. Gestionar Inventario")
            
            print("\n\033[;36mNOTIFICACIONES\033[0;m")
            print("  2. Ver Alertas y Notificaciones")
            
            print("\n\033[;36mVENTAS\033[0;m")
            print("  3. Realizar Venta")
            print("  4. Historial de Ventas")
            print("  5. Estadisticas")
            
            if self.sistema_login.es_admin:
                print("\n\033[;36mGESTION (Solo Admin)\033[0;m")
                print("  6. Gestionar Usuarios del Sistema")
                print("  7. Gestionar Clientes")
            
            print("\n\033[;31mSALIR\033[0;m")
            print("  0. Cerrar sesion")
            
            print("-"*70)
            opcion = input("Seleccione una opcion: ").strip()
            
            if opcion == "1":
                self.menu_inventario()
            elif opcion == "2":
                self.notificaciones.mostrar_alertas()
                input("\nPresione ENTER para continuar...")
            elif opcion == "3":
                self.sistema_ventas.realizar_venta()
            elif opcion == "4":
                self.sistema_ventas.ver_historial_ventas()
                input("\nPresione ENTER para continuar...")
            elif opcion == "5":
                self.sistema_ventas.generar_estadisticas()
                input("\nPresione ENTER para continuar...")
            elif opcion == "6" and self.sistema_login.es_admin:
                self.menu_usuarios()
            elif opcion == "7" and self.sistema_login.es_admin:
                self.menu_clientes()
            elif opcion == "0":
                self.sistema_login.cerrar_sesion()
                break
            else:
                print("\033[;31mOpcion invalida.\033[0;m")
    
    def menu_inventario(self):
        while True:
            print("\n" + "="*70)
            print(" "*24 + "GESTION DE INVENTARIO")
            print("="*70)
            print("\n1. Ver inventario completo")
            print("2. Buscar producto")
            print("3. Agregar producto")
            print("4. Editar producto")
            print("5. Eliminar producto")
            print("0. Volver al menu principal")
            print("-"*70)
            
            opcion = input("Seleccione una opcion: ").strip()
            
            if opcion == "1":
                self.inventario.mostrar_inventario()
                input("\nPresione ENTER para continuar...")
            
            elif opcion == "2":
                texto = input("Buscar por nombre o codigo: ").strip()
                resultados = self.inventario.buscar(texto)
                
                print("\n--- RESULTADOS DE BUSQUEDA ---")
                if not resultados:
                    print("No se encontraron coincidencias.")
                else:
                    for p in resultados:
                        print(f"\n{p.codigo} - {p.nombre}")
                        print(f"  Cantidad: {p.cantidad} | Precio: ${p.precio} | Vence: {p.fecha_vencimiento}")
                input("\nPresione ENTER para continuar...")
            
            elif opcion == "3":
                print("\n--- AGREGAR NUEVO PRODUCTO ---")
                codigo = input("Codigo: ").strip()
                nombre = input("Nombre: ").strip()
                cantidad = input("Cantidad: ").strip()
                stock = input("Stock minimo: ").strip()
                precio = input("Precio: ").strip()
                fecha = input("Fecha vencimiento (dd-mm-aaaa): ").strip()
                
                try:
                    self.inventario.agregar_producto(
                        Producto(codigo, nombre, cantidad, stock, precio, fecha)
                    )
                except Exception as e:
                    print(f"\033[;31mError al agregar producto: {e}\033[0;m")
                input("\nPresione ENTER para continuar...")
            
            elif opcion == "4":
                codigo = input("Codigo del producto a editar: ").strip()
                self.inventario.editar_producto(codigo)
                input("\nPresione ENTER para continuar...")
            
            elif opcion == "5":
                codigo = input("Codigo del producto a eliminar: ").strip()
                confirmar = input(f"Esta seguro de eliminar el producto {codigo}? (s/n): ").lower()
                if confirmar == 's':
                    self.inventario.eliminar_producto(codigo)
                else:
                    print("Operacion cancelada.")
                input("\nPresione ENTER para continuar...")
            
            elif opcion == "0":
                break
            
            else:
                print("\033[;31mOpcion invalida.\033[0;m")
    
    def menu_usuarios(self):
        while True:
            print("\n" + "="*70)
            print(" "*22 + "GESTION DE USUARIOS")
            print("="*70)
            print("\n1. Registrar usuario")
            print("2. Editar usuario")
            print("3. Eliminar usuario")
            print("4. Listar usuarios")
            print("0. Volver al menu principal")
            print("-"*70)
            
            opcion = input("Seleccione una opcion: ").strip()
            
            if opcion == "1":
                self.gestion_usuarios.registrar_usuario()
            elif opcion == "2":
                self.gestion_usuarios.editar_usuario()
            elif opcion == "3":
                cedula = input("Ingrese la cedula del usuario a eliminar: ")
                self.gestion_usuarios.eliminar_usuario(cedula)
            elif opcion == "4":
                self.gestion_usuarios.listar_usuarios()
            elif opcion == "0":
                break
            else:
                print("\033[;31mOpcion invalida.\033[0;m")
            
            if opcion in ["1", "2", "3", "4"]:
                input("\nPresione ENTER para continuar...")
    
    def menu_clientes(self):
        while True:
            print("\n" + "="*70)
            print(" "*22 + "GESTION DE CLIENTES")
            print("="*70)
            print("\n1. Registrar cliente")
            print("2. Editar cliente")
            print("3. Eliminar cliente")
            print("4. Listar clientes")
            print("0. Volver al menu principal")
            print("-"*70)
            
            opcion = input("Seleccione una opcion: ").strip()
            
            if opcion == "1":
                self.gestion_clientes.registrar_cliente()
            elif opcion == "2":
                documento = input("Ingrese el documento del cliente a editar: ")
                self.gestion_clientes.editar_cliente(documento)
            elif opcion == "3":
                documento = input("Ingrese el documento del cliente a eliminar: ")
                self.gestion_clientes.eliminar_cliente(documento)
            elif opcion == "4":
                self.gestion_clientes.listar_clientes()
            elif opcion == "0":
                break
            else:
                print("\033[;31mOpcion invalida.\033[0;m")
            
            if opcion in ["1", "2", "3", "4"]:
                input("\nPresione ENTER para continuar...")
    
    def iniciar(self):
        print("\n" + "="*70)
        print(" "*22 + "SISTEMA DE DROGUERIA")
        print(" "*27 + "Version 1.0")
        print("="*70)
        
        if self.menu_autenticacion():
            self.menu_principal()
        
        print("\n" + "="*70)
        print(" "*20 + "Sesion finalizada")
        print(" "*15 + "Gracias por usar el sistema")
        print("="*70)


# ========================================
#           EJECUCION DEL SISTEMA
# ========================================

sistema = SistemaDrogueria()
sistema.iniciar()