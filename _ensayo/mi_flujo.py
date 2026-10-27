"""Flujo de control de exportaciones: extrae el CSV, valida filas y total, y guarda el resultado del corte. 
Integrantes: Maria Dolores Robalino
Fuente: datos/exportaciones.csv (si es un archivo de EJEMPLO, digalo aqui)
SI FALLA: si la fuente no llega o cambia (faltan filas, cambia el total o aparece una columna vacía),
el flujo se detiene con código 1 y deja el motivo en flujo.log. Avisar al responsable de datos
de la unidad y no publicar el corte hasta resolverlo."""

import logging, sys
from datetime import date
import pandas as pd

# ---------- 1 · PARAMETROS (todo lo que puede cambiar, junto y arriba) ----------
RUTA_ENTRADA    = "datos/exportaciones.csv"
SALIDA          = f"salida/mi_flujo_{date.today().isoformat()}.csv"
FILAS_ESPERADAS = 7
TOTAL_ESPERADO  = 8679.13
COLUMNA_CRITICA = "producto"
# agregue aqui otro parametro de comprobacion, por ejemplo un total esperado

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler("flujo.log"), logging.StreamHandler()])
log = logging.getLogger("mi_flujo")

# ---------- 2 · LAS TRES FUNCIONES (cada una con su docstring) ----------
def extraer():
    """Lee el CSV de entrada y devuelve la tabla cruda, registrando cuántas filas llegaron."""
    tabla = pd.read_csv(RUTA_ENTRADA)
    log.info("extraidas %d filas", len(tabla))
    return tabla

def transformar(tabla):
    """Valida filas y total esperado, y devuelve la tabla lista para cargar; detiene si algo no cuadra."""
    if len(tabla) != FILAS_ESPERADAS:
        raise ValueError(f"esperaba {FILAS_ESPERADAS} filas y llegaron {len(tabla)}")
    if COLUMNA_CRITICA in tabla.columns and tabla[COLUMNA_CRITICA].isna().any():
        raise ValueError(f"la columna {COLUMNA_CRITICA} trae valores vacios")
    col_monto = [c for c in tabla.columns if c.lower() in ("monto", "valor", "total")]
    if col_monto:
        total = float(tabla[col_monto[0]].sum())
        if round(total, 2) != round(TOTAL_ESPERADO, 2):
            raise ValueError(f"el total cambio: esperaba {TOTAL_ESPERADO} y salio {round(total,2)}")
        log.info("total validado: %.2f", total)
    log.info("transformacion OK (%d filas)", len(tabla))
    return tabla

def cargar(tabla):
    """Guarda la tabla transformada en salida/ con la fecha del corte en el nombre."""
    import os; os.makedirs("salida", exist_ok=True)
    tabla.to_csv(SALIDA, index=False)
    log.info("guardado %s (%d filas)", SALIDA, len(tabla))

# ---------- 3 · LA LOGICA, EN ORDEN ----------
if __name__ == "__main__":
    try:
        cargar(transformar(extraer())); log.info("FIN OK")
    except Exception as error:
        log.error("EL FLUJO FALLO: %s", error); sys.exit(1)
