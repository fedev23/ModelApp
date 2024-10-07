import datetime
from shiny import reactive


class ProcesTime:
    def __init__(self):
        self.fechaHora = reactive.Value(None)

    def set_fecha_desarrollo(self, fecha_hora):
        # Actualiza el valor de fechaHora usando el método set()
        self.fechaHora.set(fecha_hora)

    def get_fecha_desarrollo(self):
        return self.fechaHora.get()

    def set_fecha(self, fecha_hora):
        # Actualiza el valor de fechaHora usando el método set()
        self.fechaHora.set(fecha_hora)

    def get_fecha(self):
        return self.fechaHora.get()


global_fecha = ProcesTime()
