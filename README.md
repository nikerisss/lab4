# lab4

 Install pip library
 Install virtualenv and creating virtual enviroment
 Install pyenv and choose python version
 Create Flask project
 Add adress to the localhost
 Add the variant to "Hello world"
 Install library for server(from gevent.pywsgi import WSGIServer)
 Show the result

# lab6

need to install mySql

in mySqlShell:
    
    \connect root:[password]@127.0.0.1:3306
    create database orm;
    use orm;

install alembic (in terminal):

    pip install alembic

write into alembic.ini (find sqlalchemy.url =):

    sqlalchemy.url = mysql+mysqlconnector://root:[password]@127.0.0.1:3306/[orm]

write into env.py (find url = ""):
    
    url =  "mysql+mysqlconnector://root:[password]@127.0.0.1:3306/[orm]"

write into PyCharm terminal to create table

    alembic revision --autogenerate -m "first"
    alembic upgrade head

compile insertionOrm.py to insert new fields in DataBase