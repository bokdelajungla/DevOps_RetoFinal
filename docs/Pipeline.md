# Pipeline CI

Para ejecutar Jenkins se ha optado por crear un Docker Dind sobre el que ejecutar el contenedor con la imagen de Jenkins.
Se ha seguido la información mostrada en el enlace situado al final del documento.

Creamos la red para comunicar los contenedores:
```yaml
docker network create jenkins
```
Ejecutamos el dind:
```yaml
docker run --name jenkins-docker --rm --detach ^
  --privileged --network jenkins --network-alias docker ^
  --env DOCKER_TLS_CERTDIR=/certs ^
  --volume jenkins-docker-certs:/certs/client ^
  --volume jenkins-data:/var/jenkins_home ^
  --publish 3000:3000 --publish 2376:2376 ^
  docker:dind
```
Creamos el Dockerfile para el contenedor de Jenkins.\
Dockefile:
```yaml
FROM jenkins/jenkins:2.332.2-jdk11
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

ENV DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
RUN mkdir -p $DOCKER_CONFIG/cli-plugins
RUN curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
RUN chmod +rwx $DOCKER_CONFIG/cli-plugins/docker-compose -R

USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.25.3 docker-workflow:1.28"
```
Creamos la imagen a partir del Dockerfile:
```yaml
docker build -t myjenkins-blueocean:2.332.2-1 .
```
Ejecutamos el contenedor:
```yaml
docker run --name jenkins-blueocean --rm --detach ^
  --network jenkins --env DOCKER_HOST=tcp://docker:2376 ^
  --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 ^
  --volume jenkins-data:/var/jenkins_home ^
  --volume jenkins-docker-certs:/certs/client:ro ^
  --volume "%HOMEDRIVE%%HOMEPATH%":/home ^
  --publish 8080:8080 --publish 50000:50000 myjenkins-blueocean:2.332.2-1
```
Ahora accedemos a http://localhost:8080 para acceder a Jenkins. Nos pedirá una contraseña para iniciar la instalación.\
Dicha contraseña se puede obtener ejecutando: docker logs jenkins-blueocean

Una vez completamos el proceso de instalación y creamos un usuario administrador, podemos acceder a la consola de gestión con nuestras credenciales.
A partir de aquí, creamos un nuevo trabajo del tipo 'pipeline'.
Indicamos que queremos usar un repositorio e introducimos la dirección donde se encuetra el repositorio.

Marcamos que el pipeline se encontrará en un fichero Jenkinsfile.

Ahora tenemos que crear el fichero Jenkinsfile y añadirlo al repositorio.
Jenkinsfile:
```yaml
pipeline {
  agent any
  stages {
    stage('Verify tools') {
      steps {
        sh '''
            docker version
            docker info
            docker images
            curl --version
           '''
      }
    }
    stage('Start test container') {
      steps {
        sh 'cd tests'
        sh 'docker build -t devops_retofinal_tests .'
        sh 'cd ..'
        sh 'docker run devops_retofinal_tests -d'
      }
    }
  }
  post {
    always {
      sh 'docker compose stop'
      sh 'docker compose down'
      sh 'docker compose ps'
    }
  }
}
```
Ahora basta lanzar el trabajo y seguir su evolución a través de las etapas.

Lamentablemente no conseguimos que ejecutara los test.


[Tutorial para buildear una aplicacion python](https://www.jenkins.io/doc/tutorials/build-a-python-app-with-pyinstaller/#on-windows)
