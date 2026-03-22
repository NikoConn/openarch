# openarch

Base de conocimiento para asistentes de IA en redacción de documentación técnica de arquitectura.

## Qué es esto

Este repositorio sirve como base de conocimiento para cualquier agente de IA (opencode, OpenClaw, etc.), de modo que pueda consultar la normativa vigente (CTE, normativa GVA, etc.) mientras se redactan proyectos, memoriales, informes u otros documentos técnicos.

Incluye un archivo `SKILL.md` compatible con [AgentSkills](https://agentskills.io) para uso directo como skill en OpenClaw.

## Cómo funciona

Los documentos normativos están convertidos a texto plano en la carpeta `documents/`. El agente busca directamente en estos archivos y devuelve la información relevante con la referencia al documento y apartado correspondiente.

### Documentos disponibles

**CTE - Código Técnico de la Edificación:**

- **SE** — Seguridad estructural (DB-SE, DB-SE-A, DB-SE-AE, DB-SE-C, DB-SE-F, DB-SE-M)
- **SI** — Seguridad en caso de incendio (DB-SI, Dcm-SI, Dcc-SI, documentos aportados)
- **SUA** — Seguridad de utilización y accesibilidad (DB-SUA, Dcm-SUA, Dcc-SUA, documentos aportados)
- **HE** — Ahorro de energía (DB-HE, guías de aplicación, documentos aportados)
- **HR** — Protección frente al ruido (DB-HR, Dcc-HR, guía DB-HR, IEE)
- **HS** — Salubridad (DB-HS, Dcm-HS, Dcc-HS, guía de rehabilitación frente al radón)

**Normativa autonómica (GVA):**

- Decreto 65/2019
- Plan General de Ordenación Urbana

## Uso como skill (OpenClaw)

```bash
git clone <repo> ~/.openclaw/skills/openarch
```

Para actualizar los documentos:

```bash
git -C ~/.openclaw/skills/openarch pull
```

## Uso con opencode

Lanza opencode en este repositorio y pregúntale cosas como:

- "¿Qué requisitos tiene el DB-HE para la demanda energética de calefacción?"
- "Resume los apartados del DB-SI sobre compartimentación en incendios"
- "¿Qué dice la guía de radón sobre la solución de despresurización del terreno?"
- "Redacta un justificante de cumplimiento del DB-SUA para un edificio de vivienda"
- "¿Cuáles son los límites de aislamiento acústico del DB-HR para fachadas?"

## Edición de documentos con Python

Los agentes pueden leer y modificar documentos usando Python con las librerías `python-docx` (Word) y `openpyxl` (Excel). El entorno virtual debe tener instaladas las dependencias necesarias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-docx openpyxl requests pyyaml
```

## Aspectos técnicos

Los documentos se actualizan automáticamente mediante GitHub Actions (diariamente) o manualmente:

```bash
source .venv/bin/activate && python3 scripts/doc-updater/update.py
```

El script compara la fecha de modificación de los PDFs originales con la almacenada en `scripts/doc-updater/documents.yml` y actualiza los archivos TXT si hay cambios.

## Estructura

```
openarch/
├── documents/                    # Documentos normativos en texto plano
│   ├── CTE - Codigo tecnico/    # CTE por documento básico
│   │   ├── SE/
│   │   ├── SI/
│   │   ├── SUA/
│   │   ├── HE/
│   │   ├── HR/
│   │   └── HS/
│   └── GVA/                     # Normativa autonómica
├── scripts/doc-updater/         # Script de actualización de documentos
│   ├── update.py
│   └── documents.yml            # Configuración de documentos y URLs
├── AGENTS.md                    # Instrucciones para agentes
└── SKILL.md                     # AgentSkills
```

## Nota sobre Revit

Creo que este enfoque tiene mucho potencial si se combina con [mcp-servers-for-revit](https://github.com/mcp-servers-for-revit), lo que permitiría a los agentes consultar datos directamente del modelo de Revit (superficies, materiales, tipologías, etc.) para generar documentación basada en datos reales del proyecto. Sin embargo, no tengo claro que los modelos actuales tengan la suficiente capacidad para manejar correctamente esa conexión y extraer los datos que el usuario necesite de forma fiable.
