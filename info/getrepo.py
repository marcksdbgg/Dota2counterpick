#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
smart_repo_summary.py

Clona un repo público de GitHub a un directorio temporal y genera
un *único* `.md` de **resumen** (no vuelca toda la base de código).

Incluye:

• Título con el nombre del repo  
• Árbol de carpetas (máx. 2 niveles, carpetas irrelevantes ocultas)  
• Contenido completo de archivos “documentales” clave: README, LICENSE…  
• Fragmentos de código *core* (main.py, index.ts, Dockerfile, etc.)  
  – solo si pesan ≤ MAX_LINES (p.e. 400 líneas)  

No deja archivos residuales.

Uso:

    py smart_repo_summary.py https://github.com/usuario/proyecto [-o salida.md]

Requisitos:
    * Git en PATH
    * Python ≥ 3.8 (sin dependencias extra)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# --------- CONFIGURACIÓN --------------------------------------------------- #

EXCLUDED_DIRS = {
    ".git", "__pycache__", ".venv", ".idea", ".mypy_cache", ".vscode",
    ".github", "node_modules", "dist", "build", ".pytest_cache",
    "test", "tests", "docs", "doc"
}

# Archivos documentales que siempre queremos en su totalidad
DOC_FILES = {
    "README", "README.md", "README.rst", "README.txt",
    "LICENSE", "LICENSE.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md",
    "CHANGELOG.md", "HISTORY.md"
}

# Patrones “core” de código (añade o quita según necesidad)
CORE_PATTERNS = re.compile(
    r"^(main|index|app|server|manage|setup|config)\.[a-z]+$", re.I
)

# Extensiones de texto que se consideran código o config legible
TEXT_EXTS = {
    ".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".java", ".rb",
    ".php", ".c", ".cpp", ".rs", ".sh", ".ps1", ".yml", ".yaml",
    ".toml", ".ini", ".cfg", ".conf", ".json", ".env", ".md", ".rst",
    ".dockerfile", "Dockerfile"
}

# Máximo de líneas que incluiremos de un archivo de código grande
MAX_LINES = 400

# Profundidad máxima a mostrar en el árbol
TREE_DEPTH = 2


# --------- UTILIDADES GENERALES ------------------------------------------- #
def run(cmd: list[str] | str, cwd: Path | None = None) -> None:
    """Ejecuta un comando y detiene todo el script si falla."""
    try:
        subprocess.run(cmd, cwd=cwd, check=True, text=True)
    except FileNotFoundError:
        sys.exit(f"[ERROR] Comando no encontrado: {cmd[0]!r}. "
                 "Instala Git y/o añádelo al PATH.")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"[ERROR] {' '.join(cmd)} falló con código {exc.returncode}.")


def is_text_file(path: Path) -> bool:
    if path.is_dir():
        return False
    if path.suffix.lower() in TEXT_EXTS or path.name in TEXT_EXTS:
        try:
            path.read_text(encoding="utf-8")
            return True
        except UnicodeDecodeError:
            return False
    return False


def build_tree(directory: Path, depth: int = 0, prefix: str = "") -> list[str]:
    """Árbol recursivo limitado por `TREE_DEPTH`."""
    if depth >= TREE_DEPTH:
        return []
    entries = sorted(
        [e for e in directory.iterdir() if e.name not in EXCLUDED_DIRS],
        key=lambda e: (not e.is_dir(), e.name.lower())
    )
    lines: list[str] = []
    for idx, entry in enumerate(entries, 1):
        connector = "└── " if idx == len(entries) else "├── "
        lines.append(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            spacer = "    " if idx == len(entries) else "│   "
            lines.extend(build_tree(entry, depth + 1, prefix + spacer))
    return lines


def should_include(path: Path) -> bool:
    """Solo incluye archivos .md para el volcado de contenido."""
    if path.suffix.lower() == ".md":
        return True
    return False


# --------- GENERADOR DE MARKDOWN ------------------------------------------ #
def generate_markdown(repo_root: Path, output_path: Path, repo_title: str) -> None:
    lines: list[str] = [f"# {repo_title} — Resumen de Codebase", ""]

    # 1) Árbol de carpetas
    lines += ["## Estructura (hasta 2 niveles)", "", "```"]
    lines += [f"{repo_root.name}/"]
    lines += build_tree(repo_root)
    lines += ["```", ""]

    # 2) Archivos seleccionados
    for path in sorted(repo_root.rglob("*")):
        rel_parts = path.relative_to(repo_root).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue
        if not should_include(path):
            continue

        rel_display = "/".join(rel_parts)
        lang = path.suffix.lstrip(".")
        lines += [f"### `{rel_display}`"]

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            lines += [f"_[No se pudo leer: {exc}]_", ""]
            continue

        if len(content.splitlines()) > MAX_LINES:
            content = "\n".join(content.splitlines()[:MAX_LINES]) + \
                      "\n... (truncado)\n"

        lines += [f"```{lang}", content, "```", ""]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Resumen escrito en {output_path}")


# --------- PUNTO DE ENTRADA ------------------------------------------------ #
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera un Markdown con lo esencial de un repositorio GitHub."
    )
    parser.add_argument("repo_url", help="URL HTTPS del repo GitHub")
    parser.add_argument(
        "-o", "--output", default="repo_summary.md",
        help="Nombre del archivo de salida (default: repo_summary.md)"
    )
    args = parser.parse_args()

    output_file = Path.cwd() / args.output
    repo_name = args.repo_url.rstrip("/").split("/")[-1].replace(".git", "")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        print(f"[INFO] Clonando {args.repo_url} …")
        run(["git", "clone", "--depth", "1", args.repo_url, "."], cwd=tmp)

        # Detecta raíz real si el repo contiene un único subdirectorio
        root = tmp
        items = list(root.iterdir())
        if len([p for p in items if p.is_dir()]) == 1 and \
           not any(p.is_file() for p in items):
            root = [p for p in items if p.is_dir()][0]

        print("[INFO] Generando resumen …")
        generate_markdown(root, output_file, repo_name)

    print("[INFO] Directorio temporal limpiado. Fin.")


if __name__ == "__main__":
    main()
