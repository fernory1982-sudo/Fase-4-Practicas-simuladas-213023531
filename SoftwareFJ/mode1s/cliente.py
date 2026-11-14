from models.entidad import Entidad
from exceptions import ErrorCliente, ErrorValidacion
import re

class Cliente(Entidad):
    """Clase Cliente con validaciones robustas y encapsulación"""

    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente)
        self._nombre = None
        self._email = None
        self._telefono = None

        # Usamos los setters para validar
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # ---------- Propiedades con encapsulación y validación ----------
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise ErrorValidacion("El nombre del cliente no puede estar vacío")
        if len(valor.strip()) < 3:
            raise ErrorValidacion("El nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip().title()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor: str):
        if not valor or not str(valor).strip():
            raise ErrorValidacion("El email no puede estar vacío")
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, valor.strip()):
            raise ErrorValidacion(f"Email inválido: {valor}")
        self._email = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).strip():
            raise ErrorValidacion("El teléfono no puede estar vacío")
        # Solo números, mínimo 7 dígitos
        solo_numeros = re.sub(r'\D', '', str(valor))
        if len(solo_numeros) < 7:
            raise ErrorValidacion("El teléfono debe tener al menos 7 dígitos")
        self._telefono = solo_numeros

    def validar(self) -> bool:
        """Valida que el cliente tenga todos los datos correctos"""
        if not all([self._nombre, self._email, self._telefono]):
            raise ErrorCliente("Cliente incompleto: faltan datos obligatorios")
        return True

    def descripcion(self) -> str:
        return f"Cliente {self._nombre} | Email: {self._email} | Tel: {self._telefono}"

    def __str__(self):
        return f"Cliente(id={self.id}, nombre={self._nombre})"