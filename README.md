# cxaran-cv

Motor experimental para evolucionar y adaptar un CV en formato YAML usando LLMs, con evaluación automática contra vacantes objetivo.

El proyecto toma un CV base, un perfil fuente con evidencia verificable y una lista de vacantes. A partir de eso genera variantes, las evalúa por ajuste al puesto y conserva la mejor versión para exportarla de nuevo como YAML.

## Que hace

- Carga configuracion, CV semilla, perfil fuente y vacantes desde `input/`.
- Sanitiza el contenido para eliminar campos prohibidos o texto adversarial.
- Genera una poblacion inicial de variantes del CV.
- Evalua cada variante contra una o varias vacantes objetivo.
- Aplica operadores de evolucion como seleccion, crossover y mutacion.
- Exporta el mejor CV encontrado y un reporte final en `output/final/`.

## Estructura del proyecto

```text
.
|-- input/
|   |-- config.yaml
|   |-- seed_cv.yaml
|   |-- source_profile.yaml
|   `-- target_jobs.yaml
|-- output/
|   `-- final/
|-- rendercv_output/
|-- src/
|   |-- main.py
|   |-- engine.py
|   |-- evaluator.py
|   |-- generator.py
|   |-- inference_manager.py
|   |-- sanitizer.py
|   `-- data_models.py
`-- requirements.txt
```

## Requisitos

- Python 3.9 o superior
- Dependencias listadas en `requirements.txt`
- Acceso a un proveedor compatible con la API de OpenAI-compatible que uses en `input/config.yaml`

## Instalacion

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

En macOS o Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuracion

El proyecto usa estos archivos de entrada:

- `input/config.yaml`: proveedor, modelos, restricciones, evolucion y retries.
- `input/seed_cv.yaml`: CV base en formato YAML.
- `input/source_profile.yaml`: fuente factual expandida del candidato.
- `input/target_jobs.yaml`: lista de vacantes objetivo.

### Nota importante sobre la API key

Actualmente `input/config.yaml` contiene `provider.llm_api_key_env`, pero el codigo acepta dos modos:

- El nombre de una variable de entorno, por ejemplo `GROQ_API_KEY`
- La clave pegada directamente en el YAML

La recomendacion es usar una variable de entorno. Ejemplo en PowerShell:

```powershell
$env:GROQ_API_KEY="tu_api_key"
```

Y en `input/config.yaml`:

```yaml
provider:
  llm_provider: groq
  llm_api_base_url: https://api.groq.com/openai/v1
  llm_api_key_env: GROQ_API_KEY
  llm_api_mode: responses_api
```

## Formato esperado de entradas

### `seed_cv.yaml`

Debe contener al menos:

```yaml
cv:
  name: Nombre Apellido
  email: correo@ejemplo.com
  sections:
    resumen_profesional:
      - Texto breve
    experiencia:
      - company: Empresa
        position: Puesto
        highlights:
          - Logro o responsabilidad
design:
  theme: classic
```

### `source_profile.yaml`

Debe funcionar como repositorio factual del candidato. Algunas secciones importantes en el modelo actual:

- `candidate`
- `positioning_profiles`
- `core_summary`
- `experience_expanded`
- `projects_expanded`
- `ats_evidence`

### `target_jobs.yaml`

Debe contener una lista de vacantes con campos como:

- `job_id`
- `title`
- `company`
- `description`
- `requirements`
- `responsibilities`
- `must_have_skills`
- `nice_to_have_skills`
- `keywords_ats`

## Como se ejecuta

Desde la raiz del proyecto:

```bash
python -m src.main
```

Tambien deberia funcionar con:

```bash
python src/main.py
```

## Flujo interno

1. `src/main.py` carga configuracion e inputs.
2. `src/sanitizer.py` limpia contenido sensible o adversarial.
3. `src/inference_manager.py` administra llamadas al proveedor LLM y seleccion de modelos.
4. `src/evaluator.py` puntua cada variante contra las vacantes.
5. `src/generator.py` aplica mutacion y crossover.
6. `src/engine.py` ejecuta el ciclo evolutivo completo.

## Salidas

Al finalizar, el proyecto genera principalmente:

- `output/final/best_cv.yaml`: mejor CV encontrado.
- `output/final/final_report.json`: fitness, scores y trazabilidad basica.

Adicionalmente ya existen artefactos de render en:

- `rendercv_output/`
- `output/final/rendercv_output/`

Eso sugiere una integracion posterior con RenderCV, aunque la generacion de esos archivos no ocurre directamente en `src/main.py`.

## Criterios de evaluacion

El fitness combina tres dimensiones promedio sobre todas las vacantes:

- `job_coverage`
- `ats_match`
- `evidence_density`

Los pesos actuales se definen en `input/config.yaml` dentro de `evaluation`.

## Observaciones tecnicas

- El motor usa seleccion por torneo.
- El crossover mezcla secciones entre dos padres.
- La mutacion actual reescribe secciones como `resumen_profesional` o `experiencia`.
- La mutacion usa como fuente factual principal `experience_expanded`.
- Si no hay modelos disponibles para salida estructurada, la ejecucion puede fallar.

## Recomendaciones

- No guardes claves reales dentro de `input/config.yaml`.
- Excluye `__pycache__/`, salidas generadas y artefactos temporales con `.gitignore`.
- Si vas a adaptar el CV a varias vacantes reales, enriquece `keywords_ats` y `must_have_skills`.
- Manten `source_profile.yaml` como fuente de verdad y evita meter logros inventados en el CV semilla.

## Estado actual

El repositorio ya incluye ejemplos funcionales de entrada y una corrida previa en `output/final/`, lo que facilita usarlo como base para seguir iterando.
