import datetime

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
