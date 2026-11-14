"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso: Programación 213023 - Fase 4
"""

from models.cliente import Cliente
from models.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from models.reserva import Reserva
from exceptions import (
    ErrorSistemaFJ, ErrorCliente, ErrorServicio, ErrorReserva,
    ErrorValidacion, ServicioNoDisponibleError, ReservaInvalidaError
)
from utils.logger import logger
import traceback

def simular_operaciones():
    print("=" * 70)
    print("  SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIÓN DE OPERACIONES")
    print("=" * 70)

    clientes = []
    servicios = []
    reservas = []

    # ========== OPERACIÓN 1: Cliente válido ==========
    print("\n[1] Registrando cliente válido...")
    try:
        c1 = Cliente("C001", "Ferney Morales", "ferney@email.com", "3001234567")
        c1.validar()
        clientes.append(c1)
        logger.info(f"Cliente registrado: {c1}")
        print(f"  ✓ {c1.descripcion()}")
    except ErrorValidacion as e:
        logger.error(f"Error validación cliente: {e}")
        print(f"  ✗ Error: {e}")

    # ========== OPERACIÓN 2: Cliente inválido (email malo) ==========
    print("\n[2] Intentando registrar cliente con email inválido...")
    try:
        c2 = Cliente("C002", "Ana López", "correo-invalido", "3109876543")
        clientes.append(c2)
    except ErrorValidacion as e:
        logger.error(f"Error al crear cliente: {e}")
        print(f"  ✗ Error controlado: {e}")
    except Exception as e:
        logger.exception("Error inesperado")
        print(f"  ✗ Error inesperado: {e}")

    # ========== OPERACIÓN 3: Otro cliente válido ==========
    print("\n[3] Registrando segundo cliente válido...")
    try:
        c3 = Cliente("C003", "Carlos Ruiz", "carlos.ruiz@empresa.com", "3155551234")
        clientes.append(c3)
        logger.info(f"Cliente registrado: {c3}")
        print(f"  ✓ {c3.descripcion()}")
    except Exception as e:
        logger.error(str(e))
        print(f"  ✗ {e}")

    # ========== OPERACIÓN 4: Servicios válidos ==========
    print("\n[4] Creando servicios...")
    try:
        s1 = ReservaSala("S001", "Sala Ejecutiva A", 80000, capacidad=12)
        s2 = AlquilerEquipo("S002", "Laptop Dell XPS", 45000, tipo_equipo="Computador")
        s3 = AsesoriaEspecializada("S003", "Consultoría en Arquitectura de Software", 120000, especialista="Ing. Pérez")
        servicios.extend([s1, s2, s3])
        for s in servicios:
            logger.info(f"Servicio creado: {s}")
            print(f"  ✓ {s.descripcion()}")
    except ErrorValidacion as e:
        logger.error(str(e))
        print(f"  ✗ {e}")

    # ========== OPERACIÓN 5: Servicio con precio negativo (error) ==========
    print("\n[5] Intentando crear servicio con precio negativo...")
    try:
        s_malo = ReservaSala("S999", "Sala Error", -5000, capacidad=5)
        servicios.append(s_malo)
    except ErrorValidacion as e:
        logger.error(f"Error al crear servicio: {e}")
        print(f"  ✗ Error controlado: {e}")

    # ========== OPERACIÓN 6: Reserva exitosa ==========
    print("\n[6] Creando y confirmando reserva exitosa...")
    try:
        r1 = Reserva("R001", clientes[0], servicios[0], duracion=3)
        r1.confirmar(personas=8, descuento=0.10)  # 10% descuento
        reservas.append(r1)
        logger.info(f"Reserva confirmada: {r1.descripcion()}")
        print(f"  ✓ {r1.descripcion()}")
    except (ErrorReserva, ErrorServicio, ErrorValidacion) as e:
        logger.error(f"Error en reserva: {e}")
        print(f"  ✗ {e}")

    # ========== OPERACIÓN 7: Reserva con más personas que capacidad ==========
    print("\n[7] Intentando reserva con exceso de capacidad...")
    try:
        r2 = Reserva("R002", clientes[0], servicios[0], duracion=2)
        r2.confirmar(personas=20)  # Capacidad es 12
        reservas.append(r2)
    except ErrorServicio as e:
        logger.error(f"Error de capacidad: {e}")
        print(f"  ✗ Error controlado: {e}")
    except Exception as e:
        logger.exception("Error inesperado en reserva")
        print(f"  ✗ {e}")

    # ========== OPERACIÓN 8: Reserva de equipo + try/except/else/finally ==========
    print("\n[8] Reserva de equipo con try/except/else/finally...")
    try:
        r3 = Reserva("R003", clientes[1], servicios[1], duracion=5)
        r3.confirmar(descuento=0.05, seguro=15000)
        reservas.append(r3)
    except (ErrorReserva, ErrorServicio) as e:
        logger.error(f"Fallo en reserva de equipo: {e}")
        print(f"  ✗ Error: {e}")
    else:
        # Solo se ejecuta si NO hubo excepción
        logger.info(f"Reserva de equipo exitosa: {r3.descripcion()}")
        print(f"  ✓ Reserva exitosa (bloque else): {r3.descripcion()}")
    finally:
        # Siempre se ejecuta
        print("  → Bloque finally: limpieza / registro final de la operación 8")

    # ========== OPERACIÓN 9: Servicio no disponible ==========
    print("\n[9] Intentando reservar servicio no disponible...")
    try:
        servicios[2].marcar_no_disponible()
        r4 = Reserva("R004", clientes[0], servicios[2], duracion=2)
        r4.confirmar(urgente=True)
        reservas.append(r4)
    except ServicioNoDisponibleError as e:
        logger.error(f"Servicio no disponible: {e}")
        print(f"  ✗ Error controlado: {e}")
        # Encadenamiento de excepciones
        raise ErrorReserva("No se pudo crear la reserva por servicio no disponible") from e
    except ErrorReserva as e:
        logger.error(f"Error encadenado: {e} | Causa original: {e.__cause__}")
        print(f"  ✗ Error encadenado capturado: {e}")

    # ========== OPERACIÓN 10: Cancelación de reserva ==========
    print("\n[10] Cancelando una reserva...")
    try:
        if reservas:
            resultado = reservas[0].cancelar(motivo="Cambio de planes del cliente")
            logger.info(resultado)
            print(f"  ✓ {resultado}")
            print(f"    Estado actual: {reservas[0].estado.value}")
    except ReservaInvalidaError as e:
        logger.error(str(e))
        print(f"  ✗ {e}")

    # ========== OPERACIÓN 11 (extra): Intentar cancelar de nuevo ==========
    print("\n[11] Intentando cancelar una reserva ya cancelada...")
    try:
        reservas[0].cancelar()
    except ReservaInvalidaError as e:
        logger.warning(f"Operación no permitida: {e}")
        print(f"  ✗ Error controlado: {e}")

    # ========== OPERACIÓN 12 (extra): Completar reserva ==========
    print("\n[12] Completando una reserva confirmada...")
    try:
        # Creamos una nueva para poder completarla
        r5 = Reserva("R005", clientes[1], servicios[1], duracion=2)
        r5.confirmar()
        r5.completar()
        reservas.append(r5)
        logger.info(f"Reserva completada: {r5.descripcion()}")
        print(f"  ✓ {r5.descripcion()}")
    except Exception as e:
        logger.error(str(e))
        print(f"  ✗ {e}")

    # ========== RESUMEN FINAL ==========
    print("\n" + "=" * 70)
    print("  RESUMEN FINAL DEL SISTEMA")
    print("=" * 70)
    print(f"Clientes registrados : {len(clientes)}")
    print(f"Servicios creados    : {len(servicios)}")
    print(f"Reservas gestionadas : {len(reservas)}")
    print("\nDetalle de reservas:")
    for r in reservas:
        print(f"  - {r.descripcion()}")

    print("\n✓ El sistema finalizó sin detenerse ante los errores.")
    print("✓ Todos los eventos y errores quedaron registrados en logs/sistema.log")
    print("=" * 70)


if __name__ == "__main__":
    try:
        simular_operaciones()
    except Exception as e:
        logger.critical(f"Error crítico no controlado: {e}")
        logger.critical(traceback.format_exc())
        print(f"\n¡Error crítico! Revisa el archivo de logs. Detalle: {e}")