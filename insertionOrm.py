from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from myORM import Car, User, Order

engine = create_engine('mysql+mysqlconnector://root:Wight_wolf2000@127.0.0.1:3306/orm', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

car1 = Car(id=1, model="Tesla", make="Model X", color="black", transmition="60D", costPerHour=150)
car2 = Car(id=2, model="Nissan", make="Leaf", color="white", transmition="8.193:1", costPerHour=100)
car3 = Car(id=3, model="Daewoo", make="Lanos", color="Navy", transmition="Daewoo D16", costPerHour=30)

user1 = User(id=1, status="approved", username="killer", firstName="Vasyl", lastName="Pupkin",
             email="vasyapup@gmail.com",
             password="q1w2e3", phone="+380661789668", userStatus="user")
user2 = User(id=2, status="in use", username="motherBoy", firstName="Danila", lastName="Poperechnyi",
             email="poperek@gmail.com",
             password="a1b2c3", phone="+380952286928", userStatus="user")

user3 = User(id=3, status="placed", username="primabalerina", firstName="Kostia", lastName="Salo",
             email="kostiaSalo@gmail.com",
             password="12345678", phone="+380964848522", userStatus="user")

order1 = Order(id="1", carID=2, userID=3, startDate="2021-10-28", duration=2, endDate="2021-10-28", cost=200,
               status="in use", complete=False)
order2 = Order(id="2", carID=3, userID=1, startDate="2021-10-28", duration=2, endDate="2021-10-28", cost=200,
               status="in use", complete=False)

session.add_all([car1, car2, car3])
session.add_all([user1, user2, user3])
session.commit()

session.add_all([order1])
session.commit()
