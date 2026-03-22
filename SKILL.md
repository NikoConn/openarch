---
name: openarch
description: >
  Consult Spanish building regulations (CTE, GVA).
  Search legal requirements and updated documents from official sources.
metadata:
  {
    "openclaw": {
      "emoji": "👷🏻‍♀️",
      "requires": {
        "bins": ["rg", "git"]
      }
    }
  }
---

# openarch repository

Repository for consulting architecture regulations (CTE, GVA) and managing technical documentation.

## Available documents

All in `{baseDir}/documents/` in TXT format:

### CTE
- **SE** (Structural Safety): `documents/CTE - Codigo tecnico/SE/`
- **SI** (Fire Safety): `documents/CTE - Codigo tecnico/SI/`
- **SUA** (Accessibility): `documents/CTE - Codigo tecnico/SUA/`
- **HE** (Energy Saving): `documents/CTE - Codigo tecnico/HE/`
- **HR** (Noise Protection): `documents/CTE - Codigo tecnico/HR/`
- **HS** (Health): `documents/CTE - Codigo tecnico/HS/`

### GVA
- `documents/GVA/DECRETO 65-2019.txt`
- `documents/GVA/plan-general-ordenacion-urbana.txt`

## Search regulations

Use `rg` to search for key terms in the documents:
```bash
rg -i "<term>" "{baseDir}/documents/<path>"
```

To read specific line ranges:
```bash
sed -n '<start>,<end>p' "{baseDir}/documents/<path>"
```

Always cite the source (document, section, clause).

## Update documents

To update documents to the latest available version:
```bash
git -C {baseDir} pull
```
