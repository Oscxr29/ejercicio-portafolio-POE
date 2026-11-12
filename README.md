# Portafolio de Oscar Guevara

Sitio personal estático con HTML, CSS y un poco de JavaScript. Muestra mis proyectos de la carrera de Ingeniería en Desarrollo de Software (UNIVO), el stack que uso y cómo contactarme. Sin foto de perfil por ahora.

Sitio publicado: TU_URL_VERCEL

## Archivos

| Archivo | Qué hace |
|---|---|
| [`index.html`](index.html) | Contenido: presentación, proyectos, stack, sobre mí y contacto |
| [`styles.css`](styles.css) | Tema terminal (verde y magenta sobre negro), adaptable a móvil |
| [`script.js`](script.js) | Marca en el menú la sección que se está viendo |
| [`scripts/check.py`](scripts/check.py) | Revisión automática antes de cada commit |
| [`vercel.json`](vercel.json) | Cabeceras de seguridad básicas para el despliegue |

## Ver en local

Abre `index.html` con doble clic, o usa la extensión Live Server de VS Code para que recargue sola al guardar. No hay que instalar dependencias.

## Pruebas

```bash
python scripts/check.py
```

En Windows, si `python` no responde, usa `py scripts/check.py`.

| Revisión | Qué comprueba |
|---|---|
| HTML | `lang`, `title`, meta description, viewport, un solo `h1`, IDs únicos, anclas y archivos locales existentes, `alt` en imágenes, `rel=noopener` |
| CSS | Llaves balanceadas, colores hexadecimales válidos, variables definidas |
| JS | Sintaxis con `node --check` (si Node está instalado) |
| Seguridad | Patrones de claves o tokens, archivos `.env`, `.gitignore` |
| Pendientes | Valores `TU_...` que faltan por reemplazar |

Con `--online` también comprueba que los enlaces externos respondan. Con `--strict`, los pendientes cuentan como error.

## Despliegue

Vercel está conectado a este repositorio. Cada `git push` a `main` publica una versión nueva sin pasos extra.

## Personalizar

| Quiero cambiar | Dónde |
|---|---|
| Correo y LinkedIn | Sección `#contacto` de `index.html` (busca `TU_`) |
| Agregar un proyecto | Copia un bloque `<article class="proj">` en `index.html` |
| Colores | Variables al inicio de `styles.css` (`--green`, `--magenta`, `--bg`) |


