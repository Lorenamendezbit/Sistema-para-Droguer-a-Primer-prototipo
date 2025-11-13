# ====================================================================================
# MÓDULO 6: Facturación / Estadísticas / Métodos de Pago
# Autor: Charly torres
# ====================================================================================

import datetime

# -------------------------------
# Clase Producto
# -------------------------------
class Producto:
    def __init__(self, id_producto, nombre, precio):
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio

# -------------------------------
# Clase ItemFactura
# -------------------------------
class ItemFactura:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = producto.precio * cantidad

# -------------------------------
# Clase Factura
# -------------------------------
class Factura:
    contador_id = 1

    def __init__(self, cliente, metodo_pago):
        self.id = Factura.contador_id
        Factura.contador_id += 1
        self.cliente = cliente
        self.items = []
        self.metodo_pago = metodo_pago
        self.fecha = datetime.datetime.now()
        self.total = 0

    def agregar_item(self, item):
        self.items.append(item)
        self.total += item.subtotal

    def mostrar_factura(self):
        print("\n========== FACTURA ==========")
        print(f"Factura N°: {self.id}")
        print(f"Cliente: {self.cliente}")
        print(f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-----------------------------")
        for item in self.items:
            print(f"{item.producto.nombre} x{item.cantidad} - ${item.subtotal:.2f}")
        print("-----------------------------")
        print(f"TOTAL: ${self.total:.2f}")
        print(f"Método de pago: {self.metodo_pago}")
        print("=============================\n")

# -------------------------------
# Clase SistemaFacturacion
# -------------------------------
class SistemaFacturacion:
    def __init__(self):
        self.productos = [
            Producto(1, "Paracetamol 500mg", 2.5),
            Producto(2, "Ibuprofeno 400mg", 3.0),
            Producto(3, "Jarabe para la tos", 5.5)
        ]
        self.metodos_pago = ["Efectivo", "Tarjeta de Crédito", "Tarjeta Débito", "Transferencia"]
        self.facturas = []

    # Generar una nueva factura
    def generar_factura(self):
        print("\n=== Generar Nueva Factura ===")
        cliente = input("Nombre del cliente: ")

        print("\nMétodos de pago disponibles:")
        for i, metodo in enumerate(self.metodos_pago, 1):
            print(f"{i}. {metodo}")

        try:
            indice_metodo = int(input("Seleccione método de pago: "))
            metodo_pago = self.metodos_pago[indice_metodo - 1]
        except (ValueError, IndexError):
            print("Opción inválida. Se asignará 'Efectivo'.")
            metodo_pago = "Efectivo"

        factura = Factura(cliente, metodo_pago)

        while True:
            print("\nProductos disponibles:")
            for p in self.productos:
                print(f"{p.id}. {p.nombre} - ${p.precio}")

            try:
                id_producto = int(input("Ingrese el ID del producto (0 para terminar): "))
            except ValueError:
                print("Valor inválido.")
                continue

            if id_producto == 0:
                break

            producto = next((p for p in self.productos if p.id == id_producto), None)
            if not producto:
                print("Producto no encontrado.")
                continue

            try:
                cantidad = int(input("Cantidad: "))
            except ValueError:
                print("Cantidad inválida.")
                continue

            item = ItemFactura(producto, cantidad)
            factura.agregar_item(item)

        if not factura.items:
            print("No se agregó ningún producto.")
            return

        self.facturas.append(factura)
        print("\nFactura generada exitosamente.")
        factura.mostrar_factura()

    # Mostrar todas las facturas
    def mostrar_facturas(self):
        if not self.facturas:
            print("No hay facturas registradas.")
            return
        for f in self.facturas:
            f.mostrar_factura()

    # Mostrar estadísticas
    def mostrar_estadisticas(self):
        if not self.facturas:
            print("\nNo hay facturas registradas.")
            return

        print("\n=== Estadísticas de Ventas ===")
        total_ventas = sum(f.total for f in self.facturas)
        num_facturas = len(self.facturas)
        promedio = total_ventas / num_facturas
        ventas_por_metodo = {}

        for f in self.facturas:
            ventas_por_metodo[f.metodo_pago] = ventas_por_metodo.get(f.metodo_pago, 0) + f.total

        print(f"Total facturas: {num_facturas}")
        print(f"Total recaudado: ${total_ventas:.2f}")
        print(f"Promedio por factura: ${promedio:.2f}")

        print("\nVentas por método de pago:")
        for metodo, total in ventas_por_metodo.items():
            print(f"- {metodo}: ${total:.2f}")

    # Menú del módulo
    def menu(self):
        while True:
            print("""
=========================
   MÓDULO DE FACTURACIÓN
=========================
1. Generar Factura
2. Ver Estadísticas
3. Ver Facturas Generadas
4. Salir al menú principal
""")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.generar_factura()
            elif opcion == "2":
                self.mostrar_estadisticas()
            elif opcion == "3":
                self.mostrar_facturas()
            elif opcion == "4":
                print("Regresando al menú principal...")
                break
            else:
                print("Opción inválida.")


# -------------------------------
# Ejecución directa del módulo
# -------------------------------
if __name__ == "__main__":
    sistema = SistemaFacturacion()
    sistema.menu()
