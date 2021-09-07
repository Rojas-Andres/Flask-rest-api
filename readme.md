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
    Esto es para poder ejecutar comandos de docker
    
    - id
    - para ver los grupos
        - cat /etc/group
    - El usuario que nosotros tenemos ec2-user en groups -> solo pertenece a los grupos esos pero no pertenece al grupo de docker por lo tanto toca adicionarlo
    - sudo usermod -a -G docker ec2-user
    - cat /etc/group
    - docker version -> como no deja toca desconectarnos y volver a entrar
   
Docker:
    - Añadir el host a la app "0.0.0.0" para que acceda desde cualquier lado
    Creamos la imagen -> -t significa que vamos a especificar el tag ya que si no colocamos la etiqueta esta nos la coloca por defecto latest y el punto es el directorio donde andamos parados
    - docker build -t app_python:v1 .
    - El 5000 es el puerto de la imagen (con el exopose) y el 80 lo bindeamos.
    - docker run -p 80:5000 app_python:v1

FROM -> La base de nuestra imagen
Son n capas dependiendo de las lineas que tengamos
COPY -> copiamos todo a la carpeta app -- El punto indica la carpeta donde estamos parados
WORDIR -> Nuestro entorno de trabajo sera esa carpeta donde colocamos nuestros archivos
RUN pip install -r requirements.txt -> Instalamos todo 
EXPOSE 5000 -> Al quedar en una imagen de docker este queda encapsulado por ende tenemos que exponerlo y el puerto publico
CMD ["python","app.py"] -> Este es el comando inicial que va a ejecutar . En este caso que ejecute nuestra app
