# Charts del post (estilo de marca)

Reemplazan a `charts_post_2026.py` (matplotlib, feo). Cada gráfico es un HTML con SVG inline
dibujado a mano en JS, con la receta de la skill `grafico-marca` (Jost, morado de marca,
esquinas redondeadas, track de fondo, theme claro).

- `mapa.html` → `layoffs-2026-causas-mapa.png` (barras horizontales, motivos de los 161)
- `embudo.html` → `layoffs-2026-embudo.png` (funnel 161 → 71 → 10 → 1)
- `tornado.html` → `layoffs-2026-publico-privado.png` (público vs privado, back-to-back)

Los números están hardcodeados en cada HTML (salen del dataset `2026-categorized.json`,
ventana `date < 2026-07-01`); si cambia la clasificación, actualizarlos a mano.

## Regenerar los PNG

```bash
cd charts_marca
python3 -m http.server 8899 >/dev/null 2>&1 &         # Playwright bloquea file://
NODE_PATH=$(npm root -g) node render.js               # o el node_modules donde esté playwright
kill %1
# copiar al blog:
cp mapa.png    ../../trabajo/images/layoffs-2026-causas-mapa.png
cp embudo.png  ../../trabajo/images/layoffs-2026-embudo.png
cp tornado.png ../../trabajo/images/layoffs-2026-publico-privado.png
```

`render.js` screenshotea el elemento `.card` con `deviceScaleFactor:2` (nada de viewport exacto,
así no hay bandas grises).

## Gotcha

Nunca declarar una variable JS global llamada `top` (choca con `window.top` → SyntaxError,
el script muere y el SVG sale vacío). Acá se usa `oy`.
