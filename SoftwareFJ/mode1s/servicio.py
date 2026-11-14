from abc import ABC, abstractmethod
from models.entidad import Entidad
from exceptions import ErrorServicio, ErrorValidacion, ServicioNoDisponibleError

class Servicio(Entidad, ABC):
    """Clase abstracta Servicio"""

    def __init__(self, id_servicio: str, nombre: str, precio_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        self._nombre = None
        self._precio_base = None
        self._disponible = disponible

        self.nombre = nombre
        self.precio_base = precio_base

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ErrorValidacion("El nombre del servicio no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ErrorValidacion("El precio base debe ser un número")
        if valor < 0:
            raise ErrorValidacion("El precio base no puede ser negativo")
        self._precio_base = valor

    @property
    def disponible(self):
        return self._disponible

    def marcar_no_disponible(self):
        self._disponible = False

    def marcar_disponible(self):
        self._disponible = True

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto - se sobrescribe en cada servicio (polimorfismo)"""
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs) -> bool:
        """Validación específica de cada tipo de servicio"""
        pass

    def descripcion(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"{self._nombre} | Precio base: ${self._precio_base:,.0f} | {estado}"

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, nombre={self._nombre})"


# ---------- SERVICIO 1: Reserva de Salas ----------
class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, precio_base, disponible)
        if capacidad <= 0:
            raise ErrorValidacion("La capacidad debe ser mayor a 0")
        self._capacidad = capacidad

    def calcular_costo(self, horas: float = 1, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """Método sobrescrito + sobrecarga mediante parámetros opcionales"""
        if horas <= 0:
            raise ErrorValidacion("Las horas deben ser mayores a 0")
        if not 0 <= descuento <= 1:
            raise ErrorValidacion("El descuento debe estar entre 0 y 1")

        subtotal = self._precio_base * horas
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    def validar_parametros(self, personas: int = 1, **kwargs) -> bool:
        if personas <= 0:
            raise ErrorValidacion("El número de personas debe ser mayor a 0")
        if personas > self._capacidad:
            raise ErrorServicio(f"La sala solo admite {self._capacidad} personas")
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La sala '{self._nombre}' no está disponible")
        return True

    def descripcion(self) -> str:
        return f"Sala: {self._nombre} | Capacidad: {self._capacidad} | Precio/hora: ${self._precio_base:,.0f}"


# ---------- SERVICIO 2: Alquiler de Equipos ----------
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float, tipo_equipo: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, precio_base, disponible)
        self._tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int = 1, impuesto: float = 0.19, descuento: float = 0.0, seguro: float = 0.0) -> float:
        """Sobrecarga con parámetro adicional 'seguro'"""
        if dias <= 0:
            raise ErrorValidacion("Los días deben ser mayores a 0")
        subtotal = self._precio_base * dias + seguro
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def validar_parametros(self, **kwargs) -> bool:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El equipo '{self._nombre}' no está disponible")
        return True

    def descripcion(self) -> str:
        return f"Equipo: {self._nombre} ({self._tipo_equipo}) | Precio/día: ${self._precio_base:,.0f}"


# ---------- SERVICIO 3: Asesorías Especializadas ----------
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_base: float, especialista: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, precio_base, disponible)
        self._especialista = especialista

    def calcular_costo(self, horas: float = 1, impuesto: float = 0.19, descuento: float = 0.0, urgente: bool = False) -> float:
        """Sobrecarga con flag 'urgente' que aumenta el precio"""
        if horas <= 0:
            raise ErrorValidacion("Las horas deben ser mayores a 0")
        factor_urgencia = 1.5 if urgente else 1.0
        subtotal = self._precio_base * horas * factor_urgencia
        total = subtotal * (1 - descuento) * (1 + impuesto)
        return round(total, 2)

    def validar_parametros(self, **kwargs) -> bool:
        if not self._disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self._nombre}' no está disponible")
        return True

    def descripcion(self) -> str:
        return f"Asesoría: {self._nombre} | Especialista: {self._especialista} | Precio/hora: ${self._precio_base:,.0f}"