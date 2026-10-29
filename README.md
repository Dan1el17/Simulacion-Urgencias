# 🏥 Simulación de Servicio de Emergencias Hospitalarias

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![SimPy](https://img.shields.io/badge/SimPy-%E2%89%A54.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> **Modelo analítico (red de Jackson + Erlang C) y simulación de eventos discretos para la optimización de personal (médicos y enfermeros) en un servicio de urgencias de 5 etapas.**

---

## 📋 Índice
- [Descripción del proyecto](#-descripción-del-proyecto)
- [Tecnologías utilizadas](#️-tecnologías-utilizadas)
- [Instalación](#-instalación-paso-a-paso)
- [Uso](#-uso)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Resultados y gráficas](#-resultados-y-gráficas)
- [Configuración](#️-configuración)
- [Información adicional](#-información-adicional)

---

## 🩺 Descripción del proyecto

Este proyecto modela un servicio de emergencias hospitalarias como una **red abierta de colas de Jackson con 5 etapas en serie y realimentación**:

`Registro` → `Triaje` → `Consulta` → `Laboratorio` → `Tratamiento`

Resuelve dos problemas reales de gestión hospitalaria:
1. **Identificar cuellos de botella**: ¿En qué etapa se satura el sistema cuando aumenta la demanda? ¿Cuántos médicos ($c_3$) y enfermeros ($c_5$) se necesitan?
2. **Evaluar políticas de atención**: ¿Cuánto se reduce la espera de los pacientes críticos si se atiende por prioridad de gravedad en lugar de orden de llegada (FIFO)?

El proyecto combina dos enfoques complementarios:

| Enfoque | Método | Para qué sirve |
| :--- | :--- | :--- |
| **Analítico** | Red de Jackson + Erlang C (M/M/c) | Barrido rápido de 40 configuraciones $c_3 \times c_5$ |
| **Simulación** | Eventos discretos con SimPy (30 réplicas + IC95%) | Validar el modelo y comparar FIFO vs. prioridad |

### ✨ Hallazgos principales de la última ejecución:
- ✅ **Validación**: La simulación valida al modelo analítico en los 3 escenarios (diferencias < 8% por etapa, dentro del IC95%).
- 🔴 **Saturación**: En el escenario saturado, *Consulta* es el cuello de botella ($\rho$ = 0.514).
- 🚑 **Prioridad**: Con prioridad por gravedad, el paciente crítico espera un **44% menos** (2.7 → 1.5 min) en el escenario saturado.
- 👥 **Personal mínimo**: El personal mínimo estable es 2 médicos + 1 enfermero (W = 50.4 min por paciente).

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Versión | Uso en el proyecto |
| :--- | :--- | :--- |
| **Python** | $\ge$ 3.10 | Lenguaje principal |
| **SimPy** | $\ge$ 4.1 | Motor de simulación de eventos discretos |
| **NumPy** | $\ge$ 1.24 | Cálculo numérico, álgebra lineal (ecuaciones de tráfico) |
| **SciPy** | $\ge$ 1.10 | Erlang C y distribución gamma |
| **Pandas** | $\ge$ 2.0 | Tablas de resultados y exportación CSV |
| **Matplotlib**| $\ge$ 3.7 | Generación de las 9 gráficas (PNG a 300 dpi) |
| **PyYAML** | $\ge$ 6.0 | Lectura de archivos de configuración |
| **Pydantic** | $\ge$ 2.0 | Validación del esquema de configuración |
| **pytest** | $\ge$ 7.0 | Suite de tests unitarios |

---

## 💻 Instalación (paso a paso)

### ✅ Prerrequisitos
- **Python 3.10 o superior** → descárgalo de [python.org](https://www.python.org/)
  - 💡 *En Windows, marca la casilla "Add Python to PATH" durante la instalación.*
  - Verifica la instalación: `python --version`
- **Git** → descárgalo de [git-scm.com](https://git-scm.com/)

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/Dinnel17/Simulacion_servicio_de_emergencias.git
cd Simulacion_servicio_de_emergencias
```
💡 *¿No tienes Git? Alternativa: en GitHub pulsa el botón verde **Code → Download ZIP**, descomprime el archivo y abre una terminal dentro de la carpeta extraída.*

### 2️⃣ Crear y activar un entorno virtual (recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
⚠️ Si PowerShell da un error de permisos (*running scripts is disabled*), ejecuta una sola vez: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` y vuelve a activar el venv.

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```
💡 Verás `(venv)` al inicio de tu terminal cuando esté activado.

### 3️⃣ Instalar las dependencias
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ (Opcional) Ejecutar los tests
```bash
pytest tests/ -v
```
Si todos los tests pasan en verde, tu instalación es correcta ✅

---

## 🚀 Uso

### Corrida completa (la usada para el informe)
Usa por defecto `config/base_parameters.yaml` (30 réplicas, horizonte de 100 h, warm-up de 10 h).

```bash
python -m src.main
```

El programa realiza lo siguiente:
1. Resuelve el barrido analítico de 40 configuraciones ($c_3 \times c_5$).
2. Valida el modelo analítico contra la simulación (FIFO) en los 3 escenarios.
3. Compara FIFO vs. prioridad por gravedad.
4. Busca el personal mínimo estable (W < 120 min).
5. Genera 9 gráficas (3 por escenario) y 4 tablas CSV en la carpeta `output/`.
6. Imprime en consola las Tablas 1–4 y un resumen de lectura rápida por escenario.

### Corrida rápida (para pruebas)
```bash
python -m src.main config/quick_parameters.yaml
```

### Ejemplo de salida en consola
```text
ESCENARIO: SATURADO
Personal.......: 3 medicos (consulta), 3 enfermeros (tratamiento)
Estable........: Si
Cuello botella.: Consulta (rho = 0.514)
W en sistema...: 25.8 min por paciente
Validacion.....: PASO (simulacion confirma al analitico)
Paciente CRITICO: espera FIFO = 2.7 min -> con prioridad = 1.5 min (44% de mejora)

TOTAL DE GRAFICAS GENERADAS: 9 (carpeta output/)
```

### Archivos generados en `output/`
---

## 📂 Estructura del proyecto

```text
Simulacion_servicio_de_emergencias/
├── src/
│   ├── main.py                  # Punto de entrada: orquesta todo el experimento
│   ├── config/
│   │   └── schema.py            # Carga y validación del YAML (Pydantic)
│   ├── models/
│   │   ├── analytical.py        # Red de Jackson + Erlang C (M/M/c)
│   │   └── entities.py          # Patient, StageConfig, SimulationMetrics
│   ├── simulation/
│   │   ├── engine.py            # Motor de simulación SimPy
│   │   ├── statistics.py        # Agregación, IC95% y validación
│   │   ├── patient_generator.py # Llegadas Poisson por nivel de gravedad
│   │   └── priority_strategy.py # Estrategias FIFO / prioridad no expropiativa
│   ├── experiments/
│   │   ├── runner.py            # Ejecución de réplicas y comparaciones
│   │   └── sweep.py             # Barrido c3 × c5 + personal mínimo
│   └── visualization/
│       ├── plots.py             # 9 gráficas (3 por escenario) + tablas CSV
│       └── console_tables.py    # Tablas 1–4 y resumen en consola
├── config/
│   ├── base_parameters.yaml     # Configuración completa (la del informe)
│   ├── quick_parameters.yaml    # Configuración rápida para pruebas
│   └── test_parameters.yaml     # Configuración ultrarrápida para tests
├── tests/                       # Tests unitarios (pytest)
├── output/                      # Gráficas PNG y tablas CSV (generado al correr)
├── requirements.txt             # Dependencias del proyecto
└── pyproject.toml               # Metadatos, licencia y herramientas de dev
```

---

## 📊 Resultados y gráficas

Resultados de la corrida con la configuración base (30 réplicas, IC95%):

| Escenario | Médicos ($c_3$) | Enfermeros ($c_5$) | Cuello de botella | $\rho$ máx | W en sistema | Espera paciente crítico |
| :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| **Saturado** | 3 | 3 | Consulta | 0.514 | 25.8 min | 44% menos con prioridad |
| **Equilibrado** | 5 | 3 | Triaje | 0.356 | 24.3 min | 20% menos con prioridad |
| **Holgado** | 8 | 4 | Triaje | 0.356 | 24.2 min | 25% menos con prioridad |

### Gráficas generadas por escenario

📌 **Nota:** Si ejecutas el código localmente, estas imágenes se generarán en la carpeta `output/`.

| Escenario | Utilización por etapa | Espera vs. nº de médicos | Espera por gravedad |
| :--- | :---: | :---: | :---: |
| Saturado | ![util](output/grafica_utilizacion_saturado.png) | ![esp](output/grafica_espera_vs_medicos_saturado.png) | ![grav](output/grafica_espera_gravedad_saturado.png) |
| Equilibrado | ![util](output/grafica_utilizacion_equilibrado.png) | ![esp](output/grafica_espera_vs_medicos_equilibrado.png) | ![grav](output/grafica_espera_gravedad_equilibrado.png) |
| Holgado | ![util](output/grafica_utilizacion_holgado.png) | ![esp](output/grafica_espera_vs_medicos_holgado.png) | ![grav](output/grafica_espera_gravedad_holgado.png) |

*(Asegúrate de subir la carpeta `output/` a tu repositorio para que las imágenes se visualicen correctamente en GitHub).*

---

## ⚙️ Configuración

Todos los parámetros se editan en los archivos `.yaml` dentro de `config/`. Los principales son:

```yaml
# Llegadas externas por hora (solo a registro, etapa 0)
external_arrivals:
  gamma: [10.0, 0.0, 0.0, 0.0, 0.0]

# Tasas de servicio por hora por servidor (μᵢ)
service_rates:
  mu: [20.0, 15.0, 8.0, 12.0, 10.0]   # registro, triaje, consulta, lab, tratamiento

# Servidores por etapa (c₃ = médicos, c₅ = enfermeros)
servers:
  c: [2, 2, 3, 2, 3]

# % de pacientes por nivel de gravedad (1=crítico ... 5=no urgente)
gravity_levels:
  distribution: [0.05, 0.15, 0.30, 0.35, 0.15]

simulation:
  replications: 30        # réplicas para el IC95%
  horizon_hours: 100      # duración de cada réplica
  warmup_hours: 10        # periodo de calentamiento (no se mide)
  random_seed: 42         # reproducibilidad

parameter_sweep:
  doctors_range: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]   # valores de c₃ a barrer
  nurses_range: [1, 2, 3, 4]                       # valores de c₅ a barrer
  selected_scenarios:                              # escenarios de comparación detallada
    - {c3: 3, c5: 3, label: "saturado"}
    - {c3: 5, c5: 3, label: "equilibrado"}
    - {c3: 8, c5: 4, label: "holgado"}
```

---

## 📚 Información adicional

### Modelo analítico
Red de Jackson abierta con 5 nodos y realimentación (los pacientes pueden volver a consulta desde laboratorio o volver a registro desde tratamiento):

- **Ecuaciones de tráfico:** $\lambda = (I - P^T)^{-1} \cdot \gamma$
- Cada etapa se resuelve como **M/M/c** con fórmula **Erlang C**.
- Métricas por etapa: utilización ($\rho$), espera en cola (Wq), espera total (W), pacientes en cola (Lq) y en sistema (L) — vía **Ley de Little**.
- El **cuello de botella** es la etapa con mayor $\rho$.

### Validación del modelo
La simulación FIFO se compara contra el modelo analítico etapa por etapa: se comprueba que la diferencia relativa sea menor al umbral (5%) y que el valor analítico caiga dentro del IC95% de la simulación. En los 3 escenarios la validación **PASA** ✅.

### Prioridad no expropiativa
Implementada con el patrón **Strategy** sobre `simpy.PriorityResource`: los pacientes de mayor gravedad se posicionan antes en la cola, pero **nunca interrumpen** una atención en curso. Efecto: los críticos y urgentes esperan menos; los leves y no urgentes, un poco más.

### Patrones de diseño aplicados
- **Strategy** — modos de atención (FIFO / prioridad)
- **Factory** — creación de pacientes y estrategias
- **Builder** — construcción de experimentos
- **Observer** — recolección de métricas durante la simulación
- **Template Method** — flujo de procesamiento del paciente
- **Dependency Injection** — toda la configuración vive en YAML externo

---

## 👥 Autores

| Integrante | Rol |
| :--- | :--- |
| Flores Gallardo Emilio Josue | Desarrollo y análisis |
| Pardo Lima Steeven Daniel | Desarrollo y análisis |
| Vega Jimenez Servio Julian | Desarrollo y análisis |
| Valarezo Roman Maria del Cisne | Desarrollo y análisis |

**Nota académica:** Proyecto de la asignatura *Simulación de Sistemas*. Este proyecto fue desarrollado con asistencia de herramientas de IA generativa, conforme a la política del curso.
