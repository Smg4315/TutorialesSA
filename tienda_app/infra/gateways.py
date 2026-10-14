import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float) -> bool:

        archivo_log = "pagos_locales_SIMON_MAZO.log" 

        # Simulamos una operación de red o persistencia externa
        with open("pagos_locales_SIMON_MAZO.log", "a") as f:
            f.write(f"[{datetime.datetime.now()}] BANCO NACIONAL - Cobro procesado: ${monto}\n")
        return True

