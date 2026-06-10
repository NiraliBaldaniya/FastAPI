from sqlalchemy import Column,Integer,String
from db import base

class URL(base):

	__tablename__ = "urls"

	id = Column(Integer,primary_key=True,index=True)

	long_code = Column(String)

	short_code = Column(String,index=True,unique=True)