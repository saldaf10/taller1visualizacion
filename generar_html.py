# -*- coding: utf-8 -*-
import base64, pathlib

imgs = {}
for name in ['reto1_jerarquia', 'reto2_contraste', 'reto3_persuasion']:
    imgs[name] = base64.b64encode(pathlib.Path(f'outputs/{name}.png').read_bytes()).decode()

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Taller Evaluacion 1 - Comunicacion Basada en Evidencia</title>
<style>
  :root {{
    --azul: #1565C0;
    --naranja: #E65100;
    --rojo: #B00020;
    --verde: #1B5E20;
    --texto: #212121;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Segoe UI", Arial, sans-serif; background: #FAFAFA; color: var(--texto); }}

  /* PORTADA */
  .portada {{
    background: linear-gradient(135deg, #0D47A1 0%, #1565C0 60%, #1976D2 100%);
    color: white; padding: 80px 60px; min-height: 100vh;
    display: flex; flex-direction: column; justify-content: center;
  }}
  .portada .badge {{
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3); border-radius: 20px;
    padding: 6px 16px; font-size: 12px; letter-spacing: 1.5px;
    text-transform: uppercase; margin-bottom: 28px; width: fit-content;
  }}
  .portada h1 {{ font-size: 48px; font-weight: 800; line-height: 1.15; margin-bottom: 16px; }}
  .portada h1 span {{ color: #90CAF9; }}
  .portada .subtitulo {{ font-size: 18px; opacity: 0.85; margin-bottom: 40px; max-width: 600px; line-height: 1.6; }}
  .portada .meta {{ display: flex; gap: 48px; flex-wrap: wrap; }}
  .portada .meta-item label {{ font-size: 11px; letter-spacing: 1px; text-transform: uppercase; opacity: 0.6; display: block; margin-bottom: 4px; }}
  .portada .meta-item span {{ font-size: 16px; font-weight: 600; }}
  .portada .formula {{
    margin-top: 60px; background: rgba(255,255,255,0.1);
    border-left: 4px solid #90CAF9; border-radius: 0 8px 8px 0;
    padding: 20px 28px; max-width: 560px; font-size: 15px; line-height: 1.7;
  }}
  .portada .formula strong {{ color: #90CAF9; font-size: 17px; }}

  /* SECCIONES */
  .seccion {{ padding: 80px 60px; }}
  .seccion.alt {{ background: white; }}
  .seccion-titulo {{ font-size: 13px; letter-spacing: 2px; text-transform: uppercase; color: var(--azul); font-weight: 700; margin-bottom: 10px; }}
  .seccion-h2 {{ font-size: 34px; font-weight: 800; margin-bottom: 40px; line-height: 1.2; }}

  /* TABLA CRITERIOS */
  .tabla-criterios {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
  .tabla-criterios th {{ background: var(--azul); color: white; padding: 14px 20px; text-align: left; font-size: 13px; letter-spacing: 0.5px; }}
  .tabla-criterios td {{ padding: 14px 20px; border-bottom: 1px solid #E0E0E0; font-size: 14px; }}
  .tabla-criterios tr:last-child td {{ border-bottom: none; }}
  .tabla-criterios tr:nth-child(even) td {{ background: #F8F8F8; }}
  .pill {{ display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }}
  .pill-azul {{ background: #E3F2FD; color: #1565C0; }}
  .pill-verde {{ background: #E8F5E9; color: #1B5E20; }}
  .pill-naranja {{ background: #FFF3E0; color: #E65100; }}

  /* RETO HEADER */
  .reto-header {{ display: flex; align-items: flex-start; gap: 24px; margin-bottom: 36px; flex-wrap: wrap; }}
  .reto-num {{
    background: var(--azul); color: white; width: 64px; height: 64px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 26px; font-weight: 900; flex-shrink: 0;
  }}
  .reto-num.naranja {{ background: var(--naranja); }}
  .reto-num.verde {{ background: var(--verde); }}
  .reto-info h2 {{ font-size: 28px; font-weight: 800; margin-bottom: 6px; }}
  .reto-info .tag {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }}
  .tag-azul {{ color: var(--azul); }}
  .tag-naranja {{ color: var(--naranja); }}
  .tag-verde {{ color: var(--verde); }}

  /* GRAFICA */
  .grafica-container {{
    background: white; border-radius: 12px;
    box-shadow: 0 2px 20px rgba(0,0,0,0.08); overflow: hidden; margin-bottom: 36px;
  }}
  .grafica-container img {{ width: 100%; display: block; }}

  /* GRID */
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 32px; }}
  @media (max-width: 800px) {{
    .grid-2 {{ grid-template-columns: 1fr; }}
    .portada {{ padding: 40px 24px; }}
    .seccion {{ padding: 48px 24px; }}
  }}

  /* CARD */
  .card {{ background: white; border-radius: 12px; padding: 28px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
  .card h4 {{ font-size: 14px; font-weight: 700; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* CHECKLIST */
  .checklist {{ list-style: none; }}
  .checklist li {{
    padding: 8px 0; border-bottom: 1px solid #F0F0F0;
    font-size: 14px; color: #333; display: flex; align-items: flex-start; gap: 10px;
  }}
  .checklist li:last-child {{ border-bottom: none; }}
  .check-ok {{ color: #1B5E20; font-weight: 900; font-size: 16px; flex-shrink: 0; }}

  /* JUSTIFICACION */
  .justificacion {{
    border-left: 4px solid var(--azul); background: #E3F2FD;
    border-radius: 0 8px 8px 0; padding: 20px 24px;
    font-size: 14px; line-height: 1.7; color: #1A237E;
  }}
  .justificacion.naranja {{ border-color: var(--naranja); background: #FFF3E0; color: #4E2000; }}
  .justificacion.verde {{ border-color: var(--verde); background: #E8F5E9; color: #1B3A1F; }}

  /* ACTO DE HABLA */
  .acto-habla {{
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: white; border-radius: 12px; padding: 36px; margin-bottom: 36px;
  }}
  .acto-habla h3 {{ font-size: 20px; margin-bottom: 16px; }}
  .badge-acto {{
    display: inline-block; background: #A5D6A7; color: #1B5E20;
    border-radius: 20px; padding: 4px 16px; font-weight: 800; font-size: 13px; margin-bottom: 16px;
  }}
  .narrativa {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 20px; }}
  @media (max-width: 700px) {{ .narrativa {{ grid-template-columns: 1fr; }} }}
  .narrativa-item {{
    background: rgba(255,255,255,0.12); border-radius: 8px;
    padding: 18px; border-top: 3px solid rgba(255,255,255,0.4);
  }}
  .narrativa-item .step {{ font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; opacity: 0.7; margin-bottom: 6px; }}
  .narrativa-item p {{ font-size: 13px; line-height: 1.6; }}

  .divider {{ border: none; border-top: 2px solid #EEEEEE; margin: 0; }}

  /* FOOTER */
  .footer {{
    background: #212121; color: #BDBDBD;
    padding: 40px 60px; text-align: center; font-size: 13px; line-height: 1.8;
  }}
  .footer strong {{ color: white; }}
</style>
</head>
<body>

<!-- PORTADA -->
<section class="portada">
  <div class="badge">Universidad EAFIT &mdash; Maestr&iacute;a en Ciencia de Datos</div>
  <h1>Taller &mdash; Evaluaci&oacute;n 1<br><span>Comunicaci&oacute;n Basada en Evidencia</span></h1>
  <p class="subtitulo">Unidad 1: Fundamentos de la Comunicaci&oacute;n Visual y Estrategia de Negocio<br>
  Dataset: Superstore Sales &mdash; Kaggle (rohitsahoo/sales-forecasting)</p>
  <div class="meta">
    <div class="meta-item"><label>Peso</label><span>15% de la nota final</span></div>
    <div class="meta-item"><label>Retos</label><span>3 &mdash; 33 / 33 / 34%</span></div>
    <div class="meta-item"><label>Dataset</label><span>9.800 registros &middot; 18 variables</span></div>
    <div class="meta-item"><label>Periodo</label><span>2015 &mdash; 2018</span></div>
  </div>
  <div class="formula">
    <strong>F&oacute;rmula del curso:</strong><br>
    Contexto + Datos + Contraste = Mensaje<br><br>
    Criterio de maestr&iacute;a (5.0): el tomador de decisiones puede responder<br>
    <em>"&iquest;Qu&eacute; debo hacer hoy?"</em> con solo mirar tu trabajo por <strong>5 segundos</strong>.
  </div>
</section>

<!-- CRITERIOS -->
<section class="seccion alt">
  <div class="seccion-titulo">R&uacute;brica</div>
  <h2 class="seccion-h2">Ejes de evaluaci&oacute;n por reto</h2>
  <table class="tabla-criterios">
    <thead>
      <tr><th>Eje</th><th>Qu&eacute; mide</th><th>Peso</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>T&eacute;cnico</strong></td><td>Uso correcto de librer&iacute;as Python y limpieza de c&oacute;digo</td><td><span class="pill pill-azul">40%</span></td></tr>
      <tr><td><strong>Narrativo</strong></td><td>Claridad del mensaje y jerarqu&iacute;a visual</td><td><span class="pill pill-verde">40%</span></td></tr>
      <tr><td><strong>Cr&iacute;tico</strong></td><td>Justificaci&oacute;n de la elecci&oacute;n del gr&aacute;fico</td><td><span class="pill pill-naranja">20%</span></td></tr>
    </tbody>
  </table>
</section>

<hr class="divider">

<!-- RETO 1 -->
<section class="seccion">
  <div class="reto-header">
    <div class="reto-num">1</div>
    <div class="reto-info">
      <div class="tag tag-azul">Reto 1 &mdash; 33% &bull; Jerarqu&iacute;a</div>
      <h2>"Ingenier&iacute;a de la Atenci&oacute;n"</h2>
    </div>
  </div>
  <div class="justificacion">
    <strong>Justificaci&oacute;n del tipo de gr&aacute;fico:</strong> La pregunta de negocio es de comparaci&oacute;n de
    categor&iacute;as (&iquest;qu&eacute; subcategor&iacute;a genera m&aacute;s ventas?), no de tendencia temporal. El gr&aacute;fico de
    barras horizontales ordenado de mayor a menor es el m&aacute;s eficiente para este tipo de pregunta.
    El orden descendente permite leer la jerarqu&iacute;a en un solo vistazo; la orientaci&oacute;n horizontal
    facilita leer etiquetas largas sin rotaci&oacute;n. El color selectivo (azul institucional solo en
    Phones) activa la memoria sensorial en menos de 1 segundo aplicando el principio Data-to-Ink Ratio.
  </div>
  <div class="grafica-container" style="margin-top:28px;">
    <img src="data:image/png;base64,{imgs['reto1_jerarquia']}" alt="Reto 1 - Jerarquia">
  </div>
  <div class="grid-2">
    <div class="card">
      <h4 style="color:#1565C0;">Decisiones de dise&ntilde;o</h4>
      <ul class="checklist">
        <li><span class="check-ok">&#10003;</span> Barras ordenadas de mayor a menor (no por defecto)</li>
        <li><span class="check-ok">&#10003;</span> Gris neutro en todas las subcategor&iacute;as excepto la l&iacute;der</li>
        <li><span class="check-ok">&#10003;</span> Azul institucional (#1565C0) solo en Phones</li>
        <li><span class="check-ok">&#10003;</span> Sin grilla, sin bordes, sin eje X redundante</li>
        <li><span class="check-ok">&#10003;</span> Etiquetas de valor en cada barra (reduce carga cognitiva)</li>
        <li><span class="check-ok">&#10003;</span> T&iacute;tulo accionable, no descriptivo</li>
      </ul>
    </div>
    <div class="card">
      <h4 style="color:#1565C0;">Checklist de maestr&iacute;a</h4>
      <ul class="checklist">
        <li><span class="check-ok">&#10003;</span> Dato prioritario salta a la vista sin leer etiquetas</li>
        <li><span class="check-ok">&#10003;</span> C&oacute;digo limpio con comentarios que justifican decisiones visuales</li>
        <li><span class="check-ok">&#10003;</span> Elementos decorativos eliminados (fondo, grilla, colores innecesarios)</li>
        <li><span class="check-ok">&#10003;</span> Incluye t&iacute;tulo, eje Y y fuente del dato</li>
      </ul>
    </div>
  </div>
</section>

<hr class="divider">

<!-- RETO 2 -->
<section class="seccion alt">
  <div class="reto-header">
    <div class="reto-num naranja">2</div>
    <div class="reto-info">
      <div class="tag tag-naranja">Reto 2 &mdash; 33% &bull; Contraste</div>
      <h2>"Detecci&oacute;n de Anomal&iacute;as"</h2>
    </div>
  </div>
  <div class="justificacion naranja">
    <strong>Justificaci&oacute;n del tipo de gr&aacute;fico:</strong> Los datos tienen una dimensi&oacute;n temporal
    continua (2015&ndash;2018), lo que hace que la l&iacute;nea temporal sea la representaci&oacute;n natural para
    mostrar tendencia y detectar anomal&iacute;as. La comparaci&oacute;n Antes/Despu&eacute;s demuestra con precisi&oacute;n
    qu&eacute; cambi&oacute; y por qu&eacute;: en la versi&oacute;n "Antes" todos los meses tienen el mismo tratamiento
    visual; en la versi&oacute;n "Despu&eacute;s" el contexto (gris) act&uacute;a como fondo y el pico de noviembre
    2018 (rojo) act&uacute;a como figura, aplicando el principio de figura-fondo de la Gestalt.
  </div>
  <div class="grafica-container" style="margin-top:28px;">
    <img src="data:image/png;base64,{imgs['reto2_contraste']}" alt="Reto 2 - Contraste">
  </div>
  <div class="grid-2">
    <div class="card">
      <h4 style="color:#E65100;">Decisiones de dise&ntilde;o</h4>
      <ul class="checklist">
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> L&iacute;nea hist&oacute;rica en gris neutro (contexto / fondo)</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Pico de noviembre 2018 en rojo vibrante (figura)</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Anotaci&oacute;n directa sobre el gr&aacute;fico con insight en 7 palabras</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Comparaci&oacute;n Antes/Despu&eacute;s en el mismo entregable</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> T&iacute;tulos ANTES (rojo) / DESPU&Eacute;S (verde) para guiar la lectura</li>
      </ul>
    </div>
    <div class="card">
      <h4 style="color:#E65100;">Checklist de maestr&iacute;a</h4>
      <ul class="checklist">
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Comparaci&oacute;n Antes/Despu&eacute;s presente en el entregable</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Anomal&iacute;a evidente en menos de 3 segundos sin leer el t&iacute;tulo</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Anotaci&oacute;n explica el insight directamente sobre el gr&aacute;fico</li>
        <li><span class="check-ok" style="color:#E65100;">&#10003;</span> Justificaci&oacute;n del contraste documentada en el c&oacute;digo</li>
      </ul>
    </div>
  </div>
</section>

<hr class="divider">

<!-- RETO 3 -->
<section class="seccion">
  <div class="reto-header">
    <div class="reto-num verde">3</div>
    <div class="reto-info">
      <div class="tag tag-verde">Reto 3 &mdash; 34% &bull; Persuasi&oacute;n</div>
      <h2>"Acto de Habla"</h2>
    </div>
  </div>
  <div class="acto-habla">
    <h3>Acto de Habla declarado</h3>
    <div class="badge-acto">CONVENCER</div>
    <p style="font-size:14px; line-height:1.7; opacity:0.9;">
      Se elige <strong>Convencer</strong> porque el gr&aacute;fico no solo describe las ventas por regi&oacute;n,
      sino que <em>argumenta una redistribuci&oacute;n del presupuesto comercial</em>. La regi&oacute;n South
      acumula apenas el 17% de las ventas totales pese a operar con el mismo portafolio de productos
      que las dem&aacute;s regiones. Esto constituye una brecha de rendimiento que demanda acci&oacute;n inmediata.
    </p>
    <div class="narrativa">
      <div class="narrativa-item">
        <div class="step">1 &mdash; Contexto</div>
        <p>4 regiones compiten con el mismo portafolio de productos (Furniture, Office Supplies, Technology)</p>
      </div>
      <div class="narrativa-item">
        <div class="step">2 &mdash; Hallazgo</div>
        <p>South genera solo $389K (17%) mientras West lidera con $710K (31%) &mdash; una brecha del 82%</p>
      </div>
      <div class="narrativa-item">
        <div class="step">3 &mdash; Recomendaci&oacute;n</div>
        <p>Redirigir presupuesto e inversi&oacute;n comercial hacia South para capturar la oportunidad latente</p>
      </div>
    </div>
  </div>
  <div class="justificacion verde">
    <strong>Justificaci&oacute;n del tipo de gr&aacute;fico:</strong> Se eligi&oacute; un gr&aacute;fico de barras verticales porque
    la pregunta es de comparaci&oacute;n discreta entre 4 regiones (no tendencia temporal). La orientaci&oacute;n
    vertical facilita la comparaci&oacute;n de alturas, que es la tarea visual m&aacute;s precisa para categor&iacute;as
    con nombres cortos. El color selectivo (naranja de alerta en South) dirige la atenci&oacute;n hacia la
    oportunidad de mejora, no hacia el l&iacute;der, lo que refuerza el argumento persuasivo.
  </div>
  <div class="grafica-container" style="margin-top:28px;">
    <img src="data:image/png;base64,{imgs['reto3_persuasion']}" alt="Reto 3 - Persuasion">
  </div>
  <div class="grid-2">
    <div class="card">
      <h4 style="color:#1B5E20;">Decisiones de dise&ntilde;o</h4>
      <ul class="checklist">
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> T&iacute;tulo comunica acci&oacute;n, no descripci&oacute;n del gr&aacute;fico</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Naranja en South (alerta) vs gris en las dem&aacute;s regiones</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Subt&iacute;tulo integra Contexto &rarr; Hallazgo &rarr; Recomendaci&oacute;n</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Anotaci&oacute;n directa que interpela al equipo comercial</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Etiquetas con $ y % para lectura inmediata sin eje Y</li>
      </ul>
    </div>
    <div class="card">
      <h4 style="color:#1B5E20;">Checklist de maestr&iacute;a</h4>
      <ul class="checklist">
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> T&iacute;tulo comunica una acci&oacute;n, no describe el gr&aacute;fico</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Estructura Contexto &rarr; Hallazgo &rarr; Recomendaci&oacute;n legible</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Acto de Habla (Convencer) declarado expl&iacute;citamente</li>
        <li><span class="check-ok" style="color:#1B5E20;">&#10003;</span> Al ver 5 segundos, queda claro qu&eacute; decisi&oacute;n tomar</li>
      </ul>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <strong>Taller &mdash; Evaluaci&oacute;n 1 (15%)</strong><br>
  Universidad EAFIT &mdash; Maestr&iacute;a en Ciencia de Datos &mdash; Unidad 1<br>
  Dataset: <em>Superstore Sales</em> &mdash; Kaggle (rohitsahoo/sales-forecasting) &mdash; 9.800 registros &middot; 2015&ndash;2018
</footer>

</body>
</html>"""

with open('presentacion_taller1.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('HTML generado OK -> presentacion_taller1.html')
