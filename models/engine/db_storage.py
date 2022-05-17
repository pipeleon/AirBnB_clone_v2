#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                           format(format(os.getenv('HBNB_MYSQL_USER'), 
                           os.getenv('HBNB_MYSQL_PWD'), 
                           os.getenv('HBNB_MYSQL_HOST'), 
                           os.getenv('HBNB_MYSQL_DB')),
                           pool_pre_ping=True)
    
    def all(self, cls=None):
        if cls == None:
            new_dict = {}
            query = self.__session.query(cls)
            for q in query:
                new_dict["{}.{}".format(type(q).__name__, q.id)] = q
            return new_dict
        else:
            new_dict = {}
            query = self.__session.query(cls)
            for q in query:
                new_dict["{}.{}".format(cls.__name__, q.id)] = q
            return new_dict
    
    def new(self, obj):
        self.__session.add(obj)

    def save(self): 
        self.__session.commit()
    
    def delete(self, obj=None):
        if not obj is None:
            self.__session.delete(obj)
    
    def reload(self):
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = Session()
