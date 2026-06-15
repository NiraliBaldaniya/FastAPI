from sqlalchemy import Column,Integer,String, column
from db import base

class Url(base):

	__tablename__ = "urls"

	id = Column(Integer,primary_key=True,index=True)

	long_url = Column(String)

	code = Column(String,index=True,unique=True)

	created_at = Column(String)

	clicks = Column(Integer, default=0)