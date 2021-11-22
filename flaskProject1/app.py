import bcrypt
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy import String, Integer, ForeignKey, Date, BOOLEAN

app = Flask(__name__)



@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})


besedir = os.path.abspath(os.path.dirname(__file__))
sqldb = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:fd546ut81w@localhost:3306/l6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    tablename = "User"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
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


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'username', 'firstName', 'lastName', 'email', 'password', 'phone', 'userStatus')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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

    hased = bcrypt.hashpw(password.encode('utf-8', 'ignore'), bcrypt.gensalt())

    new_user = User(status,username, firstName, lastName, email, hased, phone, userStatus)

    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


@app.route('/User', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/User/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route('/User/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

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
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


# _____________CAR___________________________________________________________________
class Car(db.Model):
    __tablename__ = "Car"
    id = db.Column(db.Integer, primary_key=True)
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


class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'model', 'make', 'color', 'transmition', 'costPerHour')


car_schema = CarSchema()
cars_schema = CarSchema(many=True)


@app.route('/Car', methods=['POST'])
def add_car():
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
def update_car(id):
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
def delete_car(id):
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



# _____________ORDER___________________________________________________________________
class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(String(20), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    carID = db.Column(db.Integer, db.ForeignKey("Car.id"))
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))

    '''User = relationship("User")
    Car = relationship("Car")'''

    def __init__(self, startDate, duration, endDate, cost, status, complete, carID, userID,):
        self.startDate = startDate
        self.duration = duration
        self.endDate = endDate
        self.cost = cost
        self.status = status
        self.complete = complete
        self.carID = carID
        self.userID = userID


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'startDate', 'duration', 'endDate', 'cost', 'status', 'complete','carID', 'userID')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)



@app.route('/Order', methods=['POST'])
def add_order():
    startDate = request.json['startDate']
    duration = request.json['duration']
    endDate = request.json['endDate']
    cost = request.json['cost']
    status = request.json['status']
    complete = request.json['complete']
    carID = request.json['carID']
    userID = request.json['userID']


    new_order = Order( startDate, duration,endDate,cost,status,complete,carID, userID,)

    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order)


@app.route('/Order', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result)


@app.route('/Order/<id>', methods=['GET'])
def get_order(id):
    car = Order.query.get(id)
    return order_schema.jsonify(car)
@app.route('/Order/<id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)

    startDate = request.json['startDate']
    duration = request.json['duration']
    endDate = request.json['endDate']
    cost = request.json['cost']
    status = request.json['status']
    complete = request.json['complete']
    carID = request.json['carID']
    userID = request.json['userID']

    order.startDate = startDate
    order.duration = duration
    order.endDate = endDate
    order.cost = cost
    order.status = status
    order.complete = complete
    order.carID = carID
    order.userID = userID

    db.session.commit()
    return order_schema.jsonify(order)


@app.route('/Order/<id>', methods=['DELETE'])
def delete_order(id):
    order= Order.query.get(id)
    db.session.delete(order)
    db.session.commit()

    return order_schema.jsonify(order)


if __name__ == '__main__':
    app.run(debug=True)
