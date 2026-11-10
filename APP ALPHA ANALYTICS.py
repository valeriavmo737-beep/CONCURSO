# ANÁLISIS FINANCIERO: Coca-Cola, McDonald's y Disney

# --- 1. Librerías ---
import streamlit as st          # la página web
import yfinance as yf           # precios de Yahoo Finance
import pandas as pd             # tablas
import numpy as np              # matemáticas
import plotly.express as px     # gráficos interactivos

# --- 2. Configuración de la página ---
st.set_page_config(page_title="ANÁLISIS FINANCIERO", page_icon="📈",
                   layout="wide", initial_sidebar_state="collapsed")

# --- 3. Colores y empresas ---
# Dos temas de colores: el interruptor elige cuál usar
TEMAS = {
    "oscuro": dict(bg="#0F172A", card="#1E293B", texto="#F8FAFC", gris="#94A3B8", borde="#334155",
                   KO="#E50914", DIS="#0063E5", MCD="#FFC72C", h1="#1E293B", h2="#1D4ED8", plotly="plotly_dark"),
    "claro":  dict(bg="#EAF5FE", card="#FFFFFF", texto="#0F172A", gris="#475569", borde="#CFE8FA",
                   KO="#D61C22", DIS="#11385B", MCD="#DAA520", h1="#075985", h2="#0284C7", plotly="plotly_white"),
}
VERDE, ROJO, AMBAR = "#10B981", "#EF4444", "#F59E0B"   # ganancia, pérdida, riesgo medio

# Nombre -> código en bolsa (ticker) e icono
EMPRESAS = {
    "Coca-Cola":  {"ticker": "KO",  "icono": "🥤"},
    "McDonald's": {"ticker": "MCD", "icono": "🍔"},
    "Disney":     {"ticker": "DIS", "icono": "🏰"},
}

# --- 4. Filtros ---
banner = st.container()   # espacio reservado arriba; se llena más abajo

with st.container(border=True, key="filtros"):
    f1, f2, f3, f4 = st.columns([3, 2, 2, 1.2])
    with f1:
        seleccion = st.multiselect("🏢 Empresas", list(EMPRESAS), default=list(EMPRESAS))   # elegir varias
    with f2:
        anios = st.slider("📅 Período (años)", 1, 10, 1)                                    # deslizador
    with f3:
        ventana = st.radio("〰️ Media móvil (sesiones)", [20, 50, 100], horizontal=True)    # elegir una
    with f4:
        oscuro = st.toggle("🌙 Modo oscuro", value=False)                                   # interruptor

T = TEMAS["oscuro" if oscuro else "claro"]                  # paleta activa
colores = {n: T[i["ticker"]] for n, i in EMPRESAS.items()}  # color de cada empresa
periodo = f"{anios} año" + ("s" if anios > 1 else "")       # "1 año" / "3 años"

# --- 5. Estilos (CSS) ---
# Variables de color que cambian con el tema
variables = (f":root{{--bg:{T['bg']};--card:{T['card']};--texto:{T['texto']};--gris:{T['gris']};"
             f"--borde:{T['borde']};--h1:{T['h1']};--h2:{T['h2']};}}")
CSS = """
#MainMenu, footer, header[data-testid="stHeader"] {visibility:hidden; height:0;}
.block-container {padding-top:1.2rem; max-width:1200px;}
.stApp {background:var(--bg); color:var(--texto);}
[data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p, [data-baseweb="tab"] p,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] p {color:var(--texto);}
[data-testid="stCaptionContainer"] * {color:var(--gris);}
[data-baseweb="select"] > div, [data-baseweb="base-input"], [data-baseweb="input"] {background:var(--card); border-color:var(--borde);}
[data-baseweb="select"] *, input {color:var(--texto);}
[data-baseweb="popover"] ul, [data-baseweb="menu"] {background:var(--card);}
.st-key-filtros {background:var(--card); border:1px solid var(--borde); border-radius:18px; padding:8px 14px;}
/* Banner */
.hero {display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:nowrap; padding:34px 40px;
       border-radius:24px; color:#fff; background:linear-gradient(120deg,var(--h1),var(--h2));
       border:1px solid var(--borde); margin-bottom:14px;}
.hero-tag {font-size:12px; letter-spacing:.18em; color:#7DD3FC; font-weight:700;}
.hero h1 {margin:6px 0 8px 0; font-size:42px; line-height:1.1; color:#fff; padding:0;}
.hero h1 a {display:none;}
.hero p {margin:0 0 16px 0; font-size:17px; color:#CBD5E1;}
.chips span {display:inline-block; margin:0 8px 6px 0; padding:6px 14px; border-radius:999px; font-weight:600;
             font-size:14px; color:#fff; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.25);}
.hero > div {flex:1 1 0; min-width:0;}
.hero > svg {flex:0 0 390px; width:390px; height:auto;}
/* Tarjetas */
.kpi, .emp, .rk-card {background:var(--card); border:1px solid var(--borde); border-radius:18px;
                      box-shadow:0 4px 16px rgba(0,0,0,.15);}
.kpi {padding:18px 20px; height:100%;}
.kpi-ico {font-size:26px;}
.kpi-tit {font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--gris); font-weight:700; margin-top:6px;}
.kpi-val {font-size:26px; font-weight:800; line-height:1.2;}
.kpi-sub {font-size:13px; color:var(--gris);}
.emp {padding:20px; overflow:hidden; position:relative;}
.emp-top {position:absolute; left:0; top:0; right:0; height:6px;}
.emp-cab {display:flex; align-items:center; gap:12px; margin-top:4px;}
.emp-ico, .rk-ico {border-radius:50%; display:flex; align-items:center; justify-content:center;}
.emp-ico {width:50px; height:50px; font-size:26px;}
.emp-nom {font-size:19px; font-weight:800; line-height:1.1;}
.emp-tic, .rk-tick {font-size:12px; color:var(--gris); font-weight:600;}
.emp-precio {font-size:32px; font-weight:800; color:var(--texto); margin:14px 0 6px 0;}
.emp-vol {font-size:13px; color:var(--gris); margin-top:8px;}
.pill {display:inline-block; padding:5px 12px; border-radius:999px; font-weight:700; font-size:14px;}
.sec {font-size:22px; font-weight:800; color:var(--texto); margin:30px 0 4px 0;}
.sec-sub {font-size:14px; color:var(--gris); margin-bottom:12px;}
/* Ranking */
.rk-head, .rk-card {display:grid; grid-template-columns:56px 2.2fr 1.3fr 1.4fr 2fr 1fr; gap:12px; align-items:center;}
.rk-head {padding:0 18px 6px 18px; font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--gris);}
.rk-card {padding:16px 18px; margin-bottom:12px; color:var(--texto);}
.rk-pos {font-size:28px; text-align:center;}
.rk-emp {display:flex; align-items:center; gap:12px;}
.rk-ico {width:46px; height:46px; font-size:24px;}
.rk-name {font-weight:800; font-size:17px; line-height:1.1;}
.rk-precio {font-weight:800; font-size:17px;}
.rk-track {height:10px; border-radius:999px; background:var(--borde); overflow:hidden;}
.rk-bar {height:100%; border-radius:999px; background:linear-gradient(90deg,#FDE68A,#F59E0B);}
.rk-vol {font-size:13px; font-weight:700; margin-bottom:5px;}
/* Celular */
@media (max-width:800px) {.hero{flex-wrap:wrap;} .hero > svg{flex:1 1 100%; width:100%;} .rk-head{display:none;} .rk-card{grid-template-columns:1fr 1fr;} .hero h1{font-size:30px;}}
"""
st.markdown(f"<style>{variables}{CSS}</style>", unsafe_allow_html=True)

# --- 6. Banner con ilustración (dibujo SVG) ---
def suave(pts):
    # Une los puntos con una curva suave
    d = f"M{pts[0][0]},{pts[0][1]}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d += f" C{(x0 + x1) / 2},{y0} {(x0 + x1) / 2},{y1} {x1},{y1}"
    return d

azul = [(72, 175), (134, 137), (193, 154), (245, 126), (294, 90), (349, 108), (385, 83)]   # puntos curva azul
morado = [(73, 207), (125, 171), (191, 189), (240, 177), (303, 143), (385, 136)]           # puntos curva morada
nodos = "".join(f'<circle cx="{x}" cy="{y}" r="7.5" fill="#fff" stroke="{c}" stroke-width="3.5"/>'
                for pts, c in [(azul[:-1], "#38BDF8"), (morado[:-1], "#C084FC")] for x, y in pts)   # círculos sobre las curvas
barras = "".join(
    f'<rect x="{x}" y="{248 - h}" width="{w}" height="{h}" rx="8" fill="#fff" fill-opacity=".22" stroke="#fff" stroke-opacity=".55" stroke-width="1.5"/>'
    f'<rect x="{x + 5}" y="{252 - h}" width="{w / 4:.0f}" height="{h - 10}" rx="3" fill="#fff" fill-opacity=".4"/>'
    for x, w, h in [(72, 30, 20), (109, 38, 33), (155, 43, 41), (209, 41, 50), (260, 36, 60), (304, 35, 70), (349, 41, 80)])   # barras (x, ancho, alto)
estrella = lambda x, y: (f'<path transform="translate({x},{y})" d="M0,-9 Q0,0 9,0 Q0,0 0,9 Q0,0 -9,0 Q0,0 0,-9Z" '
                         'fill="#fff" stroke="#BAE6FD" stroke-width="1.5"/>')   # estrellita
puntos = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{g})"/>'
                 for x, y, r, g in [(100, 128, 6, "az"), (360, 66, 8, "az"), (462, 132, 8, "mo"), (46, 190, 8, "az"), (398, 236, 8, "mo")])   # puntos decorativos
ilustracion = (
    '<svg viewBox="0 0 480 270" xmlns="http://www.w3.org/2000/svg"><defs>'
    '<linearGradient id="fondo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FBFDFF"/><stop offset="1" stop-color="#DCEEFC"/></linearGradient>'
    '<linearGradient id="az" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E0F2FE"/><stop offset="1" stop-color="#7DD3FC"/></linearGradient>'
    '<linearGradient id="mo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F5D0FE"/><stop offset="1" stop-color="#C084FC"/></linearGradient>'
    '<linearGradient id="barra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7DD3FC"/><stop offset="1" stop-color="#8B9CF8"/></linearGradient>'
    '<linearGradient id="areaA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".32"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>'
    '<linearGradient id="areaM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9D5FF" stop-opacity=".35"/><stop offset="1" stop-color="#E9D5FF" stop-opacity=".03"/></linearGradient></defs>'
    f'<path d="{suave(azul)} L385,248 L72,248 Z" fill="url(#areaA)"/><path d="{suave(morado)} L385,248 L73,248 Z" fill="url(#areaM)"/>'
    '<rect x="55" y="248" width="370" height="8" rx="4" fill="url(#az)"/>'
    f'{barras}'
    f'<path d="{suave(azul)} L440,38" fill="none" stroke="url(#az)" stroke-width="6" stroke-linecap="round"/>'
    '<polygon points="460,22 449,49 431,27" fill="#BAE6FD" stroke="#BAE6FD" stroke-width="4" stroke-linejoin="round"/>'
    f'<path d="{suave(morado)} L447,101" fill="none" stroke="url(#mo)" stroke-width="5" stroke-linecap="round"/>'
    '<polygon points="463,92 451,109 442,93" fill="#E9D5FF" stroke="#E9D5FF" stroke-width="3" stroke-linejoin="round"/>'
    f'{nodos}'
    '<rect x="60" y="34" width="132" height="76" rx="18" fill="#fff" fill-opacity=".14" stroke="#BAE6FD" stroke-width="2"/>'
    '<g transform="rotate(-90 98 72)" fill="none" stroke-width="11"><circle cx="98" cy="72" r="20" stroke="#7DD3FC" stroke-dasharray="84 42"/>'
    '<circle cx="98" cy="72" r="20" stroke="#E9D5FF" stroke-dasharray="38 88" stroke-dashoffset="-84"/></g>'
    '<g fill="#BAE6FD"><circle cx="138" cy="52" r="4"/><circle cx="138" cy="72" r="4" fill="#E9D5FF"/><circle cx="138" cy="92" r="4"/></g>'
    '<g fill="#fff" fill-opacity=".9"><rect x="148" y="48" width="34" height="8" rx="4"/><rect x="148" y="68" width="34" height="8" rx="4"/><rect x="148" y="88" width="34" height="8" rx="4"/></g>'
    '<rect x="206" y="44" width="52" height="38" rx="11" fill="#fff" fill-opacity=".14" stroke="#BAE6FD" stroke-width="2"/>'
    '<g fill="#fff"><rect x="217" y="63" width="8" height="12" rx="2"/><rect x="230" y="57" width="8" height="18" rx="2"/><rect x="243" y="51" width="8" height="24" rx="2"/></g>'
    '<path d="M258,56 C300,38 305,64 296,86" fill="none" stroke="#BAE6FD" stroke-width="2"/>'
    '<path d="M45,147 L72.6,151.9 A28,28 0 1 1 45,119 Z" fill="url(#az)"/>'
    '<path transform="translate(4,-4)" d="M45,147 L45,119 A28,28 0 0 1 67.9,130.9 Z" fill="url(#mo)"/>'
    '<path transform="translate(5,0)" d="M45,147 L67.9,130.9 A28,28 0 0 1 72.6,151.9 Z" fill="#DBEAFE" stroke="#BFDBFE" stroke-width="1.5"/>'
    '<rect x="410" y="146" width="44" height="52" rx="9" fill="url(#az)" fill-opacity=".3" stroke="#BAE6FD" stroke-width="2"/>'
    '<rect x="398" y="184" width="74" height="48" rx="13" fill="#fff" fill-opacity=".16" stroke="#BAE6FD" stroke-width="2"/>'
    '<path d="M408,206 q7,-14 14,0 t14,0 t14,-6" fill="none" stroke="#E9D5FF" stroke-width="3" stroke-linecap="round"/>'
    '<rect x="408" y="217" width="40" height="4" rx="2" fill="#fff" fill-opacity=".5"/>'
    f'{puntos}{estrella(243, 103)}{estrella(387, 57)}</svg>')

with banner:   # llena el espacio reservado arriba
    st.markdown(
        '<div class="hero"><div><div class="hero-tag">MERCADO DE VALORES · EE. UU.</div>'
        '<h1>📈 ANÁLISIS FINANCIERO</h1>'      # <- título grande
        '<p>Compara el rendimiento y el riesgo de tres marcas que conoces.</p>'
        '<div class="chips"><span>🥤 Coca-Cola · KO</span><span>🍔 McDonald\'s · MCD</span><span>🏰 Disney · DIS</span></div>'
        f'</div>{ilustracion}</div>', unsafe_allow_html=True)

# --- 7. Descarga de precios ---
@st.cache_data(ttl=3600, show_spinner=False)   # guarda el resultado 1 hora (más rápido)
def consultar_precios(ticker, anios):
    inicio = pd.Timestamp.today().normalize() - pd.DateOffset(years=anios)   # fecha de inicio
    return yf.Ticker(ticker).history(start=inicio, auto_adjust=True)

if not seleccion:
    st.info("Selecciona al menos una empresa para ver el análisis.")
    st.stop()   # detiene la app

series = {}   # aquí van los precios de cada empresa
with st.spinner("Descargando precios..."):
    for nombre in seleccion:
        try:
            hist = consultar_precios(EMPRESAS[nombre]["ticker"], anios)
            if not hist.empty and "Close" in hist:
                s = hist["Close"].dropna()                # precio de cierre sin huecos
                s.index = s.index.tz_localize(None)       # quita zona horaria
                if len(s) >= 2:
                    series[nombre] = s.rename(nombre)
        except Exception:
            st.warning(f"No se pudieron consultar los datos de {nombre}.")

if not series:
    st.error("No hay datos disponibles. Intenta de nuevo más tarde.")
    st.stop()

precios = pd.concat(series.values(), axis=1).sort_index().dropna(how="any")   # una tabla con fechas comunes
if len(precios) < 2:
    st.warning("No hay suficientes fechas comunes para comparar.")
    st.stop()

# --- 8. Cálculos ---
rend_diarios = precios.pct_change().dropna()   # cambio % de cada día
resumen = pd.DataFrame({
    "Último cierre (USD)": precios.iloc[-1],                                     # precio del último día
    "Rendimiento (%)": (precios.iloc[-1] / precios.iloc[0] - 1) * 100,           # ganancia total del período
    "Volatilidad anual (%)": rend_diarios.std() * np.sqrt(252) * 100,            # riesgo (252 días de bolsa al año)
}).round(2)

def pastilla(texto, c):
    # Etiqueta redondeada de color
    return f'<span class="pill" style="background:{c}2E;color:{c};">{texto}</span>'

# --- 9. Tarjetas resumen ---
def tarjeta_kpi(icono, titulo, valor, sub, color=None):
    color = color or T["texto"]
    return (f'<div class="kpi"><div class="kpi-ico">{icono}</div><div class="kpi-tit">{titulo}</div>'
            f'<div class="kpi-val" style="color:{color};">{valor}</div><div class="kpi-sub">{sub}</div></div>')

mejor = resumen["Rendimiento (%)"].idxmax()          # empresa que más ganó
seguro = resumen["Volatilidad anual (%)"].idxmin()   # empresa menos riesgosa
prom = resumen["Rendimiento (%)"].mean()             # rendimiento promedio
k1, k2, k3, k4 = st.columns(4)
k1.markdown(tarjeta_kpi("🏆", "Mejor rendimiento", mejor, f"{resumen.loc[mejor, 'Rendimiento (%)']:+.2f}% en {periodo}", colores[mejor]), unsafe_allow_html=True)
k2.markdown(tarjeta_kpi("🛡️", "Menor volatilidad", seguro, f"{resumen.loc[seguro, 'Volatilidad anual (%)']:.2f}% anual", colores[seguro]), unsafe_allow_html=True)
k3.markdown(tarjeta_kpi("📊", "Rendimiento promedio", f"{prom:+.2f}%", f"entre {len(resumen)} empresas", VERDE if prom >= 0 else ROJO), unsafe_allow_html=True)
k4.markdown(tarjeta_kpi("🗓️", "Datos analizados", f"{len(precios):,} días",
                        f"{precios.index[0]:%d/%m/%Y} a {precios.index[-1]:%d/%m/%Y}"), unsafe_allow_html=True)

# --- 10. Tarjeta de cada empresa ---
st.markdown('<div class="sec">Tus empresas</div><div class="sec-sub">Precio actual, rendimiento y recorrido del precio.</div>',
            unsafe_allow_html=True)

def minigrafico(serie, color):
    # Línea pequeña con el recorrido del precio (máx. 120 puntos)
    pos = np.linspace(0, len(serie) - 1, min(len(serie), 120)).astype(int)
    v = serie.values[pos]
    xs = np.linspace(0, 200, len(v))
    ys = 4 + (1 - (v - v.min()) / ((v.max() - v.min()) or 1)) * 42   # ajusta el alto
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f'<svg viewBox="0 0 200 50" preserveAspectRatio="none" style="width:100%;height:60px;">'
            f'<polygon points="0,50 {pts} 200,50" fill="{color}" fill-opacity=".15"/>'
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.5" vector-effect="non-scaling-stroke"/></svg>')

for col, nombre in zip(st.columns(len(precios.columns)), precios.columns):   # una tarjeta por empresa
    c, r = colores[nombre], resumen.loc[nombre, "Rendimiento (%)"]
    col.markdown(
        f'<div class="emp"><div class="emp-top" style="background:{c};"></div>'
        f'<div class="emp-cab"><div class="emp-ico" style="background:{c}26;">{EMPRESAS[nombre]["icono"]}</div>'
        f'<div><div class="emp-nom" style="color:{c};">{nombre}</div><div class="emp-tic">{EMPRESAS[nombre]["ticker"]}</div></div></div>'
        f'<div class="emp-precio">USD {resumen.loc[nombre, "Último cierre (USD)"]:,.2f}</div>'
        f'{pastilla(("▲" if r >= 0 else "▼") + f" {r:+.2f}% en {periodo}", VERDE if r >= 0 else ROJO)}'   # verde sube, roja baja
        f'{minigrafico(precios[nombre], c)}'
        f'<div class="emp-vol">Volatilidad anual: <b>{resumen.loc[nombre, "Volatilidad anual (%)"]:.2f}%</b></div></div>',
        unsafe_allow_html=True)

# --- 11. Gráficos ---
st.markdown('<div class="sec">Gráficos</div><div class="sec-sub">Pasa el mouse, haz zoom arrastrando o usa el deslizador de abajo.</div>',
            unsafe_allow_html=True)

def estilo(fig, eje_y=None):
    # Mismo aspecto para todos los gráficos
    fig.update_layout(template=T["plotly"], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font_color=T["texto"], hovermode="x unified", legend_title_text="",
                      margin=dict(l=10, r=10, t=30, b=10), height=430)
    fig.update_xaxes(gridcolor=T["borde"], title=None)
    fig.update_yaxes(gridcolor=T["borde"], title=eje_y)
    return fig

t1, t2, t3, t4, t5, t6 = st.tabs(["💯 Base 100", "💵 Precios", "〰️ Tendencia", "⚖️ Riesgo vs rendimiento", "🔗 Correlación", "🧮 Simulador"])

with t1:   # Base 100
    st.write("Evolución de **100 dólares invertidos al inicio**: permite comparar acciones de precios distintos.")
    base100 = precios.div(precios.iloc[0]).mul(100)   # todas arrancan en 100
    st.plotly_chart(estilo(px.line(base100, color_discrete_map=colores), "Base 100"))

with t2:   # Precios
    st.write("Precio de cierre en USD. Usa el **deslizador inferior** para acercarte a un rango de fechas.")
    fig = estilo(px.line(precios, color_discrete_map=colores), "USD")
    fig.update_xaxes(rangeslider_visible=True)   # barra para elegir fechas
    st.plotly_chart(fig)

with t3:   # Tendencia
    ver_real = st.checkbox("Mostrar también el precio real (línea punteada)", value=True)
    st.write(f"Media móvil de {ventana} sesiones: suaviza el precio para ver la tendencia.")
    fig = estilo(px.line(precios.rolling(ventana).mean(), color_discrete_map=colores), "USD")   # promedio de los últimos N días
    if ver_real:
        for c in precios.columns:
            fig.add_scatter(x=precios.index, y=precios[c], mode="lines", showlegend=False, opacity=.5,
                            line=dict(color=colores[c], width=1, dash="dot"), name=f"{c} (precio)")
    st.plotly_chart(fig)

with t4:   # Riesgo vs rendimiento
    st.write("Izquierda: cuánto ganó cada empresa. Derecha: qué tanto se movió su precio (riesgo). "
             "Lo ideal es barra **alta** en rendimiento y **baja** en volatilidad.")
    datos = resumen.reset_index().rename(columns={"index": "Empresa"})
    for caja, campo, tit in zip(st.columns(2), ["Rendimiento (%)", "Volatilidad anual (%)"],
                                ["📈 Rendimiento del período", "🎢 Volatilidad anual (riesgo)"]):   # un gráfico por columna
        fig = px.bar(datos, x="Empresa", y=campo, color="Empresa", text=campo, color_discrete_map=colores)
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside", cliponaxis=False, marker_cornerradius=10)
        fig = estilo(fig).update_layout(title=tit, showlegend=False, hovermode="closest", height=390)
        caja.plotly_chart(fig)

with t5:   # Correlación
    if len(precios.columns) > 1:
        st.write("Correlación de rendimientos diarios (de -1 a +1). Más verde = se mueven más juntas.")
        fig = px.imshow(rend_diarios.corr(), text_auto=".2f", zmin=-1, zmax=1,
                        color_continuous_scale=[ROJO, T["card"], VERDE])   # mapa de calor
        st.plotly_chart(estilo(fig).update_layout(height=380, hovermode="closest"))
        st.caption("Correlación alta = tienden a moverse juntas. No implica causalidad.")
    else:
        st.info("Selecciona al menos dos empresas para ver la correlación.")

with t6:   # Simulador
    st.write("¿Cuánto tendrías hoy si hubieras invertido al inicio del período elegido?")
    s1, s2 = st.columns(2)
    monto = s1.number_input("💰 Monto a invertir (USD)", min_value=100, value=1000, step=100)
    reparto = s2.radio("Cómo repartirlo", ["Ese monto en cada empresa", "Dividir el monto entre las empresas"])
    por_empresa = monto if reparto.startswith("Ese") else monto / len(precios.columns)   # cuánto va a cada una
    factor = precios.iloc[-1] / precios.iloc[0]   # cuántas veces creció cada acción
    final = factor * por_empresa                  # valor final
    for col, nombre in zip(st.columns(len(final)), final.index):
        col.metric(f"{EMPRESAS[nombre]['icono']} {nombre}", f"USD {final[nombre]:,.2f}", f"{final[nombre] - por_empresa:+,.2f} USD")
    st.metric("🧾 Total", f"USD {final.sum():,.2f}", f"{final.sum() - por_empresa * len(final):+,.2f} USD")

# --- 12. Ranking ---
st.markdown('<div class="sec">Ranking comparativo</div><div class="sec-sub">Ordena las empresas por el dato que prefieras.</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])
orden_col = c1.selectbox("Ordenar ranking por", ["Rendimiento (%)", "Volatilidad anual (%)", "Último cierre (USD)"])
sentido = c2.radio("Orden", ["Mayor a menor", "Menor a mayor"], horizontal=True)

tabla = resumen.reset_index().rename(columns={"index": "Empresa"})
tabla = tabla.sort_values(orden_col, ascending=(sentido == "Menor a mayor")).reset_index(drop=True)   # ordena
v_max = max(tabla["Volatilidad anual (%)"].max(), 0.01)   # sirve para el largo de las barras

def nivel_riesgo(v):
    # Bajo (<20), Medio (20 a 30), Alto (>30)
    return ("Bajo", VERDE) if v < 20 else ("Medio", AMBAR) if v < 30 else ("Alto", ROJO)

html = ['<div class="rk-head"><div></div><div>Empresa</div><div>Último cierre</div><div>Rendimiento</div>'
        '<div>Volatilidad anual</div><div>Riesgo</div></div>']
for i, f in tabla.iterrows():   # una fila del ranking por empresa
    n, c, r, vol = f["Empresa"], colores[f["Empresa"]], f["Rendimiento (%)"], f["Volatilidad anual (%)"]
    txt, col_r = nivel_riesgo(vol)
    html.append(
        f'<div class="rk-card" style="border-left:6px solid {c};"><div class="rk-pos">{["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"}</div>'
        f'<div class="rk-emp"><div class="rk-ico" style="background:{c}26;">{EMPRESAS[n]["icono"]}</div>'
        f'<div><div class="rk-name" style="color:{c};">{n}</div><div class="rk-tick">{EMPRESAS[n]["ticker"]}</div></div></div>'
        f'<div class="rk-precio">USD {f["Último cierre (USD)"]:,.2f}</div>'
        f'<div>{pastilla(("▲" if r >= 0 else "▼") + f" {r:+.2f}%", VERDE if r >= 0 else ROJO)}</div>'
        f'<div><div class="rk-vol">{vol:.2f}%</div><div class="rk-track"><div class="rk-bar" style="width:{max(6, vol / v_max * 100):.0f}%;"></div></div></div>'
        f'<div>{pastilla(txt, col_r)}</div></div>')
st.markdown("".join(html), unsafe_allow_html=True)

# --- 13. Tabla y descarga ---
if st.checkbox("📋 Ver tabla de precios de cierre"):
    st.dataframe(precios.round(2))
st.download_button("⬇️ Descargar datos (CSV)", data=tabla.to_csv(index=False).encode("utf-8-sig"),
                   file_name="resumen_acciones.csv", mime="text/csv")
st.caption("Riesgo según volatilidad anual: Bajo (<20%) · Medio (20% a 30%) · Alto (>30%), valores de referencia. "
           "Fuente: Yahoo Finance vía yfinance. Datos históricos; no son recomendación de inversión.")
