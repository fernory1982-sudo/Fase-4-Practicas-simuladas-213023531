from models.entidad import Entidad
from models.cliente import Cliente
from models.servicio import Servicio
from exceptions import ErrorReserva, ReservaInvalidaError, ErrorValidacion
from datetime import datetime
from enum import Enum

class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"


class Reserva(Entidad):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__(id_reserva)

        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Se requiere un objeto Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Se requiere un objeto Servicio válido")
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor a 0")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = EstadoReserva.PENDIENTE
        self._costo_total = 0.0
        self._fecha_confirmacion = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self, **kwargs):
        """Confirma la reserva con manejo de excepciones"""
        if self._estado != EstadoReserva.PENDIENTE:
            raise ReservaInvalidaError(f"No se puede confirmar una reserva en estado: {self._estado.value}")

        # Validar parámetros del servicio (polimorfismo)
        self._servicio.validar_parametros(**kwargs)

        # Calcular costo (polimorfismo + sobrecarga)
        self._costo_total = self._servicio.calcular_costo(self._duracion, **kwargs)
        self._estado = EstadoReserva.CONFIRMADA
        self._fecha_confirmacion = datetime.now()
        return True

    def cancelar(self, motivo: str = "Sin motivo"):
        if self._estado == EstadoReserva.CANCELADA:
            raise ReservaInvalidaError("La reserva ya está cancelada")
        if self._estado == EstadoReserva.COMPLETADA:
            raise ReservaInvalidaError("No se puede cancelar una reserva ya completada")

        self._estado = EstadoReserva.CANCELADA
        return f"Reserva {self.id} cancelada. Motivo: {motivo}"

    def completar(self):
        if self._estado != EstadoReserva.CONFIRMADA:
            raise ReservaInvalidaError("Solo se pueden completar reservas confirmadas")
        self._estado = EstadoReserva.COMPLETADA
        return True

    def validar(self) -> bool:
        self._cliente.validar()
        if self._duracion <= 0:
            raise ErrorValidacion("Duración inválida")
        return True

    def descripcion(self) -> str:
        return (f"Reserva {self.id} | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | Estado: {self._estado.value} | "
                f"Costo: ${self._costo_total:,.0f}")

    def __str__(self):
        return f"Reserva(id={self.id}, estado={self._estado.value})"