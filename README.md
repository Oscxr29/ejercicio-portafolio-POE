# Portafolio de Oscar Guevara

Sitio personal estático con HTML, CSS y un poco de JavaScript. Presenta cuatro proyectos de la carrera de Ingeniería en Desarrollo de Software (UNIVO): GeoMundo, Estructura de Datos, Servidores Web y Préstamos de biblioteca. También incluye el stack, información personal y contacto por GitHub y LinkedIn.

El sitio usa HTML, CSS, JavaScript, TypeScript, Python, Vue 3, Node.js, Express y MySQL. La interfaz tiene un tema de terminal con fuentes Chakra Petch y JetBrains Mono cargadas desde Google Fonts.

Sitio publicado: TU_URL_VERCEL

## Contenido

| Sección | Qué muestra |
|---|---|
| `#inicio` | Presentación tipo terminal y enlaces a los cuatro proyectos |
| `#proyectos` | GeoMundo, Estructura de Datos, Servidores Web y Préstamos de biblioteca |
| `#stack` | Lenguajes, frontend, backend, datos, despliegue y herramientas |
| `#sobre-mi` | Trayectoria, trabajo con Node en Windows Server, Python, Xonotic e interés en inteligencia artificial |
| `#contacto` | Enlaces a GitHub y LinkedIn |

## Archivos

| Archivo | Qué hace |
|---|---|
| [`index.html`](index.html) | Estructura, contenido, secciones, enlaces externos y carga de estilos y script |
| [`styles.css`](styles.css) | Tema terminal, variables de color y tipografía, diseño responsive y animaciones |
| [`script.js`](script.js) | Actualiza `aria-current` en el menú con `IntersectionObserver` |
| [`scripts/check.py`](scripts/check.py) | Ejecuta revisiones locales de HTML, CSS, JavaScript, secretos, placeholders y archivos |
| [`vercel.json`](vercel.json) | Configura cabeceras HTTP de seguridad para todas las rutas |
| [`.gitignore`](.gitignore) | Excluye secretos `.env`, dependencias, salidas de Vercel, archivos del sistema y logs |

## Ver en local

Abre `index.html` con doble clic, o usa la extensión Live Server de VS Code para que recargue sola al guardar. No hay que instalar dependencias.

## Pruebas

```bash
python scripts/check.py
```

En Windows, si `python` no responde, usa `py scripts/check.py`.

| Revisión | Qué comprueba |
|---|---|
| Archivos | Existencia de `index.html`, `styles.css`, `script.js`, `README.md` y `.gitignore` |
| HTML | `lang`, `title`, meta description, viewport, un solo `h1`, jerarquía de títulos, IDs únicos, anclas y archivos locales existentes, `alt` en imágenes y `rel=noopener` |
| CSS | Llaves balanceadas, colores hexadecimales válidos y variables usadas definidas |
| JS | Sintaxis con `node --check` si Node está instalado |
| Secretos | Patrones de claves o tokens, archivos `.env` y cobertura de `.env` y `node_modules` en `.gitignore` |
| Pendientes | Valores `TU_...`; con `--strict` cuentan como error |

Con `--online` también comprueba que los enlaces externos respondan. La comprobación de enlaces omite las fuentes de Google Fonts y las URL que contienen `TU_`.

## Despliegue

| Elemento | Configuración |
|---|---|
| Plataforma | Vercel |
| Entrada | Sitio estático desde `index.html`, sin proceso de build |
| Cabeceras | `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` y `X-Frame-Options: DENY` |
| Configuración | [`vercel.json`](vercel.json) aplica las cabeceras a `/(.*)` |

## Personalizar

| Qué cambiar | Dónde |
|---|---|
| Nombre, presentación, proyectos, stack y contacto | [`index.html`](index.html); las secciones usan `#inicio`, `#proyectos`, `#stack`, `#sobre-mi` y `#contacto` |
| Navegación y proyectos | Clases `.nav`, `.projects`, `.proj`, `.proj-main`, `.repo` en [`index.html`](index.html) y [`styles.css`](styles.css) |
| Colores y tipografías | Variables `--bg`, `--panel`, `--panel-2`, `--line`, `--line-strong`, `--text`, `--heading`, `--dim`, `--green`, `--green-dim`, `--magenta`, `--font-display` y `--font-mono` en [`styles.css`](styles.css) |
| Comportamiento del menú | [`script.js`](script.js); busca enlaces `.nav a` y activa `aria-current` según la sección visible |

