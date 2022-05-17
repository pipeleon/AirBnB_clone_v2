#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="states")
    else:
        @property
        def cities(self):
            """Getter attribute for cities where returns depdending on id"""
            from models import storage
            from models.city import City
            list = []
            cities = storage.all(City)
            for value in cities.values():
                if value.state_id == self.id:
                    list.append(value)
            return list      
