#!/usr/bin/env python3
"""Revisión rápida del portafolio antes de hacer commit.

Uso (desde la carpeta del proyecto):
    python scripts/check.py            # revisión local
    python scripts/check.py --online   # además prueba que los enlaces externos respondan
    python scripts/check.py --strict   # los pendientes (TU_...) también cuentan como error

En Windows, si "python" no funciona, usa: py scripts/check.py
Solo usa la biblioteca estándar de Python: no hay que instalar nada.
Nunca imprime el valor de un posible secreto, solo el archivo y el tipo.
"""

import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXT = {".html", ".css", ".js", ".md", ".json", ".txt", ".py", ".svg", ".yml", ".yaml"}
SKIP_DIRS = {".git", "node_modules", ".vercel"}

results = []  # (nivel, mensaje)


def ok(msg):
    results.append(("OK", msg))


def warn(msg):
    results.append(("AVISO", msg))


def fail(msg):
    results.append(("ERROR", msg))


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_lang = None
        self.title = ""
        self._in_title = False
        self.metas = {}
        self.ids = []
        self.hrefs = []
        self.srcs = []
        self.imgs_without_alt = 0
        self.blank_without_noopener = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.metas[key] = a.get("content", "")
        if "id" in a:
            self.ids.append(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.hrefs.append(a["href"])
            if tag == "a" and a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
                self.blank_without_noopener.append(a["href"])
        if tag in ("script", "img", "source") and a.get("src"):
            self.srcs.append(a["src"])
        if tag == "img" and a.get("alt") is None:
            self.imgs_without_alt += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def check_files():
    for name in ("index.html", "styles.css", "script.js", "README.md", ".gitignore"):
        (ok if (ROOT / name).exists() else fail)(f"Existe {name}" if (ROOT / name).exists() else f"Falta {name}")


def check_html():
    path = ROOT / "index.html"
    if not path.exists():
        return None
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))

    (ok if parser.html_lang else fail)("<html lang> definido" if parser.html_lang else "Falta lang en <html>")
    (ok if parser.title.strip() else fail)("Tiene <title>" if parser.title.strip() else "Falta <title>")
    has_desc = bool(parser.metas.get("description"))
    (ok if has_desc else fail)("Tiene meta description" if has_desc else "Falta meta description")
    has_vp = "width=device-width" in parser.metas.get("viewport", "")
    (ok if has_vp else fail)("Tiene meta viewport (adaptable a móvil)" if has_vp else "Falta meta viewport")

    h1s = parser.headings.count(1)
    (ok if h1s == 1 else fail)("Un solo <h1>" if h1s == 1 else f"Debe haber un <h1>, hay {h1s}")
    skips = [(a, b) for a, b in zip(parser.headings, parser.headings[1:]) if b - a > 1]
    (ok if not skips else warn)("Jerarquía de títulos sin saltos" if not skips else f"Saltos de nivel en títulos: {skips}")

    dupes = {i for i in parser.ids if parser.ids.count(i) > 1}
    (ok if not dupes else fail)("IDs únicos" if not dupes else f"IDs repetidos: {sorted(dupes)}")

    anchors = [h for h in parser.hrefs if h.startswith("#") and len(h) > 1]
    broken = [h for h in anchors if h[1:] not in parser.ids]
    (ok if not broken else fail)(
        f"{len(anchors)} anclas internas apuntan a un id existente" if not broken else f"Anclas rotas: {broken}"
    )

    local = [r for r in parser.hrefs + parser.srcs if not re.match(r"^(https?:|mailto:|data:|#|//)", r)]
    missing = [r for r in local if not (ROOT / r.split("?")[0].split("#")[0]).exists()]
    (ok if not missing else fail)(
        f"{len(local)} archivos locales referenciados existen" if not missing else f"Archivos que no existen: {missing}"
    )

    (ok if parser.imgs_without_alt == 0 else fail)(
        "Todas las imágenes tienen alt" if parser.imgs_without_alt == 0 else f"{parser.imgs_without_alt} imagen(es) sin alt"
    )
    (ok if not parser.blank_without_noopener else fail)(
        "Enlaces con target=_blank llevan rel=noopener"
        if not parser.blank_without_noopener
        else f"Falta rel=noopener en: {parser.blank_without_noopener}"
    )
    return parser


def check_css():
    path = ROOT / "styles.css"
    if not path.exists():
        return
    css = path.read_text(encoding="utf-8")
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    balanced = stripped.count("{") == stripped.count("}")
    (ok if balanced else fail)("Llaves { } balanceadas en el CSS" if balanced else "Llaves { } desbalanceadas en el CSS")

    bad = []
    for n, line in enumerate(stripped.splitlines(), 1):
        if ":" not in line:
            continue
        for m in re.finditer(r"#([0-9a-fA-F]+)(?=[\s;,)]|$)", line):
            if len(m.group(1)) not in (3, 4, 6, 8):
                bad.append(f"línea {n}: #{m.group(1)}")
        if re.search(r"#[0-9a-fA-F]{3,8}\s+[0-9a-fA-F]{1,4}\s*;", line):
            bad.append(f"línea {n}: color con espacio en medio")
    (ok if not bad else fail)("Colores hexadecimales válidos" if not bad else f"Colores sospechosos: {bad}")

    used = set(re.findall(r"var\(--([\w-]+)", stripped))
    defined = set(re.findall(r"--([\w-]+)\s*:", stripped))
    # Variables que el HTML define en línea, por ejemplo style="--d:.2s"
    html_path = ROOT / "index.html"
    if html_path.exists():
        defined |= set(re.findall(r"--([\w-]+)\s*:", html_path.read_text(encoding="utf-8")))
    undefined = sorted(used - defined)
    (ok if not undefined else fail)(
        "Todas las variables CSS usadas están definidas" if not undefined else f"Variables CSS sin definir: {undefined}"
    )


def check_js():
    path = ROOT / "script.js"
    if not path.exists():
        return
    node = shutil.which("node")
    if not node:
        warn("Node no está instalado: se omite la revisión de sintaxis de script.js")
        return
    proc = subprocess.run([node, "--check", str(path)], capture_output=True, text=True)
    (ok if proc.returncode == 0 else fail)(
        "script.js sin errores de sintaxis" if proc.returncode == 0 else f"Error de sintaxis en script.js: {proc.stderr.strip()[:200]}"
    )


SECRET_PATTERNS = {
    "clave de AWS": r"AKIA[0-9A-Z]{16}",
    "token de GitHub": r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}",
    "clave tipo sk-": r"\bsk-[A-Za-z0-9]{20,}",
    "llave privada": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "contraseña asignada": r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"\s]{6,}['\"]",
    "URL con credenciales": r"https?://[^/\s:@]+:[^/\s@]+@",
}


def iter_text_files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS) and p.suffix.lower() in TEXT_EXT:
            yield p


def check_secrets():
    hits = []
    for p in iter_text_files():
        if p.name == "check.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for label, pat in SECRET_PATTERNS.items():
            if re.search(pat, text):
                hits.append(f"{p.relative_to(ROOT)} ({label})")
    (ok if not hits else fail)("Sin patrones de secretos en los archivos" if not hits else f"Posible secreto en: {hits}")

    env_files = [str(p.relative_to(ROOT)) for p in ROOT.rglob(".env*") if p.is_file() and not (set(p.parts) & SKIP_DIRS)]
    (ok if not env_files else fail)("No hay archivos .env" if not env_files else f"Archivos .env presentes: {env_files}")

    gi = ROOT / ".gitignore"
    if gi.exists():
        content = gi.read_text(encoding="utf-8")
        missing = [x for x in (".env", "node_modules") if x not in content]
        (ok if not missing else warn)(
            ".gitignore cubre .env y node_modules" if not missing else f".gitignore no menciona: {missing}"
        )


def check_placeholders(strict):
    found = {}
    for p in iter_text_files():
        if p.name == "check.py":
            continue
        n = len(re.findall(r"TU_[A-Z_]+", p.read_text(encoding="utf-8", errors="ignore")))
        if n:
            found[str(p.relative_to(ROOT))] = n
    if not found:
        ok("Sin valores pendientes (TU_...)")
    else:
        (fail if strict else warn)(f"Pendiente de reemplazar (busca TU_ en VS Code): {found}")


def check_online(parser):
    if parser is None:
        return
    urls = sorted({h for h in parser.hrefs if h.startswith("http") and "TU_" not in h and "fonts.g" not in h})
    for url in urls:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "portafolio-check/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                (ok if r.status < 400 else fail)(f"{r.status} {url}")
        except urllib.error.HTTPError as e:
            (warn if e.code in (403, 429, 999) else fail)(f"{e.code} {url}")
        except Exception as e:  # sin red, DNS, etc.
            warn(f"No se pudo comprobar {url} ({type(e).__name__})")


def main():
    strict = "--strict" in sys.argv
    check_files()
    parser = check_html()
    check_css()
    check_js()
    check_secrets()
    check_placeholders(strict)
    if "--online" in sys.argv:
        check_online(parser)

    for level, msg in results:
        print(f"[{level:<5}] {msg}")
    errors = sum(1 for lvl, _ in results if lvl == "ERROR")
    warns = sum(1 for lvl, _ in results if lvl == "AVISO")
    print(f"\n{len(results) - errors - warns} correctas, {warns} avisos, {errors} errores")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
