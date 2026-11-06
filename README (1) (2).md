# Proyecto de analítica financiera \| IX Concurso ITM 2026

> **Plantilla de trabajo para estudiantes.** Crea una copia de este archivo en el repositorio de tu equipo y reemplaza los textos entre corchetes. Conserva las preguntas como apoyo durante la investigación. No publiques claves de acceso ni información privada.

**Curso:** Lenguajes de Programación · Ingeniería Financiera  
**Concurso:** 12 de noviembre de 2026  
**Simulacro:** 10 de noviembre de 2026  
**Tecnología:** \[Python \+ Streamlit \]

## 1\. Identificación del proyecto

- **Nombre de la aplicación:** Alpha Analytics  
- **Equipo e integrantes:** Valeria Muñoz, Isabela Montoya, Estefania Amaya   
- **Enlace a la aplicación:** \[Pendiente / URL\]  
- **Repositorio del proyecto:** \[URL\]  
- **Última actualización:** \[AAAA-MM-DD\]

## 2\. ¿Qué queremos investigar? · S25

**Investiga:** ¿qué significa analizar el comportamiento histórico de un activo financiero? ¿Qué preguntas pueden responderse con datos de mercado y cuáles no?

* Analizar el comportamiento histórico de un activo financiero consiste en estudiar cómo han evolucionado, a lo largo del tiempo, su precio y otras variables de mercado, como el volumen de negociación, los dividendos y la volatilidad. El propósito es identificar patrones, tendencias, relaciones con otras variables y niveles de riesgo que permitan comprender su desempeño pasado y apoyar decisiones mejor fundamentadas. Este análisis describe lo que ocurrió, pero no garantiza que se repita en el futuro.   
* Que preguntas si podemos responder: Son las que se pueden medir y verificar con series históricas de precios, rendimientos y otras variables cuantificables. Por ejemplo:  
  ¿Qué rentabilidad obtuvo la acción en los últimos 12 meses?  
  ¿Qué tan volátil fue frente a otros activos o frente al índice del mercado?  
  ¿Cuál fue su caída máxima (*drawdown*) en un periodo determinado?  
    
* Que preguntas no podríamos responder: Son las que dependen de causas, valoraciones personales o hechos futuros que los precios históricos no revelan por sí solos, por ejemplo: ¿Por qué cayó el precio de una acción? El precio muestra la caída, pero no necesariamente su causa, ¿Es una buena inversión para cualquier persona? Depende de los objetivos, horizonte y tolerancia al riesgo del inversionista.

- **Situación o fenómeno de interés:** El comportamiento financiero de Coca-Cola (KO), Disney (DIS) y McDonald’s (MCD), y cómo han cambiado sus acciones y resultados a lo largo del tiempo.   
- **Pregunta principal:** ¿Cómo variaron los precios de las acciones y los ingresos de KO, DIS y MCD durante la última década y cuál mostró el desempeño más estable?   
- **Objetivo del análisis:** Comparar la evolución histórica de los precios y los ingresos de las tres empresas, describir sus tendencias y cambios, e identificar cuál tuvo un desempeño más estable en el período estudiado.   
- **Importancia financiera:** El análisis permite observar cómo empresas de distintos sectores (bebidas, entretenimiento y restaurantes) han respondido a cambios económicos y del mercado. También sirve para practicar la interpretación de datos financieros y para aprender a fundamentar conclusiones con evidencia histórica, sin asumir que el desempeño pasado garantiza resultados futuros.   
- **Preguntas complementarias:** ¿Qué factores propios de cada sector podrían ayudar a explicar las diferencias observadas entre Coca-Cola, Disney y McDonald’s? 

>   
> **Comprueba:** ¿tu pregunta identifica activos, variables y un período de estudio? ¿Es posible responderla con datos disponibles?

## 3\. Activos, datos y alcance · S25

**Investiga:** ¿qué activos se ajustan a tu pregunta? ¿qué datos históricos existen? ¿qué frecuencia, período y fuente utilizarás?

| Activo | Símbolo o ticker | Tipo | Razón para incluirlo |
| :---- | :---- | :---- | :---- |
| Disney  | \[DIS\] | \[Acción (Sector Consumo Discrecional / Entretenimiento)\]  | \[Tiene marcas muy fuertes (Marvel, Pixar, Star Wars) que generan ingresos por muchos lados: parques, cine y streaming. \] |
| Mcdonald's  | \[MCD\] | \[Acción (Sector Consumo Discrecional) \] | \[Es una de las franquicias más grandes del mundo, con presencia en más de 100 países \] |
| Coca-Cola | \[KO\] | \[Acción (Sector Consumo Masivo / Defensivo) \] | \[Marca global que la gente consume todos los días, incluso en épocas de crisis \]  |

- **Fuente de datos:** \[Yahoo\! Finance, claude, Chat GPT\]  
- **Período:** \[DIS 1985 – 2026\]  \[MCD 1985 – 2026\] \[KO  1985 – 2026\]   
- **Frecuencia:** \[Anual\]  
- **Variables disponibles:** \[Fecha, Precio de apertura, Precio máximo, Precio mínimo, Precio de cierre, Cierre ajustado, ingresos totales\]   
- **Limitaciones de los datos:** \[diferencias de mercado.\]

**Primera prueba:** \[Enlace al notebook o archivo que descarga o consulta datos; indica qué funcionó y qué no\]

## 4\. Metodología de análisis · S25–S26

**Investiga:** ¿qué indicadores permiten responder la pregunta principal? ¿cómo se calculan? ¿qué interpretación y limitaciones tienen?

| Indicador / técnica | ¿Qué mide? | ¿Por qué lo necesitamos? | Implementación |
| :---- | :---- | :---- | :---- |
| 1\. Retorno Porcentual / Rentabilidad Histórica  | Mide el cambio porcentual del precio de cierre de un periodo a otro (${P}_{t}/{P}_{t-1}-1$)  | Permite evaluar la ganancia o pérdida generada por invertir a largo plazo en DIS, MCD y KO.  | \[pct\_change() en Python  |
| 2\. Volatilidad (Desviación Estándar)  | Mide la dispersión o variabilidad de los rendimientos de la acción frente a su media histórica.  | Cuantifica y compara el nivel de riesgo financiero entre las tres multinacionales.  | \[np.std() / Función EST.DESV\]  |
| 3\. Rendimiento por Dividendo  | El porcentaje que la empresa paga en dividendos respecto al precio actual de la acción.  | Es esencial en empresas maduras y defensivas como **Coca-Cola (KO)** y **McDonald's (MCD)** para evaluar flujos de efectivo al inversor.  | \[Módulo de dividendos en Python (Ticker.dividends)\]  |

No es necesario utilizar todos los indicadores estudiados en clase. Selecciona y justifica únicamente los pertinentes.

### Visualizaciones previstas

| Gráfico | Pregunta que ayuda a responder | Variables | Interpretación esperada |
| :---- | :---- | :---- | :---- |
| Precio normalizado (base 100\)  | ¿Cuál de las tres acciones creció más desde un mismo punto de partida y cómo evolucionó cada una en el tiempo?  | Fecha (eje X); precio de cierre ajustado de KO, DIS y MCD, convertido a base 100 (eje Y)  | La línea más alta al final del periodo indica el mayor rendimiento acumulado. Las líneas que se separan o se cruzan muestran cuándo una acción tomó ventaja sobre las otras |
| Drawdown (caída desde máximos)  | ¿Cuánto llegó a caer cada acción desde su pico anterior y cuánto tardó en recuperarse?  | Fecha (eje X); porcentaje de caída respecto al máximo histórico previo (eje Y)  | Las caídas más profundas y prolongadas indican mayor riesgo de pérdida.   |
| Volatilidad móvil (ventana de 90 días)  | ¿Cómo cambió el riesgo de cada acción a lo largo del tiempo y en qué momentos aumentó?  | Fecha (eje X); desviación estándar anualizada de los rendimientos diarios en una ventana de 90 días (eje Y)  | Los picos señalan periodos de incertidumbre o estrés del mercado.  |
| Mapa de calor de correlaciones  | ¿Qué tan parecido es el comportamiento de las tres acciones entre sí?  | Matriz de correlación, valores de \-1 a 1\) | Valores cercanos a 1 indican que las acciones se mueven juntas y diversifican poco. Valores bajos indican mayor diversificación. |

**Primer resultado verificable:** \[Enlace a un cálculo o gráfico realizado con datos reales y una interpretación breve\]

## 5\. Diseño de la aplicación · S25

**Investiga:** ¿cómo se construyen controles, gráficos y métricas con la herramienta elegida? ¿qué sucede cuando el usuario modifica una selección?

- **Usuarios previstos:** Estudiantes, docentes y personas interesadas en los mercados financieros que deseen consultar, comparar e interpretar el comportamiento histórico de las tres empresas.  
    
- **Entradas y filtros:** Activos: Coca-Cola (KO), Disney (DIS) y McDonald's (MCD).  
  Periodo: últimos diez años (2016-2025).  
  Frecuencia: mensual para precios y anual para ingresos.  
  Variables: precios históricos, ingresos, rentabilidad y volatilidad.  
  Comparación: selección individual o conjunta de las tres empresas.  
    
- **Secciones de la interfaz:** Pantalla principal: Resumen de las tres empresas y principales indicadores. Comparación de precios: Gráfico de precios normalizados con base 100. Análisis de riesgo: Volatilidad y Maximum Drawdown. Conclusiones:Comparación de estabilidad y explicación de resultados.  
- **Resultados visibles:** Gráficos de líneas para comparar precios e ingresos.  
  Tarjetas con indicadores de rentabilidad y volatilidad.  
  Tablas comparativas entre las empresas.  
  Explicaciones automáticas sobre los resultados.  
  Identificación de la empresa con mayor estabilidad histórica.  
    
- **Interacción principal:** El usuario podrá modificar los activos seleccionados, el periodo y la frecuencia de los datos:  
    
  Cuando cambie una selección:  
* Se actualizarán los datos correspondientes  
* Se recalcularán los indicadores financieros   
* Los gráficos mostrarán únicamente los activos y periodos seleccionados.  
* Las tablas comparativas cambiarán automáticamente.  
* Las conclusiones se adaptarán a los nuevos resultados.


  
**Flujo previsto:**  
Selección de activos y parámetros → Obtención de datos → Preparación y cálculos → Visualización → Interpretación.

**Boceto o esquema:** \[Inserta una imagen o enlace al diseño, por ejemplo `docs/boceto.png`\]

**Decisión técnica:** ¿Por qué usarás Python o R y qué biblioteca de aplicación elegiste?  
R// Usaremos Python Porque es un lenguaje potente, rápido y automatizado ideal para procesar grandes volúmenes de series de tiempo financieras históricas 

## 6\. Construcción y pruebas · S26 (5 de noviembre)

Actualiza esta sección durante el laboratorio de desarrollo.

- **Componentes implementados:**   
  **Descarga de datos:** La app se conecta solita a internet (usando Yahoo Finance) para traer los precios y datos históricos de las acciones de Coca-Cola, McDonald's y Disney.  
  **Cálculos matemáticos:** El sistema hace las operaciones en Python para calcular cuánto subieron o bajaron las acciones (rendimientos) y qué tan riesgosas o inestables han sido (volatilidad).  
  **Pantalla interactiva:** Diseñamos una página web muy fácil de usar con streamlit donde puedes ver gráficos en movimiento y mover filtros de fechas.  
    
- **Cómo ejecutar la aplicación:**Para ejecutar la aplicación, el equipo se encarga de conectar el sistema a las fuentes de datos financieras en línea y procesar la información de forma automática. Primero, se prepara el espacio de trabajo en el computador para asegurar que todas las herramientas y librerías necesarias queden debidamente organizadas. A continuación, se instalan los componentes de software requeridos para el análisis de los datos. Por último, se pone en marcha la interfaz interactiva mediante un servidor local, lo que permite navegar visualmente por las gráficas, consultar el comportamiento histórico de las acciones y revisar los resultados de manera dinámica y sencilla.   
- **Dependencias:**El funcionamiento del proyecto se sustenta en diversas herramientas tecnológicas y librerías especializadas que trabajan de la mano. Entre los componentes principales destacan herramientas como Streamlit para el desarrollo y diseño de la interfaz visual e interactiva, además de librerías de procesamiento y análisis de datos financieros que permiten gestionar la información de las acciones de forma automatizada y garantizar la estabilidad general de la aplicación en el entorno de pruebas.   
- **Pruebas realizadas:** Consulta de precios históricos de KO, DIS y MCD, Obtener y organizar correctamente los datos financieros de cada empresa, Se estableció la estructura de consulta y análisis de los datos, identificando las variables necesarias para realizar comparaciones y generar gráficos.   
- **Errores conocidos y cómo se resolvieron:** Errores que se podrían presentar con la consulta y organización de los datos históricos. Se propone solucionarlas mediante Python, verificando fechas, datos faltantes y formatos para facilitar la comparación de las tres empresas   
- **Pendientes antes del simulacro:** Finalizar la descarga y organización de los datos financieros, completar los cálculos e indicadores, terminar los gráficos comparativos, verificar el funcionamiento de los filtros y las actualizaciones de la aplicación, realizar pruebas generales, corregir posibles errores y preparar la presentación de los resultados.

>   
> No afirmes que una función está implementada si aún no ha sido probada.

## 7\. Hallazgos e interpretación · S26–S28

Para cada hallazgo importante, registra:

1. **Evidencia:** Precio normalizado base 100, drawdown, volatilidad móvil, mapa de calor de correlaciones, volatilidad anualizada.  
2. **Qué muestra:** La evolución de los precios de las acciones y sus cambios a lo largo del tiempo, descripción objetiva del comportamiento.  
3. **Interpretación financiera:** Explica qué implica en términos de rendimiento, riesgo o diversificación.   
4. **Limitaciones:** El periodo incluye eventos atípicos (pandemia, inflación alta, subida de tasas) que pueden no repetirse y distorsionar las conclusiones, el desempeño pasado no garantiza resultados futuros, los datos muestran qué ocurrió, pero no prueban por qué. 

**Conclusión provisional o final:** El análisis permitirá comparar el comportamiento histórico de Coca-Cola, Disney y McDonald's, identificando sus cambios de precios, rentabilidad y volatilidad. Con estos resultados se podrá determinar cuál presentó mayor estabilidad durante el periodo estudiado, teniendo en cuenta que el comportamiento pasado no garantiza resultados futuros.

> Los resultados históricos no garantizan rendimientos futuros.

## 8\. Simulacro · S27 (10 de noviembre)

**Guion de sustentación (3–5 minutos):**

- Problema financiero y activos.  
- Datos y metodología.  
- Demostración de interactividad.  
- Hallazgos e interpretación.  
- Conclusión y limitaciones.

**Retroalimentación recibida:** \[Observaciones del docente o compañeros\]

| Ajuste necesario | Responsable | Estado |
| :---- | :---- | :---- |
| \[Ajuste\] | \[Integrante\] | \[Pendiente / en proceso / resuelto\] |

## 9\. Presentación final · S28 (12 de noviembre)

- **Enlace funcional de la aplicación:** \[URL\]  
- **Versión final / commit:** \[Enlace\]  
- **Evidencia de presentación:** \[Enlace autorizado\]  
- **Conclusiones finales:** \[Síntesis\]  
- **Limitaciones y posibles mejoras:** \[Descripción\]

## 10\. Bitácora de trabajo y aportes

| Fecha | Integrante(s) | Investigación o decisión | Avance técnico / evidencia | Próximo paso |
| :---- | :---- | :---- | :---- | :---- |
| 2026-11-03 | \[Nombre\] | \[Qué investigamos\] | \[Enlace a código o documento\] | \[Acción\] |
| 2026-11-05 | \[Nombre\] | \[Decisiones\] | \[Evidencia\] | \[Acción\] |
| 2026-11-10 | \[Nombre\] | \[Retroalimentación\] | \[Cambio\] | \[Acción\] |

## Recursos de consulta

- [Libro de programación y analítica financiera del curso](https://github.com/vyolete/proyecto_analitica_financiera)  
- [Documentación de yfinance](https://ranaroussi.github.io/yfinance/)  
- [Documentación de pandas](https://pandas.pydata.org/docs/)  
- [Documentación de Streamlit](https://docs.streamlit.io/)  
- [Documentación de Shiny para R](https://shiny.posit.co/r/)

**Uso del documento:** En S25 desarrolla especialmente las secciones 2 a 5 y registra tu primera prueba; en S26, S27 y S28 actualiza el mismo README. No dupliques información en entregas separadas.