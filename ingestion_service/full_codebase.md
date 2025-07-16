# Estructura de la Codebase

```
app/
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       └── endpoints
│   │           └── __init__.py
│   ├── application
│   │   ├── __init__.py
│   │   ├── ports
│   │   │   └── __init__.py
│   │   └── use_cases
│   │       └── __init__.py
│   ├── core
│   │   └── __init__.py
│   ├── domain
│   │   └── __init__.py
│   ├── infrastructure
│   │   ├── __init__.py
│   │   ├── kafka
│   │   │   └── __init__.py
│   │   └── match_stream
│   │       └── __init__.py
│   └── utils
│       └── __init__.py
└── export_codebase.py
```

# Codebase: `app`

## File: `app\__init__.py`
```py

```

## File: `app\api\__init__.py`
```py

```

## File: `app\api\v1\__init__.py`
```py

```

## File: `app\api\v1\endpoints\__init__.py`
```py

```

## File: `app\application\__init__.py`
```py

```

## File: `app\application\ports\__init__.py`
```py

```

## File: `app\application\use_cases\__init__.py`
```py

```

## File: `app\core\__init__.py`
```py

```

## File: `app\domain\__init__.py`
```py

```

## File: `app\infrastructure\__init__.py`
```py

```

## File: `app\infrastructure\kafka\__init__.py`
```py

```

## File: `app\infrastructure\match_stream\__init__.py`
```py

```

## File: `app\utils\__init__.py`
```py

```

## File: `export_codebase.py`
```py
from pathlib import Path

# Carpetas que queremos excluir dentro de /app
EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', '.idea', '.mypy_cache', '.vscode', '.github', 'node_modules'}

def build_tree(directory: Path, prefix: str = "") -> list:
    """
    Genera una representación en árbol de la estructura de directorios y archivos,
    excluyendo las carpetas especificadas en EXCLUDED_DIRS.
    """
    # Filtrar y ordenar los elementos del directorio
    entries = sorted(
        [entry for entry in directory.iterdir() if entry.name not in EXCLUDED_DIRS],
        key=lambda e: e.name
    )
    tree_lines = []
    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        tree_lines.append(prefix + connector + entry.name)
        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            tree_lines.extend(build_tree(entry, prefix + extension))
    return tree_lines

def generate_codebase_markdown(base_path: str = ".", output_file: str = "full_codebase.md"):
    base = Path(base_path).resolve()
    app_dir = base

    if not app_dir.exists():
        print(f"[ERROR] La carpeta 'app' no existe en {base}")
        return

    lines = []

    # Agregar la estructura de directorios al inicio del Markdown
    lines.append("# Estructura de la Codebase")
    lines.append("")
    lines.append("```")
    lines.append("app/")
    tree_lines = build_tree(app_dir)
    lines.extend(tree_lines)
    lines.append("```")
    lines.append("")

    # Agregar el contenido de la codebase en Markdown
    lines.append("# Codebase: `app`")
    lines.append("")

    # Recorrer solo la carpeta app
    for path in sorted(app_dir.rglob("*")):
        # Ignorar directorios excluidos
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if path.is_file():
            rel_path = path.relative_to(base)
            lines.append(f"## File: `{rel_path}`")
            try:
                content = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                lines.append("_[Skipped: binary or non-UTF8 file]_")
                continue
            except Exception as e:
                lines.append(f"_[Error al leer el archivo: {e}]_")
                continue
            ext = path.suffix.lstrip('.')
            lang = ext if ext else ""
            lines.append(f"```{lang}")
            lines.append(content)
            lines.append("```")
            lines.append("")

    # Agregar pyproject.toml si existe en la raíz
    toml_path = base / "pyproject.toml"
    if toml_path.exists():
        lines.append("## File: `pyproject.toml`")
        try:
            content = toml_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            lines.append("_[Skipped: binary or non-UTF8 file]_")
        except Exception as e:
            lines.append(f"_[Error al leer el archivo: {e}]_")
        else:
            lines.append("```toml")
            lines.append(content)
            lines.append("```")
            lines.append("")

    output_path = base / output_file
    try:
        output_path.write_text("\n".join(lines), encoding='utf-8')
        print(f"[OK] Código exportado a Markdown en: {output_path}")
    except Exception as e:
        print(f"[ERROR] Error al escribir el archivo de salida: {e}")

# Si se corre el script directamente
if __name__ == "__main__":
    generate_codebase_markdown()

```
