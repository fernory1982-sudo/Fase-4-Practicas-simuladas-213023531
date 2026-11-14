class ErrorSistemaFJ(Exception):
    """Excepción base del sistema Software FJ."""

    def __init__(self, mensaje, codigo_error=None):
        if mensaje is None:
            mensaje = "Error del sistema"

        self.mensaje = str(mensaje)
        self.codigo_error = codigo_error
        super().__init__(self.mensaje, codigo_error)

    def __str__(self):
        if self.codigo_error is not None:
            return f"{self.mensaje} (Código: {self.codigo_error})"
        return self.mensaje

    def __repr__(self):
        return f"{self.__class__.__name__}(mensaje={self.mensaje!r}, codigo_error={self.codigo_error!r})"


class ErrorCliente(ErrorSistemaFJ):
    """Errores relacionados con clientes."""
    pass


class ErrorServicio(ErrorSistemaFJ):
    """Errores relacionados con servicios."""
    pass


class ErrorReserva(ErrorSistemaFJ):
    """Errores relacionados con reservas."""
    pass


class ErrorValidacion(ErrorSistemaFJ):
    """Errores de validación de datos."""
    pass


class ServicioNoDisponibleError(ErrorServicio):
    """Cuando un servicio no está disponible."""
    pass


class ReservaInvalidaError(ErrorReserva):
    """Cuando se intenta una reserva inválida."""
    pass


__all__ = [
    "ErrorSistemaFJ",
    "ErrorCliente",
    "ErrorServicio",
    "ErrorReserva",
    "ErrorValidacion",
    "ServicioNoDisponibleError",
    "ReservaInvalidaError",
]