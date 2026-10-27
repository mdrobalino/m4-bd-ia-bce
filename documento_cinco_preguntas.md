# Documento de cinco preguntas — TG2
Fecha: 2026-10-27

## 1. ¿Qué proceso automatiza?
El control de un corte mensual de exportaciones: extraer el CSV, validar que lleguen las filas esperadas, que no haya valores vacíos en la columna crítica y que el total coincida con el esperado, y guardar la salida con la fecha del corte.

## 2. ¿Cuál es la fuente y qué pasa si falla?
Fuente: datos/exportaciones.csv (archivo de EJEMPLO; en producción sería el export mensual real del área). Si la fuente no llega o cambia, el flujo se detiene con código 1 y deja el motivo en flujo.log. Avisar al responsable de datos de la unidad y no publicar el corte hasta resolverlo.

## 3. ¿Qué comprobación detiene el proceso?
Tres raises dentro de transformar:  - Si el número de filas no es FILAS_ESPERADAS,  - Si la columna crítica trae valores vacíos,  - Si el total no coincide con TOTAL_ESPERADO.Cada uno deja un ERROR en flujo.log y el script sale con código 1.

## 4. ¿Cuánto tiempo ahorra?
A mano: ~15 minutos por corte (abrir el CSV, contar filas, sumar el total, renombrar el archivo). Con el flujo: menos de 2 segundos, sin intervención, y con registro auditable de cada corrida.

## 5. ¿A quién se avisa si falla y cómo se entera?
Al responsable de datos de la unidad (dueño de las estadísticas). Se entera por el ERROR en flujo.log y por el código de salida 1 del comando; si el flujo corre programado, ese código dispara la alerta del programador de tareas.
