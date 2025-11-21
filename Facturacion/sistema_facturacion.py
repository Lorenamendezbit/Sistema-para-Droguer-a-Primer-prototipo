from .producto import Producto
from .item_factura import ItemFactura
from .factura import Factura

class SistemaFacturacion:
    def __init__(self):
        self.productos = [
            Producto(1, "Paracetamol 500mg", 2.5),
            Producto(2, "Ibuprofeno 400mg", 3.0),
            Producto(3, "Jarabe para la tos", 5.5)
        ]
        self.metodos_pago = ["Efectivo", "Tarjeta de Crédito", "Tarjeta Débito", "Transferencia"]
        self.facturas = []

    def generar_factura(self):
        print("\n=== Generar Nueva Factura ===")
        cliente = input("Nombre del cliente: ")

        print("\nMétodos de pago disponibles:")
        for i, metodo in enumerate(self.metodos_pago, 1):
            print(f"{i}. {metodo}")

        try:
            indice_metodo = int(input("Seleccione método de pago: "))
            metodo_pago = self.metodos_pago[indice_metodo - 1]
        except:
            metodo_pago = "Efectivo"

        factura = Factura(cliente, metodo_pago)

        while True:
            print("\nProductos disponibles:")
            for p in self.productos:
                print(f"{p.id}. {p.nombre} - ${p.precio}")

            try:
                id_producto = int(input("Ingrese el ID del producto (0 para terminar): "))
            except:
                continue

            if id_producto == 0:
                break

            producto = next((p for p in self.productos if p.id == id_producto), None)
            if not producto:
                print("Producto no encontrado.")
                continue

            try:
                cantidad = int(input("Cantidad: "))
            except:
                continue

            factura.agregar_item(ItemFactura(producto, cantidad))

        if factura.items:
            self.facturas.append(factura)
            factura.mostrar_factura()
        else:
            print("No se agregó ningún producto.")

    def mostrar_facturas(self):
        if not self.facturas:
            print("No hay facturas registradas.")
            return
        
        for f in self.facturas:
            f.mostrar_factura()

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
