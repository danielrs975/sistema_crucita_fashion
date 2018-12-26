Sistema Crucita Fashion Boutique
================================
[![Build Status](https://travis-ci.com/danielrs975/sistema_crucita_fashion.svg?branch=master)](https://travis-ci.com/danielrs975/sistema_crucita_fashion)

  Este proyecto consiste en el desarrollo de una aplicación web para la administración de un local de ventas, esto incluye un control sobre el inventario, ventas y reservas que se realicen. También se le proveera de servicios a los usuarios de la app como por ejemplo poder realizar compras, ver catálogos de inventario recien añadido, etc. Para mayor información vea el siguinte archivo https://docs.google.com/document/d/1fP2F8wYau6VhY54gA0icHZzOzI1K_u4ydvt7FU7UIYw/edit?usp=sharing

Herramientas de desarrollo a utilizar
-------------------------------------
* Python 3.6
* Django 2.1.4
* Travis CI
* Heroku
* Basecamp

Preparando el ambiente de trabajo
---------------------------------
  Para comenzar a participar en el proyecto primero se necesita configurar el ambiente necesario para poder empezar a desarrollar. A continuación se presentarán una serie de pasos para poder configurar el ambiente con éxito

  1. Crear una carpeta llamada *Crucita_Fashion* con 
  ```shell
  mkdir Crucita_Fashion
  ```
  2. Clonar el repositorio dentro de esta carpeta con el siguiente comando.Si no se tiene configurado ssh entonces utilice el segundo comando.
  ```shell
  git clone git@github.com:danielrs975/sistema_crucita_fashion.git Crucita_Fashion/
  ```
 
  ```shell
  git clone https://github.com/danielrs975/sistema_crucita_fashion.git Crucita_Fashion/
  ```
  3. Entrar en la carpeta *Crucita_Fashion/* y ejecutar el siguiente comando para crear la carpeta que contendrá el virtual environment
  ```shell
  mkdir env
  ```
  4. Crear el virtual environment con *virtualenv* o con el de su preferencia. Con virtualenv sería de la siguiente manera
  ```shell
  virtualenv env/ -p python3
  ```
  5. Instalar las dependencias del proyecto. Estas se encuentra en el archivo *requirements.txt* y se instalan con el siguiente comando
  ```shell
  pip install -r requirements.txt
  ```
  6. Realizar la configuración de la base de datos, esto se hace ejecutando el shell script llamado *installdb.sh* que esta ubicado en la raiz del proyecto. Al mismo nivel donde esta *manage.py*
  ```shell
  ./installdb.sh
  ```
  7. Ahora falta hacer las migraciones para terminar de configurar la base de datos, esto se hace con. **IMPORTANTE** todo esto se debe de hacer con el ambiente de trabajo activado que se hace con ```source env/bin/activate``` esto último se debe hacer cada vez que se quiera comenzar a trabajar en el proyecto. Para salir del ambiente ```deactivate```.
  ```shell
  python manage.py makemigrations
  ```
  
  ```shell
  python manage.py migrate
  ```
  8. Por último para verificar que todo ha sido configurado perfectamente corra el servidor con el siguiente comando. Si todo esta bien entonces al abrir en el navegador *localhost* deberia aparecer la página
  ```shell
  python manage.py runserver
  ```

Workflow (Flujo de trabajo)
---------------------------
### Organización de las ramas
<div style="text-align: justify;">
  Tendremos nuestra rama master que contendrá todas aquellas funcionalidades que estén listas para hacer usadas. Por cada sprint se creará una nueva rama llamada sprintN siendo N el número del sprint que se está realizando en este momento. Cada uno de los participantes del proyecto sacarán sus ramas del sprint que se está realizando actualmente el nombre de la rama a sacar se explicará más adelante.
</div>

### Creación de las ramas
  Como fue explicado anteriormente, por cada sprint habrá una rama que lo represente. Para cada uno de los participantes del Sprint actual seguirá las siguientes instrucciones para la creación de una rama.
  1. Cada participante creará una rama con el siguiente nombre *sprintN/(usuario-git)/(nombre-corto-de-la-tarea-asignada)*  siendo N el número del sprint actual. Con el siguiente comando se puede crear la rama
  ```shell
  git checkout -b sprintN/(usuario-git)/(nombre-corto-de-la-tarea-asignada)
  ```
  2. El desarrollador realizará toda su tarea en esa rama y las pruebas unitarias también se colocarán en su aqui.
  3. Si se quiere ver los tickets que lanza django en caso de error cambie el valor de DEBUG de False a True. Pero antes de pushear el cambio asegurese que esta variable vuelva a estar en False. Esta variable se encuentra en settings.py en la carpeta *crucita_fashion/*
  
### Merge de las ramas
  Luego de terminada una tarea por un participante del proyecto esta será revisada por el jefe del proyecto para realizar merge con la rama del Sprint. Por último cuando se termine el Sprint se procederá a realizar un pull requests para realizar la integración con la rama master y luego el deployment para que el cliente pueda empezar a usar inmediatamente las nuevas funcionalidades. **IMPORTANTE:** NO HACER PUSH DIRECTAMENTE EN MASTER.
