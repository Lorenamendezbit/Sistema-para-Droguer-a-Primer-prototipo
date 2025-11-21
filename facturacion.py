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


# ===============================
#       PROGRAMA INTERACTIVO
# ===============================

print("=== SISTEMA DE FACTURACIÓN ===")

factura = Factura()

while True:
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = input("Nombre del producto: ")

    try:
        cantidad = int(input("Cantidad: "))
        precio = int(input("Precio unitario: "))
    except ValueError:
        print("Error: ingresa números válidos.")
        continue

    factura.agregar_item(nombre, cantidad, precio)

    continuar = input("\n¿Agregar otro producto? (s/n): ").lower()
    if continuar != "s":
        break

factura.generar_factura()
print("Gracias por usar el sistema.")
