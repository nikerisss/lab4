import os
from functools import wraps
from turtledemo.chaos import f

import bcrypt
from flask import Flask, request, jsonify, make_response
from flask_bcrypt import check_password_hash
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.future import engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash
from flask import Flask, json, jsonify, request, make_response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, validates, ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager



app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))

#+os.path.join(basedir, 'db.postgresql')

app.config['SECRET_KEY']='1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5528@localhost:5432/forpp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

ma=Marshmallow(app)

jwt=JWTManager(app)

class User(db.Model):
    tablename = "User"
    user_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    userStatus = db.Column(db.String(20), nullable=False)

    def __init__(self, status, username, firstName, lastName, email, password, phone, userStatus):
        self.status = status
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phone = phone
        self.userStatus = userStatus




class Car(db.Model):
    tablename = "Car"
    car_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    make = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    transmition = db.Column(db.String(20), nullable=False)
    costPerHour = db.Column(db.String(20), nullable=False)


    def __init__(self, model, make, color, transmition, costPerHour):
        self.model = model
        self.make = make
        self.color = color
        self.transmition = transmition
        self.costPerHour = costPerHour


class Order(db.Model):
    tablename = "Order"
    id = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(String(20), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    carID = db.Column(db.Integer, ForeignKey(Car.car_id))
    userID = db.Column(db.Integer, ForeignKey(User.user_id))


    def __init__(self, startDate, duration, endDate, cost, status, complete, carID, userID, ):
        self.startDate = startDate
        self.duration = duration
        self.endDate = endDate
        self.cost = cost
        self.status = status
        self.complete = complete
        self.carID = carID
        self.userID = userID




class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'username', 'firstName', 'lastName', 'email', 'password', 'phone', 'userStatus')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'startDate', 'duration', 'endDate', 'cost', 'status', 'complete','carID', 'userID')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'model', 'make', 'color', 'transmition', 'costPerHour')


car_schema = CarSchema()
cars_schema = CarSchema(many=True)

#всі можуть
@app.route('/User', methods=['POST'])
def add_user():
    status = request.json['status']
    username = request.json['username']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    userStatus = request.json['userStatus']



    new_user = User(status,username, firstName, lastName, email, password, phone, userStatus)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

#всі можуть
@app.route('/User', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

#всі можуть
@app.route('/User/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)




@app.route('/User/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):

    current_identity_username = get_jwt_identity()
    user = User.query.get(id)

    if current_identity_username != user.username:
        return jsonify('Access is denided')

    status = request.json['status']
    username = request.json['username']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = request.json['password']
    phone = request.json['phone']
    userStatus = request.json['userStatus']

    user.status = status
    user.username = username
    user.firstName = firstName
    user.lastName = lastName
    user.email = email
    user.password = password
    user.phone = phone
    user.userStatus = userStatus
    db.session.commit()
    return user_schema.jsonify(user)



@app.route('/User/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_identity_username = get_jwt_identity()
    user = User.query.get(id)

    if current_identity_username != user.username:
        return jsonify('Access is denied')

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


def get_by_username(username):

    user = User.query.filter_by(username=username).first()

    return user

def get_by_id(id):

    user = User.query.filter_by(user_id=id).first()

    return user

@app.route('/Order', methods=['POST'])
@jwt_required()
def add_order():


    cur_ide = get_jwt_identity()

    cur_adm = get_by_username(cur_ide)
    #cur_adm = get_by_username(cur_ide.username)

    startDate = request.json['startDate']
    duration = request.json['duration']
    endDate = request.json['endDate']
    cost = request.json['cost']
    status = request.json['status']
    complete = request.json['complete']
    carID = request.json['carID']
    userID = request.json['userID']

    cur_use = get_by_id(userID)

    if cur_ide != cur_use.username:
        return jsonify('wrong user id in order ')


    new_order = Order( startDate, duration,endDate,cost,status,complete,carID, userID,)

    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order)


@app.route('/Order', methods=['GET'])
@jwt_required()
def get_orders():

    cur_ide = get_jwt_identity()

    cur_adm = get_by_username(cur_ide)

    if cur_adm.userStatus != 'admin':
        return jsonify('The access denied!Possibly you dont have enough rights')

    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result)


@app.route('/Order/<id>', methods=['GET'])
@jwt_required()
def get_order(id):
    cur_ide = get_jwt_identity()

    cur_adm = get_by_username(cur_ide)

    cur_use = get_by_id(id)

    if cur_ide != id:
        return jsonify('wrong user id in order ')

    car = Order.query.get(id)
    return order_schema.jsonify(car)


@app.route('/Order/<id>', methods=['PUT'])
@jwt_required()
def update_order(id):

    cur_ide = get_jwt_identity()

    order = Order.query.get(id)

    cur_use = get_by_username(cur_ide)

    #return jsonify({'id1':cur_use.user_id,'id2':Order.userID })
    if cur_use.user_id != order.userID:
        return jsonify('Accesss denied')


    startDate = request.json['startDate']
    duration = request.json['duration']
    endDate = request.json['endDate']
    cost = request.json['cost']
    status = request.json['status']
    complete = request.json['complete']
    carID = request.json['carID']

    order.startDate = startDate
    order.duration = duration
    order.endDate = endDate
    order.cost = cost
    order.status = status
    order.complete = complete
    order.carID = carID

    db.session.commit()
    return order_schema.jsonify(order)


@app.route('/Order/<id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    cur_ide = get_jwt_identity()

    order = Order.query.get(id)

    cur_use = get_by_username(cur_ide)

    # return jsonify({'id1':cur_use.user_id,'id2':Order.userID })
    if cur_use.user_id != order.userID:
        return jsonify('Accesss denied')

    order= Order.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)


@app.route('/login', methods=['GET','POST'])
def login():

    auth = request.authorization


    if not auth or not auth.username or not auth.password:
        return make_response('could', 401)

    # access_token = create_access_token(identity=auth.username)
    # return jsonify({'token ': access_token})
    #user = session.query(User).filter_by(username=auth.username).first()
    user = get_by_username(auth.username)
    # user =
    # user_obj = user.query.filter_by(username=auth.username).first()

    if (user.password == auth.password):
        token1 = create_access_token(identity=user.username)
        return jsonify({'token ': token1})


    return make_response('not',401)

@app.route('/Car', methods=['POST'])
@jwt_required()
def add_car():

    cur_ide = get_jwt_identity()

    cur_adm = get_by_username(cur_ide)

    if cur_adm.userStatus != 'admin':
        return jsonify('The access denied!Possibly you dont have enough rights')


    model = request.json['model']
    make = request.json['make']
    color = request.json['color']
    transmition = request.json['transmition']
    costPerHour = request.json['costPerHour']
    new_car = Car(model, make, color, transmition, costPerHour)

    db.session.add(new_car)
    db.session.commit()
    return car_schema.jsonify(new_car)


@app.route('/Car', methods=['GET'])
def get_cars():


    all_cars = Car.query.all()
    result = cars_schema.dump(all_cars)
    return jsonify(result)


@app.route('/Car/<id>', methods=['GET'])
def get_car(id):
    car = Car.query.get(id)
    return car_schema.jsonify(car)


@app.route('/Car/<id>', methods=['PUT'])
@jwt_required()
def update_car(id):

    cur_ide = get_jwt_identity()

    cur_adm = get_by_username(cur_ide)

    if cur_adm.userStatus != 'admin':
        return jsonify('The access denied!Possibly you dont have enough rights')


    car = Car.query.get(id)

    model = request.json['model']
    make = request.json['make']
    color = request.json['color']
    transmition = request.json['transmition']
    costPerHour = request.json['costPerHour']

    car.model = model
    car.make = make
    car.color = color
    car.transmition = transmition
    car.costPerHour = costPerHour

    db.session.commit()
    return car_schema.jsonify(car)


@app.route('/Car/<id>', methods=['DELETE'])
@jwt_required()
def delete_car(id):
    cur_ide = get_jwt_identity()

    cur_adm = get_by_username(cur_ide)

    if cur_adm.userStatus != 'admin':
        return jsonify('The access denied!Possibly you dont have enough rights')

    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    return car_schema.jsonify(car)


@app.errorhandler(404)
def pageNotFound(error):
    return "page not found"



@app.errorhandler(400)
def handle_400_error(error):
    return make_response(jsonify({'error' : 'Bad  request'}),400)


if __name__=='__main__':
    app.run(debug=True)
    print("-----------------")