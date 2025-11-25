from datetime import datetime
# ========================================
#        MODULO DE VENTAS
# ========================================

class Factura:
    contador_facturas = 1000
    
    def _init_(self, cliente=None):
        Factura.contador_facturas += 1
        self.numero_factura = Factura.contador_facturas
        self.items = []
        self.cliente = cliente
        self.fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    def agregar_item(self, codigo, nombre, cantidad, precio):
        subtotal = cantidad * precio
        self.items.append((codigo, nombre, cantidad, precio, subtotal))
    
    def calcular_total(self):
        total = 0
        for _, _, _, _, subtotal in self.items:
            total += subtotal
        return total
    
    def generar_factura(self):
        print("\n" + "="*80)
        print(" "*30 + "FACTURA DE VENTA")
        print("="*80)
        print(f"Factura No: {self.numero_factura}")
        print(f"Fecha: {self.fecha}")
        
        if self.cliente:
            print(f"Cliente: {self.cliente.nombre}")
            print(f"Documento: {self.cliente.documento}")
        else:
            print("Cliente: General")
        
        print("-"*80)
        print(f"{'Codigo':<10} {'Producto':<35} {'Cant':<8} {'P.Unit':<12} {'Subtotal'}")
        print("-"*80)
        
        if not self.items:
            print("No hay productos agregados.")
        else:
            for codigo, nombre, cantidad, precio, subtotal in self.items:
                print(f"{codigo:<10} {nombre:<35} {cantidad:<8} ${precio:<11.0f} ${subtotal:.0f}")
        
        print("-"*80)
        print(f"{'TOTAL A PAGAR:':<66} ${self.calcular_total():.0f}")
        print("="*80)
    
    def _str_(self):
        cliente_nombre = self.cliente.nombre if self.cliente else "General"
        return f"Factura #{self.numero_factura} | {self.fecha} | Cliente: {cliente_nombre} | Total: ${self.calcular_total():.0f}"


class SistemaVentas:
    def _init_(self, inventario, gestion_clientes):
        self.inventario = inventario
        self.gestion_clientes = gestion_clientes
        self.historial_ventas = []
    
    def realizar_venta(self):
        print("\n" + "="*80)
        print(" "*32 + "NUEVA VENTA")
        print("="*80)
        
        tiene_cliente = input("El cliente esta registrado? (s/n): ").lower()
        cliente = None
        
        if tiene_cliente == 's':
            doc_cliente = input("Ingrese el documento del cliente: ")
            cliente = self.gestion_clientes.buscar_cliente(doc_cliente)
            if not cliente:
                print("\033[;31mCliente no encontrado. Se procesara como venta general.\033[0;m")
        
        factura = Factura(cliente)
        
        print("\nAgregue productos a la factura (escriba 'fin' para terminar)")
        
        while True:
            print("\n" + "-"*50)
            codigo = input("Codigo del producto (o 'fin' para terminar): ").strip()
            
            if codigo.lower() == 'fin':
                break
            
            producto = self.inventario.buscar_por_codigo(codigo)
            
            if not producto:
                print("\033[;31mProducto no encontrado.\033[0;m")
                continue
            
            print(f"\nProducto: {producto.nombre}")
            print(f"Precio: ${producto.precio}")
            print(f"Disponible: {producto.cantidad} unidades")
            
            try:
                cantidad = int(input("Cantidad a vender: "))
                
                if cantidad <= 0:
                    print("\033[;31mLa cantidad debe ser mayor a 0.\033[0;m")
                    continue
                
                if cantidad > producto.cantidad:
                    print(f"\033[;31mStock insuficiente. Solo hay {producto.cantidad} unidades.\033[0;m")
                    continue
                
                if producto.reducir_cantidad(cantidad):
                    factura.agregar_item(
                        producto.codigo,
                        producto.nombre,
                        cantidad,
                        producto.precio
                    )
                    print(f"\033[;32mProducto agregado a la factura.\033[0;m")
                else:
                    print("\033[;31mError al reducir el stock.\033[0;m")
                    
            except ValueError:
                print("\033[;31mCantidad invalida.\033[0;m")
        
        if not factura.items:
            print("\n\033[;33mNo se agregaron productos. Venta cancelada.\033[0;m")
            return False
        
        factura.generar_factura()
        
        confirmar = input("\nConfirmar venta? (s/n): ").lower()
        
        if confirmar == 's':
            self.historial_ventas.append(factura)
            print("\033[;32mVenta registrada exitosamente.\033[0;m")
            return True
        else:
            for codigo, _, cantidad, _, _ in factura.items:
                producto = self.inventario.buscar_por_codigo(codigo)
                if producto:
                    producto.cantidad += cantidad
            print("\033[;33mVenta cancelada. Stock restaurado.\033[0;m")
            return False
    
    def ver_historial_ventas(self):
        if not self.historial_ventas:
            print("\n\033[;33mNo hay ventas registradas.\033[0;m")
            return
        
        print("\n" + "="*90)
        print(" "*35 + "HISTORIAL DE VENTAS")
        print("="*90)
        
        total_general = 0
        for factura in self.historial_ventas:
            print(factura)
            total_general += factura.calcular_total()
        
        print("="*90)
        print(f"Total de ventas: {len(self.historial_ventas)}")
        print(f"Ingresos totales: ${total_general:.0f}")
        print("="*90)
    
    def ver_detalle_factura(self):
        if not self.historial_ventas:
            print("\n\033[;33mNo hay facturas registradas.\033[0;m")
            return
        
        try:
            num_factura = int(input("Ingrese el numero de factura: "))
            
            for factura in self.historial_ventas:
                if factura.numero_factura == num_factura:
                    factura.generar_factura()
                    return
            
            print("\033[;31mFactura no encontrada.\033[0;m")
        except ValueError:
            print("\033[;31mNumero de factura invalido.\033[0;m")
    
    def generar_estadisticas(self):
        if not self.historial_ventas:
            print("\n\033[;33mNo hay ventas para generar estadisticas.\033[0;m")
            return
        
        print("\n" + "="*80)
        print(" "*28 + "ESTADISTICAS DE VENTAS")
        print("="*80)
        
        total_ventas = len(self.historial_ventas)
        ingresos_totales = sum(f.calcular_total() for f in self.historial_ventas)
        promedio_venta = ingresos_totales / total_ventas if total_ventas > 0 else 0
        
        productos_vendidos = {}
        for factura in self.historial_ventas:
            for codigo, nombre, cantidad, _, _ in factura.items:
                if codigo not in productos_vendidos:
                    productos_vendidos[codigo] = {"nombre": nombre, "cantidad": 0}
                productos_vendidos[codigo]["cantidad"] += cantidad
        
        print(f"\nResumen General:")
        print(f"   Total de ventas realizadas: {total_ventas}")
        print(f"   Ingresos totales: ${ingresos_totales:.0f}")
        print(f"   Promedio por venta: ${promedio_venta:.0f}")
        
        print(f"\nProductos mas vendidos:")
        productos_ordenados = sorted(
            productos_vendidos.items(),
            key=lambda x: x[1]["cantidad"],
            reverse=True
        )
        
        for i, (codigo, data) in enumerate(productos_ordenados[:5], 1):
            print(f"   {i}. {data['nombre']} ({codigo}): {data['cantidad']} unidades")
        
        print("="*80)
