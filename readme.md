https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/


Crear base de datos sqlite3:
    - sqlite3 basedatos.db
Realizar migraciones:
    - python manage.py db init
    - python manage.py db migrate
    - python manage.py db upgrade
'sqlite:///database.db'
Aws : 
 - amazon linux
 - t2.large
 En la consola:
    - sudo yum update
    - sudo yum upgrade
    - sudo amazon-linux-extras install docker
    - Iniciar el docker engine
        - sudo service docker start
    - sudo yum install git 

    git clone https://github.com/Rojas-Andres/Flask-rest-api
    
    - sudo usermod -a -G docker ec2-user
   
Docker:
    - Añadir el host a la app "0.0.0.0" para que acceda desde cualquier lado
    Creamos la imagen -> -t significa que vamos a especificar el tag ya que si no colocamos la etiqueta esta nos la coloca por defecto latest y el punto es el directorio donde andamos parados
    - docker build -t app_python:v1 .
    
    - El 5000 es el puerto de la imagen (con el exopose) y el 80 lo bindeamos.
    
    - docker run -p 80:5000 app_python:v1

Subir imagen a dockerHub:
    - login desde la terminal con docker login
    - docker build -t anrojlo/flask_docker:v1 .
    - docker tag anrojlo/flask_docker:v1 anrojlo/flask_docker_subido
    - docker push anrojlo/flask_docker_subido