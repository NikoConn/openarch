#!/usr/bin/env python3

import yaml
import requests
import subprocess
import tempfile
import os
import sys
from datetime import datetime
from pathlib import Path

DOCS_FILE = Path(__file__).parent / "documents.yml"
LASTRUN_FILE = Path(__file__).parent / "lastrun"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "documents"


def load_docs():
    with open(DOCS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_docs(docs):
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        yaml.dump(
            docs,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=200,
        )


def walk_entries(node, path_parts=()):
    """Recursively yield (relative_path, doc_dict) for all entries.
    '_root' keys are skipped in the path (used only for YAML structure)."""
    if isinstance(node, list):
        for doc in node:
            if isinstance(doc, dict) and "name" in doc:
                yield (Path(*path_parts) / f"{doc['name']}.txt", doc)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key == "_root":
                yield from walk_entries(value, path_parts)
            else:
                yield from walk_entries(value, (*path_parts, key))


def get_remote_last_modified(url):
    try:
        resp = requests.head(url, timeout=30, allow_redirects=True)
        resp.raise_for_status()
        return resp.headers.get("Last-Modified")
    except requests.RequestException as e:
        print(f"    ERROR conectando a {url}: {e}", file=sys.stderr)
        return None


def download_and_convert(url, local_path):
    full_path = PROJECT_ROOT / local_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        print(f"    Descargando...")
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        with open(tmp_path, "wb") as f:
            f.write(resp.content)

        print(f"    Convirtiendo a TXT...")
        result = subprocess.run(
            ["pdftotext", tmp_path, str(full_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"    ERROR pdftotext: {result.stderr}", file=sys.stderr)
            return None

        last_modified = resp.headers.get("Last-Modified")
        print(f"    OK")
        return last_modified
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def discover_local_files():
    files = set()
    for txt in DOCS_DIR.rglob("*.txt"):
        files.add(txt.relative_to(DOCS_DIR))
    return files


def main():
    docs = load_docs()
    yaml_paths = set()
    updated = False
    checked = 0
    changed = 0
    no_url = 0
    errors = 0

    print("=== Verificando documentos del YAML ===\n")

    for rel_path, doc in walk_entries(docs):
        yaml_paths.add(rel_path)
        url = doc.get("url")

        if not url:
            print(f"  NO URL  {rel_path}")
            no_url += 1
            continue

        checked += 1
        remote_lm = get_remote_last_modified(url)

        if remote_lm is None:
            errors += 1
            continue

        stored_lm = doc.get("last_modified")

        if stored_lm == remote_lm:
            print(f"  OK      {rel_path}")
            continue

        status = "NEW" if stored_lm is None else "UPD"
        print(f"  {status}    {rel_path}")
        local = str(Path("documents") / rel_path)
        new_lm = download_and_convert(url, local)
        if new_lm:
            doc["last_modified"] = new_lm
            updated = True
            changed += 1
        else:
            errors += 1

    print(f"\n=== Buscando archivos locales no en el YAML ===\n")

    local_files = discover_local_files()
    new_entries = []

    for rel in sorted(local_files):
        if rel in yaml_paths:
            continue

        parts = rel.parts
        name = rel.stem

        print(f"  NUEVO   {rel}")

        node = docs
        for i, part in enumerate(parts[:-1]):
            if part not in node:
                remaining = len(parts) - 1 - i
                if remaining > 1:
                    node[part] = {}
                else:
                    node[part] = []
            if isinstance(node[part], list):
                if i < len(parts) - 2:
                    node[part] = {"_root": node[part]}
                    node = node[part]
                else:
                    node[part].append({
                        "name": name,
                        "url": None,
                        "last_modified": None,
                    })
                    node = None
                    break
            else:
                node = node[part]

        if node is not None and isinstance(node, dict):
            if "_root" in node:
                node["_root"].append({
                    "name": name,
                    "url": None,
                    "last_modified": None,
                })
            else:
                node["_root"] = [{
                    "name": name,
                    "url": None,
                    "last_modified": None,
                }]

        new_entries.append(rel)
        updated = True

    print(f"\n=== Resumen ===")
    print(f"  Comprobados: {checked}")
    print(f"  Actualizados: {changed}")
    print(f"  Sin URL: {no_url}")
    print(f"  Nuevos detectados: {len(new_entries)}")
    print(f"  Errores: {errors}")

    if updated:
        save_docs(docs)
        print("\ndocuments.yml actualizado.")
    else:
        print("\nSin cambios.")

    with open(LASTRUN_FILE, "w", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()}\n")
        f.write(f"checked={checked}\n")
        f.write(f"changed={changed}\n")
        f.write(f"no_url={no_url}\n")
        f.write(f"new_files={len(new_entries)}\n")
        f.write(f"errors={errors}\n")


if __name__ == "__main__":
    main()
