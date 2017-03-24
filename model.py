from datetime import *
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask import *
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    dob = Column(Date)
    city = Column(String)
    address = Column(String)
    zipcode = Column(String)
    business = relationship("Business", back_populates="owner")


class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True) #Thats how you log in
    hash_password = Column(String)      #Thats how you log in
    city = Column(String)
    address = Column(String)
    zipcode = Column(String)
    category = Column(String)
    #comments = relationship("Comment", back_populates="business") #Not yet here
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship("Owner", back_populates="business")

    def hash_password(self, password):
        self.hash_password = pwd_context.encrypt(password)

    def verify_password(self, spassword):
        return pwd_context.verify(password, self.hash_password)



engine = create_engine('sqlite:///database.db')


Base.metadata.create_all(engine)
