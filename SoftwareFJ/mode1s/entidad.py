from abc import ABC, abstractmethod
from datetime import datetime

class Entidad(ABC):
    """Clase abstracta que representa entidades generales del sistema"""

    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise ValueError("El ID de la entidad no puede estar vacío")
        self._id = str(id_entidad).strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que deben implementar las clases hijas"""
        pass

    @abstractmethod
    def descripcion(self) -> str:
        """Método abstracto para obtener descripción de la entidad"""
        pass

    def __str__(self):
        return f"{self.__class__.__name__}(id={self._id})"