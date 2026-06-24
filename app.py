"""
=====================================================================
 Agenda para Múltiples Profesionales
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_agenda_multiple_profesionales_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Agenda para Múltiples Profesionales."""

    def __init__(self, citas, profesionales, horas):
        self.citas = float(citas)
        self.profesionales = float(profesionales)
        self.horas = float(horas)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        if self.profesionales == 0:
            return {"error": "Debe haber al menos 1 profesional."}
        por_profesional = self.citas / self.profesionales
        minutos_disponibles = self.horas * 60 * self.profesionales
        min_por_cita = minutos_disponibles / self.citas if self.citas > 0 else 0
        return {"por_profesional": por_profesional, "min_por_cita": min_por_cita}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["min_por_cita"] < 15:
            return "⚠️ Muy poco tiempo por cita (<15min)."
        return "✅ Distribución viable."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("citas"), input_float("profesionales"), input_float("horas"))
    r = c.calcular()
    if "error" in r:
        mostrar(f'❌ {r["error"]}', clase="is-error"); return
    html = f"""
      <div class="result-value">👥 {r["por_profesional"]:.1f} citas/profesional</div>
      <p class="result-detail">~{fmt_num(r["min_por_cita"])} min por cita · {c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "citas": input_float("citas"),
            "profesionales": input_float("profesionales"),
            "horas": input_float("horas"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "citas" in datos:
            document.querySelector("#citas").value = datos["citas"]
        if "profesionales" in datos:
            document.querySelector("#profesionales").value = datos["profesionales"]
        if "horas" in datos:
            document.querySelector("#horas").value = datos["horas"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
