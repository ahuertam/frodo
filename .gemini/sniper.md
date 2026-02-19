# Sniper — Cazador de chollos en segunda mano 🎯

## Qué hace
Rastrea Vinted y Wallapop automáticamente buscando artículos a buen precio. Genera un dashboard HTML con resultados en vivo (fotos, precios, enlaces). Anti-bot con delays aleatorios y User-Agent rotatorio.

## Archivos clave

| Archivo | Función |
|---|---|
| `sniper.py` | Cerebro del agente (14KB). Selenium para scraping. |
| `results.html` | Dashboard de resultados (12KB). Se regenera automáticamente. |
| `doc.md` | Documentación |

## Carpetas

- `venv/` → Entorno virtual (Selenium, etc.)

## Flujo

1. `./venv/bin/python3 sniper.py`
2. Escribe qué buscar (ej: "Zelda 3DS")
3. Elige plataforma (1=Vinted, 2=Wallapop)
4. Abre `results.html` en navegador — se auto-refresca cada 5 segundos

## Plataformas

| Plataforma | Estado |
|---|---|
| **Vinted** | ✅ Muy estable |
| **Wallapop** | ⚠️ Funcional pero puede pedir CAPTCHA (Cloudflare) |

## Características

- Modo interactivo (no tocas código)
- User-Agent rotatorio
- Esperas aleatorias (30-90s) para simular humano
- Timestamp de "Último escaneo" en el dashboard

## Dependencias
`selenium` + ChromeDriver

## Notas para desarrollo

- Todo modo interactivo, no hay config files.
- El `results.html` es HTML estático regenerado — no es un servidor web.
- Problemas comunes: Connection Refused al Ctrl+C (normal), CAPTCHA en Wallapop.
