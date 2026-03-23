// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.2.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Jordan Michelt Aran Perez",
  title: "Jordan Michelt Aran Perez - CV",
  footer: context { [#emph[Jordan Michelt Aran Perez -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in Mar 2026] ],
  locale-catalog-language: "en",
  text-direction: ltr,
  page-size: "us-letter",
  page-top-margin: 0.7in,
  page-bottom-margin: 0.7in,
  page-left-margin: 0.7in,
  page-right-margin: 0.7in,
  page-show-footer: true,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 79, 144),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 79, 144),
  colors-section-titles: rgb(0, 79, 144),
  colors-links: rgb(0, 79, 144),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Source Sans 3",
  typography-font-family-name: "Source Sans 3",
  typography-font-family-headline: "Source Sans 3",
  typography-font-family-connections: "Source Sans 3",
  typography-font-family-section-titles: "Source Sans 3",
  typography-font-size-body: 10pt,
  typography-font-size-name: 30pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: true,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: true,
  links-underline: false,
  links-show-external-link-icon: false,
  header-alignment: center,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_partial_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.5cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: true,
  entries-degree-width: 1cm,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0.15cm,
  entries-highlights-space-above: 0cm,
  entries-highlights-space-between-items: 0cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 3,
    day: 20,
  ),
)


= Jordan Michelt Aran Perez

#connections(
  [#connection-with-icon("location-dot")[Tampico, Tamaulipas, Mexico]],
  [#link("mailto:jordan@cxaran.com", icon: false, if-underline: false, if-color: false)[#connection-with-icon("envelope")[jordan\@cxaran.com]]],
  [#link("tel:+52-833-451-7152", icon: false, if-underline: false, if-color: false)[#connection-with-icon("phone")[833 451 7152]]],
  [#link("https://cxaran.com/", icon: false, if-underline: false, if-color: false)[#connection-with-icon("link")[cxaran.com]]],
  [#link("https://linkedin.com/in/cxaran", icon: false, if-underline: false, if-color: false)[#connection-with-icon("linkedin")[cxaran]]],
  [#link("https://github.com/cxaran", icon: false, if-underline: false, if-color: false)[#connection-with-icon("github")[cxaran]]],
)


== Resumen Profesional

Creador de software apasionado por investigar, conectar ideas y resolver rompecabezas difíciles. Mi mayor motivación es explorar temas de inteligencia artificial y optimización matemática para desarrollar soluciones modernas. Tengo experiencia asumiendo proyectos de principio a fin usando herramientas diversas. Me caracterizan mis valores, mi interés por aprender e investigar cosas nuevas y aportar soluciones creativas al equipo.

== Proyectos Destacados

#regular-entry(
  [
    #strong[Plataforma de control de reportes para construccion maritima]

    - Plataforma full stack para registrar y dar seguimiento al avance por fases.

    - Arquitectura backend API con FastAPI, frontend en Next.js y persistencia en PostgreSQL.

    - Despliegue en AWS y operacion continua en entorno Linux Ubuntu.

  ],
  [
    Jan 2023 – Mar 2026

  ],
)

#regular-entry(
  [
    #strong[Tesis de maestria en optimizacion generalizada para problemas de agrupacion]

    - Diseñé e investigué un Algoritmo Coevolutivo de Agrupación con Cooperación Auto-Adaptativa (GCA-AC) como enfoque general para problemas de optimización por agrupación.

    - Modelé y validé la propuesta sobre dos dominios distintos: Bin Packing de una dimensión (BPP-1D) y Programación de Máquinas Paralelas (PMS).

    - Integré mecanismos de auto-adaptación de parámetros y estrategias de aprendizaje para mejorar adaptabilidad, rendimiento y calidad de solución.

    - Desarrollé la experimentación computacional y el análisis comparativo contra algoritmos especializados, obteniendo resultados competitivos y útiles para futuras líneas de investigación.

  ],
  [
    Jan 2021 – Dec 2023

  ],
)

#regular-entry(
  [
    #strong[Interfaz web para experimentacion en optimizacion multiobjetivo]

    - Desarrollé una herramienta web para apoyar la experimentación académica en problemas multiobjetivo con conocimiento imperfecto.

    - Diseñé la interfaz gráfica y el flujo de pruebas para facilitar la configuración, ejecución y análisis de escenarios experimentales.

  ],
  [
    Jan 2020 – Dec 2021

  ],
)

== Educacion

#education-entry(
  [
    #strong[Instituto Tecnologico de Ciudad Madero], Maestria en Ciencias de la Computacion

    - Cedula profesional: 15512722

    - Tesis: Optimizacion generalizada para problemas de agrupacion: Un enfoque coevolutivo autoadaptativo.

  ],
  [
    Ciudad Madero, Tamaulipas, Mexico

    Jan 2021 – Dec 2023

  ],
  degree-column: [
    #strong[M.C.]
  ],
)

#education-entry(
  [
    #strong[Instituto Tecnologico de Ciudad Madero], Ingenieria en Sistemas Computacionales

    - Cedula profesional: 12392258

    - Proyecto de titulacion: Desarrollo de una interfaz grafica web para soporte a la experimentacion con problemas multiobjetivo con conocimiento imperfecto.

    - Uno de los tres promedios mas altos de la licenciatura.

  ],
  [
    Ciudad Madero, Tamaulipas, Mexico

    Jan 2016 – Dec 2021

  ],
  degree-column: [
    #strong[I.S.C.]
  ],
)

== Habilidades Tecnicas

#strong[Lenguajes:] Python, JavaScript, Java, C\/C++, Dart, R

#strong[Frameworks y web:] FastAPI, Flask, Node.js, React, Next.js, Flutter

#strong[Bases de datos:] PostgreSQL, SQL Server, MongoDB

#strong[Cloud y sistemas:] AWS, Ubuntu, Linux

#strong[Datos e IA:] TensorFlow, Pandas, optimizacion matematica, analisis de datos, algoritmos heurísticos

#strong[Herramientas:] Git, APIs REST

== Experiencia

#regular-entry(
  [
    #strong[ESEASA], Full-Stack Engineer \/ Software Architect

    - Desarrollé de punta a punta una plataforma crítica con FastAPI + Next.js + PostgreSQL que redujo en más del 50\% el tiempo de procesamiento de reportes y habilitó visibilidad en tiempo real de las fases de construcción de plataformas offshore.

    - Lidere  todo el ciclo de vida de desarrollo de software (SDLC): arquitectura, modelado de datos, API REST, CI\/CD e infraestructura en AWS (Ubuntu), dando soporte a una operación industrial 24\/7 con cero tiempo de inactividad.

    - Integré algoritmos de optimización matemática que sincronizan el seguimiento de las fases de construcción con los cronogramas maestros, vinculando directamente la investigación académica con KPIs de negocio medibles.

    - Gestiono de forma integral los despliegues a producción y el mantenimiento preventivo y correctivo en AWS, garantizando operaciones seguras, escalables y confiables para el control de construcción marítima.

  ],
  [
    Tampico, Tamaulipas, Mexico

    Oct 2023 – Mar 2026

  ],
)

#regular-entry(
  [
    #strong[Prointernet], Backend Developer

    - Desarrollé de forma independiente el backend para más de 5 sitios web comerciales del sector hospitality, traduciendo requerimientos de negocio de restaurantes y hoteles en soluciones confiables y listas para el cliente.

    - Implementé funcionalidades clave para la operación y la presencia digital de cada negocio, asegurando entregas puntuales, alineadas a especificación y orientadas a clientes externos.

  ],
  [
    Tampico, Tamaulipas, Mexico

    Jan 2020 – Dec 2021

  ],
)

== Publicaciones

#regular-entry(
  [
    #strong[A cooperative coevolutionary genetic approach to solve packing problems]

    Jordan Michelt Aran Perez, Laura Cruz Reyes, Bernabe Dorronsoro, Hector Fraire, Nelson Rangel Valdez, Claudia Guadalupe Gomez Santillan, Marcela Quiroz Castellanos

     (10th International Workshop on Numerical and Evolutionary Optimization (NEO X))

  ],
  [
    Jan 2022

  ],
)

== Actividades Academicas

#strong[Profesor adjunto:] Analisis y Diseño de Algoritmos, Instituto Tecnologico de Ciudad Madero (ago 2022 - dic 2022)

#strong[Profesor adjunto:] Probabilidad y Estadistica, Maestria en Ciencias de la Computacion (ene 2023 - jun 2023)

#strong[Ponente:] Un paseo por los caminos de la Inteligencia Artificial (feb 2023 - mar 2023)
