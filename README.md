## Tratamiento de Datos Ejercicio 2 - Grupo 7 - FastAPI

## Preguntas para el Trabajo Final

### 1. ¿Cómo podría un atacante aprovechar los endpoints de tu API para realizar múltiples consultas y agotar este límite, y qué impacto tendría esto en la disponibilidad del servicio para usuarios legítimos?

Un atacante podría aprovechar los endpoints debido a que la API no cuenta con autenticación ni control de acceso. Al ser endpoints públicos, cualquier persona puede consumirlos directamente sin necesidad de iniciar sesión.

En este escenario, el atacante podría crear un script automatico que envíe solicitudes de forma masiva al endpoint de búsqueda. Incluso podría hacer un bucle que realice cientos o miles de consultas seguidas con diferentes nombres de películas para evitar respuestas repetidas. 

Cada una de estas solicitudes haría que mi aplicación consulte a la OMDb API, consumiendo una petición del límite diario.

Debido a que no existe un mecanismo de control como rate limiting , el atacante podría ejecutar este proceso de forma continua y automatizada, logrando agotar las 1000 consultas diarias en muy poco tiempo.

El impacto de esto sería que una vez alcanzado el límite, la aplicación ya no podría obtener datos desde la API externa. 

Esto afectaría directamente a los usuarios legítimos ya que no podrían realizar búsquedas ni ver información de películas. Aunque el sistema seguiría funcionando a nivel técnico, su funcionalidad principal quedaría inutilizable generando una denegación de servicio indirecta.

### 2. El sistema procesa un archivo Excel (PLACAS.xlsx) como entrada para realizar consultas automatizadas en el portal de la ANT y luego extrae y almacena los resultados.¿Cómo podría un atacante manipular el contenido del archivo Excel (por ejemplo, el formato de las placas o celdas específicas) para afectar el comportamiento del script o generar resultados incorrectos durante el scraping?

Un atacante podría manipular el archivo PLACAS.xlsx no solo ingresando valores inválidos, sino también introduciendo cargas maliciosas con el objetivo de evaluar posibles vulnerabilidades en el portal web de la ANT. Dado que la información del Excel se inserta directamente en un formulario web mediante Selenium, un atacante podría incluir cadenas especialmente diseñadas, como scripts o payloads, para comprobar si la aplicación es vulnerable a ataques como Cross-Site Scripting (XSS).

Si el portal no valida correctamente las entradas y refleja este contenido en la respuesta, podría ejecutarse código en el navegador, lo que evidenciaría una vulnerabilidad de tipo XSS reflejado. Aunque el script en sí no ejecuta estos comandos directamente, sí actúa como un medio para inyectarlos en la aplicación web.

Asimismo, un atacante podría probar con caracteres especiales o secuencias inesperadas para identificar posibles fallos en la validación del lado del servidor. Esto podría provocar comportamientos anómalos en la aplicación, errores en la respuesta o incluso revelar información adicional del sistema.

Desde el punto de vista del script, este tipo de manipulación también podría afectar el resultado de la automatización, ya que respuestas inesperadas o estructuras HTML alteradas podrían hacer que Selenium no encuentre los elementos correctamente, generando errores o resultados incompletos.

El archivo Excel no solo representa una fuente de datos, sino también un vector potencial de ataque si no se validan adecuadamente sus contenidos, ya que podría ser utilizado para inyectar entradas maliciosas en el portal web.

## Desarrollo del Ejercicio

Para el desarrollo del presente ejercicio tomaremos como premisa la hipotética creación de un catálogo de películas en formato físico para los fanáticos de estos formatos, las cuales serán clasificadas y almacenadas junto a datos básicos. Asumiremos que cada película que poseamos en el catálogo físico será almacenada dentro de una base de datos local usando como parámetro de clasificación el código asignado en ImDB(Internet Movie DataBase). Los datos de la película serán consultados mediante un api externo llamado The Open Movie DataBase OMDB https://www.omdbapi.com/.

Para el consumo de la data desde esta API es necesaria la creación de una clave de acceso o APIKEY, la cual por buena práctica será colocada dentro de un archivo .env y omitida mediante .gitignore de su carga al repositorio de GitHub. Para permitir la revisión se colocará la misma dentro de la plataforma Canvas UIDE, junto con los enlaces a los repositorios que conforman el ejercicio práctico de la clase 2. Esta clave deber ser colocada en un archivo .env local para lo cual se adjunta al repositorio de GitHub el archivo .env.example con la sintaxis adecuada para permitir la llamada a la variable de entorno desde Phyton. Este procedimiento es necesario para evitar los accesos no autorizados, ya que el api nos permite un máximo de mil consultas diarias.


<img width="572" height="84" alt="image" src="https://github.com/user-attachments/assets/e197b039-5ff4-407c-9826-41fb0c97ecce" />



<img width="1323" height="385" alt="image" src="https://github.com/user-attachments/assets/3d9dfe03-082f-4b8d-a5db-ebcdd71ee3f8" />


Como primer endpoint el servicio ingresa al buscador primario, que incluye un cuadro de búsqueda y un botón para realizar la consulta a la base de datos local, la cual transacciona utilizando SQLITE a un archivo .db localmente. Para una mejor estética de la página se creó un archivo de estilos css para mejorar la presentación visual y que el servicio sea más amigable con el usuario.


<img width="1935" height="1607" alt="image" src="https://github.com/user-attachments/assets/aa2c2117-5282-41d7-beb3-474c8df624a9" />


Una vez que el servicio ha consultado la data en OMDB, muestra los resultados aproximados al texto consultado y nos da la opción de escoger cual es la película que buscamos.


<img width="1941" height="1611" alt="image" src="https://github.com/user-attachments/assets/7b33d066-c18a-4560-bf11-d739a8fc579a" />



<img width="2116" height="1482" alt="image" src="https://github.com/user-attachments/assets/70cfa61b-c2c1-48fc-bbf5-bfec9ee17bb3" />



Una vez dentro del detalle de la película buscada, encontramos la opción de almacenar en la base de datos local.



<img width="2114" height="464" alt="Captura de pantalla 2026-04-21 101926" src="https://github.com/user-attachments/assets/7bf88e00-032a-4305-b70a-c6b1517ef046" />




Adicionalmente se creó el endpoint para consulta de la base de datos, el cual muestra el contenido de la misma y nos da la opción de revisar los datos almacenados para cada película.



<img width="2106" height="1217" alt="Captura de pantalla 2026-04-21 101936" src="https://github.com/user-attachments/assets/6075dacb-695d-4083-a2de-e6b5ce230098" />



<img width="2109" height="2063" alt="Captura de pantalla 2026-04-21 101943" src="https://github.com/user-attachments/assets/f28b3d74-5085-478c-809f-7ce1699d7be3" />

Finalmente se creó un endpoint para borrar la base de datos, pero no se colocó ningún acceso dentro de la página para este propósito y se accede al endpoint mediante la dirección {url}/clear, para el caso de nuestro ejercicio sería localhost:8080/clear.




