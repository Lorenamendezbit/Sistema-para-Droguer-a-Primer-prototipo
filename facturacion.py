class Factura:
    def __init__(self):
        self.items = []  # (nombre, cantidad, precio)

    def agregar_item(self, nombre, cantidad, precio):
        self.items.append((nombre, cantidad, precio))

    def calcular_total(self):
        total = 0
        for nombre, cantidad, precio in self.items:
            total += cantidad * precio
        return total

    def generar_factura(self):
        print("\n===== FACTURA =====")
        print("Productos:")

        if not self.items:
            print("No hay productos agregados.")
            return

        for nombre, cantidad, precio in self.items:
            subtotal = cantidad * precio
            print(f" - {nombre} x{cantidad} = ${subtotal}")

        print("\nTOTAL A PAGAR: $", self.calcular_total())
        print("===================\n")

