#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class DBStorage:
    """ Class for DatabaseStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor method"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                           format(os.getenv('HBNB_MYSQL_USER'), 
                           os.getenv('HBNB_MYSQL_PWD'), 
                           os.getenv('HBNB_MYSQL_HOST'), 
                           os.getenv('HBNB_MYSQL_DB')),
                           pool_pre_ping=True)
    
    def all(self, cls=None):
        """Show all instance depending on the class"""
        from models.base_model import BaseModel
        from models.city import City
        from models.state import State
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        
        if cls == None:
            new_dict = {}
            query = self.__session.query(State, City, User, Place, Review, Amenity).all()
            for q in query:
                new_dict["{}.{}".format(type(q).__name__, q.id)] = q
            return new_dict
        else:
            new_dict = {}
            query = self.__session.query(cls).all()
            for q in query:
                new_dict["{}.{}".format(cls.__name__, q.id)] = q
            return new_dict
    
    def new(self, obj):
        self.__session.add(obj)
        self.save()

    def save(self): 
        self.__session.commit()
    
    def delete(self, obj=None):
        if not obj is None:
            self.__session.delete(obj)
        self.save()
    
    def reload(self):
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
