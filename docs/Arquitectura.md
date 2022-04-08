# Arquitectura

La arquitectura de nuestro sistema será la siguiente:

Nuestra aplicación estará hecha en el lenguaje de programación Python usando el framework Flask, ya que es específico para poder hacer un servicio web. El servicio correrá en Docker, el cual nos parece la herramienta más útil para que nuestra aplicación pueda funcionar en el máximo de sitios posibles.

Necesitaremos unos balanceadores de carga de aplicaciones para que tome las decisiones y admita el mapeo de puertos, de esto se encarga nuestro servicio de AWS. A continuación usaremos terminadores SSL para proteger los datos durante la transferencia creando un canal de cifrado, esto lo podemos hacer directamente gracias al framework de Flask.

Para las bases de datos vamos a usar SQLite para toda la información operativa de la aplicación, como pueden ser las cadenas de búsqueda y los usuarios. Mientras que las métricas de uso (número total de invocaciones y tiempo medio de respuesta) para cada endpoint se guardarán en una base de datos NoSQL, en este caso Redis. 

Nuestra aplicación se desplegará en la infraestructura de AWS (Amazon Web Services), usaremos el servicio AWS Fargate ya que está diseñado para crear aplicaciones sin tener que administrar servidores. El precio sería de 0,0053 USD por GB  por hora, es la mejor opción para una aplicación de estas dimensiones.

![Arquitectura](AWS.png?raw=true "Arquitectura")