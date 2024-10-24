# Vatios

## Descripción del Proyecto

**Vatios** es una aplicación móvil diseñada para proporcionar información actualizada sobre los precios de la electricidad en España. La aplicación permite a los usuarios gestionar sus electrodomésticos y recibir notificaciones personalizadas sobre las tarifas eléctricas. 
Con un enfoque en la usabilidad y eficiencia, Vatios facilita el acceso a información esencial sobre el consumo energético.

## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Funcionalidades](#funcionalidades)
- [Requisitos Funcionales](#requisitos-funcionales)
- [Requisitos No Funcionales](#requisitos-no-funcionales)

## Funcionalidades

- **Actualización Automática**: Precios de electricidad actualizados al abrir la aplicación.
- **Gestión de Notificaciones**: Configuración de notificaciones personalizadas sobre precios mínimos, máximos y horas baratas.
- **Visualización de Precios**: Acceso a precios mínimos, máximos y actuales, con codificación de colores según el promedio diario.
- **Cálculo de Gasto**: Estimación del gasto de electrodomésticos en base a su consumo y tarifas eléctricas.
- **Interfaz Gráfica**: Diseño intuitivo y adaptable a diferentes tamaños de pantalla.

## Requisitos Funcionales

| ID   | Título                                          | Obligatoriedad | Descripción                                                                                                         | Relación            | Estado     |
|------|------------------------------------------------|----------------|---------------------------------------------------------------------------------------------------------------------|---------------------|------------|
| RF01 | Base Datos – Precios Electricidad              | Crítico        | Cada vez que el usuario abra la aplicación, se actualizarán los datos de precios de electricidad.                   | RF05                | Completado |
| RF02 | Base Datos – Notificaciones                     | Crítico        | Cuando el usuario cambie el estado de una notificación, el sistema guardará el estado en la base de datos.          |                     | Completado |
| RF03 | Base Datos – Precios Mínimos y Máximos        | Complementario | Cuando el usuario modifique los precios mínimos y máximos, estos se guardarán en la base de datos.                 |                     | Completado |
| RF04 | Base Datos – Notificaciones                     | Crítico        | Cuando el usuario modifique características de notificaciones, los datos serán guardados en la base de datos.      |                     | Completado |
| RF05 | Base Datos – Ubicación Usuario                 | Opcional       | Cuando el usuario cambie su ubicación, esta se guardará en la base de datos.                                      |                     | Propuesto  |
| RF06 | Base Datos – Electrodoméstico                  | Crítico        | Cuando un usuario introduzca el nombre y el gasto de un electrodoméstico, estos datos serán guardados.             |                     | Completado |
| RF07 | Activar interruptor “Precios del Dia”          | Complementario | Al activar el interruptor, se mostrarán todos los precios del día en la pantalla principal.                        | RF11                | Completado |
| RF08 | Cambio Ubicación                               | Opcional       | Cuando el usuario cambie de ubicación, se actualizarán los precios de la luz en todas las pantallas.                |                     | Propuesto  |
| RF09 | Precios Mínimos y Máximos                      | Crítico        | El sistema obtendrá y mostrará los precios mínimos y máximos según la ubicación del usuario.                        | RF01                | Completado |
| RF10 | Precio Actual                                  | Crítico        | El sistema obtendrá el precio actual de la luz y lo mostrará en el recuadro correspondiente.                       | RF01                | Completado |
| RF11 | Lista de Precios                               | Crítico        | El sistema obtendrá una lista de precios de la luz y la mostrará en la pantalla principal.                         | RF01, RF07          | Completado |
| RF12 | Asignar Colores – Interruptor OFF              | Crítico        | Se asignará un color a cada precio eléctrico según su relación con el promedio diario.                              | RF01                | Completado |
| RF13 | Asignar Colores – Interruptor ON               | Opcional       | Se establecerá un color para precios según si están por debajo o por encima de los mínimos y máximos.              | RF03, RF01          | Completado |
| RF14 | Consulta horas económicas                       | Complementario | El sistema mostrará el número de horas económicas que el usuario haya insertado.                                   | RF05                | Completado |
| RF15 | Editar Notificación – Hora precios mínimos y máximos | Complementario | El usuario podrá modificar la hora para ser notificado de precios mínimos y máximos.                                |                     | Completado |
| RF16 | Notificación precios mínimos y máximos         | Crítico        | El sistema notificará al usuario con información de precios mínimos y máximos a la hora establecida.                | RF15                | Propuesto  |
| RF17 | Editar Notificación – Precio Bajo              | Complementario | El usuario podrá modificar el tiempo de notificación para cuando el precio baje de un valor establecido.            | RF04                | Completado |
| RF18 | Notificación Precio Bajo                       | Crítico        | El sistema notificará al usuario antes de que el precio baje de un valor establecido.                              | RF04                | Propuesto  |
| RF19 | Editar Notificación – Horas Baratas            | Complementario | El usuario podrá modificar el número de horas baratas que le aparecerán en la notificación.                        |                     | Completado |
| RF20 | Notificación Horas Baratas                     | Crítico        | El sistema notificará al usuario sobre el número de horas más baratas establecidas.                                | RF04                | Propuesto  |
| RF21 | Añadir Electrodoméstico                        | Complementario | El usuario podrá añadir un electrodoméstico y su gasto por Kw/h a la base de datos.                               | RF06                | Completado |
| RF22 | Cálculo del gasto estimado                     | Complementario | El sistema calculará el gasto estimado de cada electrodoméstico en la base de datos.                              | RF06, RF24          | Completado |
| RF23 | Borrar Electrodoméstico                        | Complementario | El usuario podrá borrar un electrodoméstico de la base de datos al hacer clic en el icono correspondiente.         | RF06                | Completado |
| RF24 | Cambio hora, para el cálculo estimado de cada electrodoméstico | Opcional | El usuario podrá modificar la hora a la que se calculan los gastos estimados para cada electrodoméstico.         | RF06, RF22          | Completado |
| RF25 | Actualización de los datos                     | Crítico        | El sistema mostrará siempre los últimos cambios realizados por el usuario.                                         | RF24, RF23, RF22, RF21, RF14, RF13, RF12, RF11, RF10, RF04, RF07 | Completado |
| RF26 | Navegación – 3 Pantallas                       | Crítico        | El usuario podrá navegar entre las tres pantallas principales en todo momento.                                     |                     | Completado |

## Requisitos No Funcionales

| ID    | Título                                   | Prioridad | Descripción                                                                                                   | Tipo             |
|-------|------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------|------------------|
| RNF01 | Framework de la aplicación               | Alta      | El marco del desarrollo de la aplicación es Kivy.                                                            | Usabilidad        |
| RNF02 | Aplicación Android                       | Alta      | La aplicación será ejecutada en dispositivos móviles Android.                                                | Usabilidad        |
| RNF03 | Idioma                                  | Alta      | La aplicación está en español, empleando frases cortas y fáciles de entender.                               | Interfaz          |
| RNF04 | Conexión a Internet                     | Alta      | El dispositivo debe disponer de conexión a internet para obtener los datos.                                  | Rendimiento       |
| RNF05 | API – Precio Electricidad               | Alta      | La aplicación obtiene todos los datos desde la API oficial del gobierno.                                    | Confiabilidad, Seguridad |
| RNF06 | Tiempo de aprendizaje                   | Alta      | El tiempo de aprendizaje del sistema por parte de un usuario será de cinco minutos como máximo.               | Interfaz          |
| RNF07 | Interfaz Gráfica                        | Alta      | El sistema debe disponer de interfaces gráficas bien formadas.                                              | Interfaz          |
| RNF08 | Disponibilidad                          | Alta      | El sistema debe tener una disponibilidad del 99,99% de las veces en que un usuario intente acceder a él.    | Confiabilidad     |
| RNF09 | Código                                  | Alta      | El código estará bien estructurado y organizado para facilitar el mantenimiento de la aplicación.             | Mantenimiento      |
| RNF10 | Eficiencia de funciones                 | Alta      | La aplicación debe permitir al usuario acceder a las funcionalidades en menos de 5 segundos.                 | Rendimiento       |
| RNF11 | Diseño adaptable a distintas pantallas  | Alta      | La aplicación debe poder mostrarse en distintos dispositivos con varios tamaños de pantalla.                 | Interfaz          |
| RNF12 | Almacenamiento de Datos                  | Alta      | El software permite la persistencia de datos configurados por el usuario. Los datos se almacenarán y recuperarán de forma eficiente. | Rendimiento       |

