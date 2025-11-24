from datetime import datetime

# ------------------------------
#      CLASE PRODUCTO
# ------------------------------
class Producto:
    def __init__(self, codigo, nombre, cantidad, stock_minimo, fecha_vencimiento=None):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.stock_minimo = int(stock_minimo)
        self.fecha_vencimiento = fecha_vencimiento  # formato dd-mm-aaaa

    def en_alerta_stock(self):
        return self.cantidad <= self.stock_minimo

    def obtener_fecha_vencimiento(self):
        """Convierte 'dd-mm-aaaa' a un objeto datetime."""
        if not self.fecha_vencimiento:
            return None
        try:
            return datetime.strptime(self.fecha_vencimiento, "%d-%m-%Y")
        except:
            return None

    def dias_para_vencer(self):
        """Retorna días para vencer o None si no hay fecha."""
        fecha_v = self.obtener_fecha_vencimiento()
        if not fecha_v:
            return None

        hoy = datetime.now()
        diferencia = (fecha_v - hoy).days
        return diferencia

    def esta_vencido(self):
        dias = self.dias_para_vencer()
        if dias is None:
            return False
        return dias < 0

    def alerta_vencimiento(self):
        dias = self.dias_para_vencer()
        if dias is None:
            return False
        return 0 <= dias <= 10


# ------------------------------
#      CLASE INVENTARIO
# ------------------------------
class Inventario:
    def __init__(self):
        self.productos = {}
        self.cargar_iniciales()

    def agregar_anio(self, fecha_ddmm):
        """Convierte una fecha dd-mm a dd-mm-aaaa aplicando la regla B."""
        dia, mes = map(int, fecha_ddmm.split("-"))
        hoy = datetime.now()
        anio_actual = hoy.year

        # Si el mes ya pasó este año → año siguiente
        if mes < hoy.month:
            anio = anio_actual + 1
        # Si es el mismo mes pero el día ya pasó → siguiente año
        elif mes == hoy.month and dia < hoy.day:
            anio = anio_actual + 1
        else:
            anio = anio_actual

        return f"{dia:02d}-{mes:02d}-{anio}"

    def cargar_iniciales(self):
        productos_base = [
            ("P001", "Acetaminofén 500mg", 5, 5, "15-12"),
            ("P002", "Ibuprofeno 400mg", 20, 10, "20-12"),
            ("P003", "Omeprazol 20mg", 2, 5, "02-01"),
            ("P004", "Jarabe para la tos", 15, 8, "05-01"),
            ("P005", "Vitamina C 1g", 1, 3, "28-11"),
            ("P006", "Antialérgico Loratadina", 30, 10, "10-12"),
            ("P007", "Crema antibacterial", 12, 5, "25-12"),
            ("P008", "Agua oxigenada", 25, 10, "30-12"),
            ("P009", "Algodón 50g", 18, 5, "18-12"),
            ("P010", "Alcohol antiséptico 70%", 7, 5, "22-12"),
            # Próximos a vencer
            ("P011", "Suero oral", 12, 5, "12-11"),
            ("P012", "Gotas óticas", 8, 3, "15-11"),
            ("P013", "Gasas esterilizadas", 20, 5, "18-11"),
        ]

        for codigo, nombre, cant, stock, fecha in productos_base:
            fecha_completa = self.agregar_anio(fecha)
            self.agregar_producto(
                Producto(codigo, nombre, cant, stock, fecha_completa),
                mostrar_mensaje=False
            )

    def agregar_producto(self, producto, mostrar_mensaje=True):
        if producto.codigo in self.productos:
            if mostrar_mensaje:
                print("El código ya existe.")
            return False

        self.productos[producto.codigo] = producto

        if mostrar_mensaje:
            print(f"✔ Producto '{producto.nombre}' agregado.")
        return True

    def buscar(self, texto):
        texto = texto.lower()
        return [p for p in self.productos.values()
                if texto in p.nombre.lower() or texto in p.codigo.lower()]

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            print("✔ Producto eliminado.")
            return True
        print(" Producto no encontrado.")
        return False

    def obtener_alertas(self):
        stock_bajo = []
        proximos = []
        vencidos = []

        for p in self.productos.values():

            if p.esta_vencido():
                vencidos.append(p)
            elif p.alerta_vencimiento():
                proximos.append(p)

            if p.en_alerta_stock():
                stock_bajo.append(p)

        return stock_bajo, proximos, vencidos

    def mostrar_inventario(self):
        if not self.productos:
            print("Inventario vacío.")
            return

        print("\n--- INVENTARIO ---")
        for p in self.productos.values():
            print(f"{p.codigo} | {p.nombre} | Cantidad: {p.cantidad} | "
                  f"Stock mínimo: {p.stock_minimo} | Vence: {p.fecha_vencimiento}")


# ------------------------------
#      CLASE NOTIFICACIONES
# ------------------------------
class Notificaciones:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_alertas(self):
        hoy = datetime.now()
        print(f"\n  Hoy es: {hoy.day}-{hoy.month}-{hoy.year}")

        stock_bajo, proximos, vencidos = self.inventario.obtener_alertas()

        print("\n---  PRODUCTOS VENCIDOS ---")
        if not vencidos:
            print("No hay productos vencidos.")
        else:
            for p in vencidos:
                print(f"{p.codigo} - {p.nombre} | Vencido el {p.fecha_vencimiento}")

        print("\n--- PRÓXIMOS A VENCER (menos de 10 días) ---")
        if not proximos:
            print("No hay productos próximos a vencer.")
        else:
            for p in proximos:
                dias = p.dias_para_vencer()
                print(f"{p.codigo} - {p.nombre} | Vence en {dias} días ({p.fecha_vencimiento})")

        print("\n---  STOCK BAJO ---")
        if not stock_bajo:
            print("No hay productos con stock bajo.")
        else:
            for p in stock_bajo:
                print(f"{p.codigo} - {p.nombre} | {p.cantidad}/{p.stock_minimo}")


# ------------------------------
#      SISTEMA PRINCIPAL
# ------------------------------
class SistemaDrogueria:
    def __init__(self):
        self.inventario = Inventario()
        self.notificaciones = Notificaciones(self.inventario)

    def menu_principal(self):
        while True:
            print("\n--- MENU PRINCIPAL ---")
            print("1. Ver inventario")
            print("2. Buscar producto")
            print("3. Agregar producto")
            print("4. Eliminar producto")
            print("5. Notificaciones")
            print("6. Salir")

            op = input("Opción: ").strip()

            if op == "1":
                self.inventario.mostrar_inventario()

            elif op == "2":
                texto = input("Buscar por nombre o código: ").strip()
                resultados = self.inventario.buscar(texto)
                print("\n--- RESULTADOS ---")
                if not resultados:
                    print("No se encontraron coincidencias.")
                else:
                    for p in resultados:
                        print(f"{p.codigo} - {p.nombre} | Vence: {p.fecha_vencimiento}")

            elif op == "3":
                codigo = input("Código: ")
                nombre = input("Nombre: ")
                cantidad = input("Cantidad: ")
                stock = input("Stock mínimo: ")
                fecha = input("Fecha vencimiento (dd-mm-aaaa): ")

                self.inventario.agregar_producto(
                    Producto(codigo, nombre, cantidad, stock, fecha)
                )

            elif op == "4":
                codigo = input("Código a eliminar: ")
                self.inventario.eliminar_producto(codigo)

            elif op == "5":
                self.notificaciones.mostrar_alertas()

            elif op == "6":
                print("Saliendo...")
                break

            else:
                print("Opción inválida.")


# ------------------------------
#      EJECUCIÓN
# ------------------------------
if __name__ == "__main__":
    SistemaDrogueria().menu_principal()