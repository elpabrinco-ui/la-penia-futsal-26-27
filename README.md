# La Peña F.C. · Futsal 2026/27

Sitio del equipo para el torneo de futsal DAI (Række 1). Muestra el próximo partido, el fixture, la tabla, las estadísticas y el plantel. Se abre desde cualquier celular, sin cuenta de Claude.

## Cómo está armado

- `index.html`: la página. No se toca para actualizar datos.
- `data.json`: todos los datos del sitio. Se edita este archivo para actualizar.
- `assets/`: escudo e ícono.

## Qué hay en `data.json`

| Parte | Quién la actualiza | Qué contiene |
| --- | --- | --- |
| `fixtures` | Automático (agente diario) | 30 partidos de la liga. `result` es `null` hasta que se juega, después `{"h": 2, "a": 1}` (goles del local y del visitante). |
| `standings` | Automático (agente diario) | Tabla oficial de DAI. |
| `meta.updated` | Automático | Fecha de la última actualización (`AAAA-MM-DD`). |
| `squad` | Matías | Jugadores: nombre, número (`null` si no hay), posición y apodo opcional (`nick`). |
| `matches` | Matías (por chat) | Datos por partido, con el `id` del partido como clave. |

Datos que se cargan en `matches["<id>"]`:

```json
{
  "lineup":  ["Nombre completo", "..."],
  "goals":   {"Nombre completo": 2},
  "assists": {"Nombre completo": 1},
  "yellow":  {"Nombre completo": 1},
  "red":     {},
  "avail":   {"Nombre completo": "si"},
  "mvp":     "Nombre",
  "note":    "Texto libre"
}
```

`avail` acepta `si`, `duda` o `no`. Los nombres tienen que ser iguales a los de `squad`.

## Reglas para el agente que actualiza

1. Leer la tabla y el calendario de DAI:
   - Calendario completo: https://resultater.dai-sport.dk/tms/Turneringer-og-resultater/Pulje-Komplet-Kampprogram.aspx?PuljeId=947
   - Tabla: https://resultater.dai-sport.dk/tms/Turneringer-og-resultater/Pulje-Stilling.aspx?PuljeId=947
2. Actualizar solo `fixtures` (fecha, hora, cancha y `result`), `standings` y `meta.updated`.
3. No tocar `squad` ni `matches`: los carga Matías.
4. Si un partido cambia de fecha, hora o cancha, guardar el cambio. Si falta un resultado en la web, dejar `result` en `null`.
5. Si la web de DAI no responde o cambia de formato, no inventar datos: dejar el archivo como está.
6. Después de cambiar `data.json`, guardar y subir el cambio a `main`. El sitio se publica solo.

## Publicación

El sitio se publica con GitHub Pages desde la rama `main`.
