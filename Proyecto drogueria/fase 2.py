from datetime import datetime

# ========================================
#        MODULO DE INVENTARIO
# ========================================

class Producto:
    def _init_(self, codigo, nombre, cantidad, stock_minimo, precio=0, fecha_vencimiento=None):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.stock_minimo = int(stock_minimo)
        self.precio = float(precio) if precio else 0
        self.fecha_vencimiento = fecha_vencimiento

    def en_alerta_stock(self):
        return self.cantidad <= self.stock_minimo

    def obtener_fecha_vencimiento(self):
        if not self.fecha_vencimiento:
            return None
        try:
            return datetime.strptime(self.fecha_vencimiento, "%d-%m-%Y")
        except:
            return None

    def dias_para_vencer(self):
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
    
    def reducir_cantidad(self, cantidad):
        if self.cantidad >= cantidad:
            self.cantidad -= cantidad
            return True
        return False


class Inventario:
    def _init_(self):
        self.productos = {}
        self.cargar_iniciales()

    def agregar_anio(self, fecha_ddmm):
        dia, mes = map(int, fecha_ddmm.split("-"))
        hoy = datetime.now()
        anio_actual = hoy.year

        if mes < hoy.month:
            anio = anio_actual + 1
        elif mes == hoy.month and dia < hoy.day:
            anio = anio_actual + 1
        else:
            anio = anio_actual

        return f"{dia:02d}-{mes:02d}-{anio}"

    def cargar_iniciales(self):
        productos_base = [
            ("P001", "Acetaminofen 500mg", 5, 5, 2500, "15-12"),
            ("P002", "Ibuprofeno 400mg", 20, 10, 3000, "20-12"),
            ("P003", "Omeprazol 20mg", 2, 5, 4500, "02-01"),
            ("P004", "Jarabe para la tos", 15, 8, 12000, "05-01"),
            ("P005", "Vitamina C 1g", 1, 3, 8000, "28-11"),
            ("P006", "Antialergico Loratadina", 30, 10, 5500, "10-12"),
            ("P007", "Crema antibacterial", 12, 5, 15000, "25-12"),
            ("P008", "Agua oxigenada", 25, 10, 3500, "30-12"),
            ("P009", "Algodon 50g", 18, 5, 4000, "18-12"),
            ("P010", "Alcohol antiseptico 70%", 7, 5, 6000, "22-12"),
            ("P011", "Suero oral", 12, 5, 2000, "12-11"),
            ("P012", "Gotas oticas", 8, 3, 18000, "15-11"),
            ("P013", "Gasas esterilizadas", 20, 5, 3500, "18-11"),
        ]

        for codigo, nombre, cant, stock, precio, fecha in productos_base:
            fecha_completa = self.agregar_anio(fecha)
            self.agregar_producto(
                Producto(codigo, nombre, cant, stock, precio, fecha_completa),
                mostrar_mensaje=False
            )

    def agregar_producto(self, producto, mostrar_mensaje=True):
        if producto.codigo in self.productos:
            if mostrar_mensaje:
                print("\033[;31mEl codigo ya existe.\033[0;m")
            return False

        self.productos[producto.codigo] = producto

        if mostrar_mensaje:
            print(f"\033[;32mProducto '{producto.nombre}' agregado.\033[0;m")
        return True

    def buscar(self, texto):
        texto = texto.lower()
        return [p for p in self.productos.values()
                if texto in p.nombre.lower() or texto in p.codigo.lower()]
    
    def buscar_por_codigo(self, codigo):
        return self.productos.get(codigo, None)

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            print("\033[;32mProducto eliminado.\033[0;m")
            return True
        print("\033[;31mProducto no encontrado.\033[0;m")
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
            print("Inventario vacio.")
            return

        print("\n" + "="*90)
        print(" "*35 + "INVENTARIO COMPLETO")
        print("="*90)
        print(f"{'Codigo':<10} {'Nombre':<30} {'Cant':<8} {'Stock Min':<12} {'Precio':<12} {'Vencimiento'}")
        print("-"*90)
        
        for p in self.productos.values():
            print(f"{p.codigo:<10} {p.nombre:<30} {p.cantidad:<8} {p.stock_minimo:<12} ${p.precio:<11.0f} {p.fecha_vencimiento}")
        print("="*90)
    
    def editar_producto(self, codigo):
        if codigo not in self.productos:
            print("\033[;31mProducto no encontrado.\033[0;m")
            return False
        
        p = self.productos[codigo]
        print(f"\nEditando: {p.nombre}")
        print("Deje en blanco para mantener el valor actual")
        
        nuevo_nombre = input(f"Nombre [{p.nombre}]: ").strip()
        nueva_cantidad = input(f"Cantidad [{p.cantidad}]: ").strip()
        nuevo_stock = input(f"Stock minimo [{p.stock_minimo}]: ").strip()
        nuevo_precio = input(f"Precio [{p.precio}]: ").strip()
        nueva_fecha = input(f"Fecha vencimiento [{p.fecha_vencimiento}]: ").strip()
        
        if nuevo_nombre:
            p.nombre = nuevo_nombre
        if nueva_cantidad and nueva_cantidad.isdigit():
            p.cantidad = int(nueva_cantidad)
        if nuevo_stock and nuevo_stock.isdigit():
            p.stock_minimo = int(nuevo_stock)
        if nuevo_precio:
            try:
                p.precio = float(nuevo_precio)
            except:
                pass
        if nueva_fecha:
            p.fecha_vencimiento = nueva_fecha
        
        print("\033[;32mProducto actualizado correctamente.\033[0;m")
        return True


class Notificaciones:
    def _init_(self, inventario):
        self.inventario = inventario

    def mostrar_alertas(self):
        hoy = datetime.now()
        print(f"\n{'='*70}")
        print(f"  Fecha actual: {hoy.day}-{hoy.month}-{hoy.year}")
        print(f"{'='*70}")

        stock_bajo, proximos, vencidos = self.inventario.obtener_alertas()

        print("\n--- PRODUCTOS VENCIDOS ---")
        if not vencidos:
            print("  No hay productos vencidos.")
        else:
            for p in vencidos:
                dias = abs(p.dias_para_vencer())
                print(f"  {p.codigo} - {p.nombre}")
                print(f"     Vencido hace {dias} dias ({p.fecha_vencimiento})")

        print("\n--- PROXIMOS A VENCER (menos de 10 dias) ---")
        if not proximos:
            print("  No hay productos proximos a vencer.")
        else:
            for p in proximos:
                dias = p.dias_para_vencer()
                print(f"  {p.codigo} - {p.nombre}")
                print(f"     Vence en {dias} dias ({p.fecha_vencimiento})")

        print("\n--- STOCK BAJO ---")
        if not stock_bajo:
            print("  No hay productos con stock bajo.")
        else:
            for p in stock_bajo:
                print(f"  {p.codigo} - {p.nombre}")
                print(f"     Cantidad actual: {p.cantidad} | Minimo requerido: {p.stock_minimo}")
        
        print("="*70)
    
    def hay_alertas(self):
        stock_bajo, proximos, vencidos = self.inventario.obtener_alertas()
        return len(stock_bajo) > 0 or len(proximos) > 0 or len(vencidos) > 0