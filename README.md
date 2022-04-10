# DevOps Reto Final 
Repositorio para el Reto Final de DevOps

## Enunciado
Caso de estudio - Servicio web de consultas

Nuestra aplicación es un servidor web que expone una serie de endpoints:

- Alta de usuarios, que recibe un email y una contraseña y crea un nuevo usuario en el sistema (Si no existe)
- Login de usuarios, que para un par de email/contraseña válido devuelve un token válido durante 30 minutos.
- Los siguientes endpoints necesitan recibir un token válido en la cabecera HTTP “X-Service-Token”
  - /almacena, que guarda las frases que recibe en una base de datos.
  - /query, que devuelve el número de veces que una palabra aparece en frases del almacenamiento.
  - /logout - expira el token
  - /delete - elimina el usuario y expira el token

El servicio se apoya en una base de datos SQL para almacenar la información operativa: cadenas de búsqueda y usuarios.

El servicio almacena métricas de uso para cada endpoint en una base de datos NoSQL como Redis, MongoDB, Memcached, etc:

- número total de invocaciones
- tiempo medio de respuesta

---
## Objetivo

Dado el caso de estudio, se pide al alumno elaborar los siguientes entregables:
### [Arquitectura de la solución](docs/Arquitectura.md)

Elaborar un documento formal en el que se describa la arquitectura de la solución. Se valorará positivamente una redacción clara y correcta y el uso de diagramas y topologías allá donde una imagen valga más que mil palabras.

Software que os puede ayudar a que el resultado sea vistoso:
- Flowchart Maker & Online Diagram Software (Enlaces a un sitio externo.)
- Cloudcraft – Draw AWS diagrams (Enlaces a un sitio externo.)
- https://aws.amazon.com/es/architecture/icons/ (Enlaces a un sitio externo.)

En concreto, se pide elaborar con detalle los siguientes puntos:

#### Obligatorios

Es necesario desarrollar estos dos temas para que esta parte cuente como apta:
##### Descripción de la arquitectura del sistema

Definir qué servicios, métodos y tecnologías se necesitan para poder ofrecer una solución:
- balanceadores de carga
- Terminadores SSL
- Bases de datos
- Sobre qué software correrá el servicio en esas máquinas (por ejemplo, si la solución usa Java, definir si se usará Tomcat, Catalina u otra alternativa)

##### Arquitectura Cloud

Se ha decidido desplegar nuestra infraestructura sobre una nube pública, al carecer de recursos físicos.
- Selección de proveedor
- Definición de servicios a usar
- Cantidad y tipo de instancias
- Aproximación de costes mensuales de la parte fija (no incluyendo costes variables en función del tráfico o la cantidad de datos almacenados)

#### Opcionales

Desarrollar estos dos puntos es opcional y valdrá para subir la nota. En cualquier caso, su análisis os dará información y perspectiva para otras partes del reto.
##### Descripción del despliegue

Explicar en detalle cómo se llevará a cabo el despliegue de nuevas versiones de software:

- Elección de repositorio de artefactos, según su tipo
- Modelo de versionado
- Estrategia de despliegue sin indisponibilidad
- Plan de marcha atrás

##### Definición y cálculo de SLAs

Se pide buscar al menos un SLA (Service Level Agreement) para nuestro servicio, detallar cómo se conseguiría medir el indicador asociado (SLI) y cómo podríamos saber qué podemos incumplirlo, con un plan de acción para remediarlo.

### [Entorno de Desarrollo](docs/Entorno.md)

Para facilitar el onboarding en el proyecto de nuevos desarrolladores, nada mejor que tener un entorno local de desarrollo potente, fiable y que se asemeje lo más posible al entorno final.

Se pide la definición de un entorno exportable de desarrollo.

- Por exportable entendemos que se debe poder subir a control de versiones, descargar y ejecutar sin más. En caso de que se necesite alguna dependencia (software concreto, credenciales, variables de entorno) ésta deberá estar debidamente documentada.
- Debe estar basado en alguna tecnología de virtualización (contenedores, máquinas virtuales…) que consiga, mediante la ejecución de un comando / script  o similar levantar los servicios requeridos para poder probar localmente, de la forma más rápida posible, los cambios que hagamos a nuestro servicio web.

Se puede usar cualquier tecnología que tenga sentido, mientras el resultado sea el pedido: Se recomienda reutilizar algunos de los creados durante el curso con [Docker Compose](https://docs.docker.com/compose/) o [Vagrant](https://www.vagrantup.com/)

### [Declaración y configuración de infraestructura](docs/Infra.md)

Algo que sabemos que es imprescindible es que toda nuestra infraestructura, así como su configuración, esté declarada como código fuente en control de versiones.

Se pide declarar la infraestructura como código, usando cualquiera de las herramientas vistas durante el curso (Terraform, Vagrant, AWS Cloudformation o equivalente si se elige otro proveedor) de los sistemas mínimos necesarios para poder ofrecer el servicio descrito de forma óptima desde un punto de vista Devops.

Adicionalmente, hay que añadir playbooks de Ansible (o Salt, o Chef, o lo que estimemos oportuno) para configurar los servicios en la infraestructura definida.

Aquí nos podríamos liar durante días y semanas y no terminar así que. para centrar un poco el tiro, se pide entregar al menos uno de los tres bloques identificados:
#### Entorno de producción

Los servidores sobre los que se instalará y arrancará el servicio web. Debe existir un esquema de alta disponibilidad para evitar caídas de servicio y posibilitar despliegues sin downtime. Cualquier otra máquina que se considere necesaria debe ser instalada y configurada también).

Se debe instalar el software necesario para poder instalar, arrancar y actualizar el servidor web en cualquier momento.
#### Entorno de preproducción

Idéntico a producción pero con un único nodo en lugar de los N elegidos para dar mayor estabilidad.
#### Máquinas asociadas a servicios que dan soporte al ciclo de vida

Instalar y configurar los siguientes servicios

- CICD (Jenkins)
- Almacenamiento: (Artifactory, Docker Registry, …)
- Colector de datos de telemetría (ElasticSearch, Prometheus…)
- [**Opcional**] Si se elige levantar algún servicio en lugar de usar un SaaS del proveedor de cloud elegido, debemos añadir su configuración (por ejemplo, si elegimos usar nuestra propia base de datos en lugar de contratar Amazon RDS)

**OJO**: Aquí hay que tener muy en cuenta que los entornos de producción y preproducción pueden estar en redes diferentes (eso es elección nuestra como operadores, aunque ciertamente una buena práctica). Si esto es así, hay que conseguir que la conectividad desde las máquinas del ciclo de vida hacia los entornos productivos sea posible:
- Es un **error** generar una infraestructura que dependa de una conectividad inexistente para funcionar.

### [Pipeline CI](docs/Pipeline.md) 

Diseñar un Pipeline CI en **Jenkins** con las siguientes características **obligatorias**:
1. Ejecución de tests unitarios
2. Construcción de artefacto
3. Almacenamiento artefacto
4. Despliegue a entorno de pre-producción

Opcionalmente, para subir nota se pueden añadir los pasos necesarios para llegar a producción de forma apropiada:
1. Tests integración sobre pre-producción (puede ser un smoke-test sobre la infra de preprod)
2. Despliegue a producción con zero-downtime

Se debe entregar un fichero _Jenkinsfile_ que implemente el flujo pedido y que funcione, de modo que se podría añadir al repositorio y cargarlo como un Multibranch Job, como se hizo en la UF 6.

---
## Implementación
Se ha optado por realizar una implementación del servicio usando Python y Flask mediante peticiones POST y GET al servidor.\
Se ha considerado que cuando se usa el endpoint "almacena" se está modificando el estado del servidor y por tanto el verbo HTTP correcto es POST.\
Sin embargo, cuando se hace uso del endpoint "consulta", se envían datos al servidor pero no se modifica su estado, así que se ha optado por emplear GET.\
Del mismo modo cuando se da de alta un Usuario se ha de emplear el método POST. Para hacer login o logout se empleará GET.\
Para probar el funcionamiento se recomienda emplear un programa como Curl o Postman.
Se ha eliminado el fichero de almacenamiento de cadenas de las versiones anteriores y se ha sustituido por una tabla dentro de la base de datos del programa.\
Se pretendía implementar el frontend de la aplicación mediante plantillas html, para facilitar el testing y la presentación, pero ha sido posible. 


### Dependencias
Las dependencias están declaradas en el fichero _requirements.txt_


### Ejecución
Para iniciar la aplicación ejecute el comando:

_python server.py [-h] [-p \<puerto\>]_

Si no se indica ningún parámetro se levantará el servicio con las opciones por defecto que es empleando el puerto 12345.\
Para terminar la aplicación pulsar Ctrl+C

Para Windows, se ha creado el fichero _start.bat_ que inicia el servicio con sus valores por defecto si no se incluyen parámetros y además permite elegir un puerto mediante la sintaxis:
_start.bat -p puerto_

## Funcionamiento
Los endpoints son:
* /
* /signup
* /login
* /logout
* /users
* /almacena
* /consulta
* /ready
* /health
* /metrics

Hay que destacar que se usa SSL, por los que los endpoints ahora emplean el protocolo HTTPS (si se intenta acceder a ellos mediante HTTP dará un error).

### Home
Si se accede al endpoint / se muestra el mensaje HTML "Servicio Web para Cadenas"

### Signup
Permite el registro de un nuevo usuario en la base de datos.\
Se debe indicar en el cuerpo del mensaje un JSON con un nombre (name) y una contraseña (password):
```yalm
{ 
    "name":"Fulanito",
    "password":"contraseña" 
}
```
El servidor devuelve un mensaje JSON en la respuesta indicando el resultado de la operación.\
El nuevo usuario y la contraseña se almacenan en la base de datos (no se almacena la contraseña en claro, si no un hash)

### Login
Permite al usuario autenticarse  indicando su nombre y su contraseña mediante la cabecera de Autorización de HTML.

Si el usuario existe y la contraseña es correcta (se hace el hash y se comprueba con la que se tiene guardada en la base de datos) el servidor devuelve un token que será válido durante 60 minutos.
Este token deberá ser incluido en la cabecera de las peticiones a los endpoints protegidos en un campo llamado _X-Service-Token_ para que nos permita usarlos.

### Logout
Si se accede al endpoint con un token válido, se incluye dicho token en una tabla de tokens expirados. A partir de ese momento no podrá acceder a ningún endpoint protegido hasta que consiga un nuevo token válido mediante el endpoint /login 

### Almacena
Se necesita un token válido para poder llevar a cabo el almacenamiento.\
Para llevar a cabo el almacenamiento de una cadena en el fichero se debe realizar un POST e incluir el parámetro string con la cadena que queremos almacenar en el fichero:
* ej: _POST 127.0.0.1/almacena?string=Cadena+a+almacenar_

Si se emplea un verbo distinto de POST devolverá un error 405 Method Not Allowed.\
Si no se incluye el parámetro "string" devolverá una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe incluir el parámetro string).

### Consulta
Se necesita un token válido para llevar a cabo la consulta.\
Para llevar a cabo la consulta de una palabra en el fichero se debe realizar un GET e incluir el parámetro string con la palabra que queremos almacenar en el fichero:
* ej: _POST 127.0.0.1/consulta?string=Cadena_

Si se emplea un verbo distinto de GET devolverá un error 405 Method Not Allowed.\
Si no se incluye el parámetro "string" devolverá una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe incluir el parámetro string).\
Si se envía más de una palabra devolvera una respuesta 400 BAD REQUEST con un json en el cuerpo con información sobre el error (debe enviar una única palabra).
### Ready
Endpoint que comprueba la conexión con la base de datos y el correcto funcionamiento de los logs
Si todo funciona correctamente devuelve un 200 OK. Si alguno de los dos falla devuelve un 503 NO DISPONIBLE.

### Health
Endpoint que devuelve 200 OK si el funciona correctamente, 503 si no está disponible.

### Metrics
Este endpoint devuelve un JSON con las métricas de los endpoints CONSULTA y ALMACENA y del numero de cadenas almacenadas actualmente en la base de datos.\
En concreto devuelve el número de peticiones en cada endpoint y el tiempo medio de respuesta de cada endpoint.\
El formato de salida es el siguiente:

```yalm
{
  "metrics": [
    {
      "Endpoint_CONSULTA": [
        {
          "name": "consulta_avg_response_time",
          "value": averageConsulta
        },
        {
          "name": "consulta_hits",
          "value": consultaHits
        }
      ]
    },
    {
      "Endpoint_ALMACENA": [
        {
          "name": "almacena_avg_response_time",
          "value": averageAlmacena
        },
        {
          "name": "almacena_hits",
          "value": almacenaHits
        }
      ]
    },
    {
      "Resource_DB": [
        {
          "name": "db_entries",
          "value": resultsEntries
        }
      ]
    }
  ]
}
```
Si no estuviera disponible enviará un mensaje 503.

## Tests
En la carpeta tests se han incluído los test unitarios para probar el funcionamiento del servicio.\
NOTA: Se ha conseguido implementar la comprobación del funcionamiento de los tokens, que es una mejora sobre la versión anterior.
IMPLEMENTADOS:
* _test_almacena.py_ -- prueba el funcionamiento del endpoint "almacena"
* _test_consulta.py_ -- prueba el funcionamiento del endpoint "consulta"
* _test_health.py_ -- prueba el funcionamiento del endpoint "health"
* _test_ready.py_ -- prueba el funcionamiento del endpoint "ready"
* _test_others.py_   -- prueba el funcionamiento del resto de funciones de server.py
POR IMPLEMENTAR:
* _test_signup.py_ -- prueba el funcionamiento del endpont "signup"
* _test_logout.py_ -- prueba el funcionamiento del endpont "signup"

Para poder ejecutar los test y ver su cobertura es necesario instalar _pytest_ y _coverage_

Para evaluar la covertura:\
_coverage run -m pytest_\
Para visualizar el resultado:\
_coverage report_\
Para generar un reporte detallado en HTML:\
_coverage html_\
El resultado de éste último cuando se ejecutó en nuestra máquina se ha incluido en el repositorio (Una cobertura del 84%).


## Pruebas
Se recomienda el uso de Postman para comprobar el funcionamiento de la aplicación.\
A tal efecto se ha incluído el fichero _DevOpsServer.postman_collection.json_ que contiene una colección que con todos los casos de prueba.\


## Autores ✒️

Los componentes del grupo:

* **Antonio De Gea Velasco**
* **Adrian Rodriguez Montesinos**
* **Jorge Sánchez-Alor Expósito**
