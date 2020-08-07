# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE

class NogizakaMemberTable(Base):
    __tablename__ = 'nogizaka'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)


def main():
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main()