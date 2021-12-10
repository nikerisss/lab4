from sqlalchemy import String, Integer, Float, ForeignKey, Column, Date, Boolean, update, insert, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:Wight_wolf2000@127.0.0.1:3306/orm', echo=True)

Base = declarative_base()


class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True)
    carID = Column(Integer, ForeignKey("Car.id"), nullable=False)
    userID = Column(Integer, ForeignKey("User.id"), nullable=False)
    startDate = Column(Date, nullable=False)
    duration = Column(Float, nullable=False)
    endDate = Column(Date, nullable=False)
    cost = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    complete = Column(Boolean, nullable=False)


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False)
    firstName = Column(String(20), nullable=False)
    lastName = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    userStatus = Column(String(20), nullable=False)


class Car(Base):
    __tablename__ = "Car"
    id = Column(Integer, primary_key=True)
    model = Column(String(20), nullable=False)
    make = Column(String(20), nullable=False)
    color = Column(String(20), nullable=False)
    transmition = Column(String(20), nullable=False)
    costPerHour = Column(String(20), nullable=False)




