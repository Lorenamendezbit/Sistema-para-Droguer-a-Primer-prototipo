from datetime import datetime

class Reserva:
    def __init__(self, id_reserva, cliente, habitacion, fecha_inicio, fecha_fin):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = "activa"

    def modificar_reserva(self, nueva_fecha_inicio, nueva_fecha_fin):
        if self.estado != "activa":
            print("⚠️ No se puede modificar una reserva que no está activa.")
            return
        self.fecha_inicio = nueva_fecha_inicio
        self.fecha_fin = nueva_fecha_fin
        print("✅ Reserva modificada correctamente.")

    def cancelar_reserva(self):
        if self.estado == "cancelada":
            print("⚠️ La reserva ya estaba cancelada.")
        else:
            self.estado = "cancelada"
            print("✅ Reserva cancelada correctamente.")

    def finalizar_reserva(self):
        if self.estado == "activa":
            self.estado = "finalizada"
            print("✅ La reserva ha sido finalizada.")
        else:
            print("⚠️ No se puede finalizar una reserva que no está activa.")