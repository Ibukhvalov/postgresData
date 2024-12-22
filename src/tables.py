from sqlalchemy import create_engine, MetaData, Column, CHAR, Integer, text, VARCHAR, Date, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.functions import random

engine = create_engine(
    'postgresql+psycopg2://postgres:345672176@localhost/xmas',
    echo = True,
)

Base = declarative_base()
metadata = MetaData()

class Region(Base):
    __tablename__ = 'data.region'
    id = Column(INTEGER, )

class RegionPostcodes(Base):
    __tablename__ = 'data.region_postcodes'

    postcode = Column(CHAR(6), primary_key = True, nullable=False)
    region_id = Column(Integer, ForeignKey("data.region.id", ondelete = "CASCADE"))

    def __init__(self, region_id, pcode):
        self.region_id = region_id
        self.postcode = pcode

    def __repr__(self):
        return f'{self.postcode} relates to {self.region_id}'

class Child(Base):
    __tablename__ = 'data.child'

    birth_certificate = Column(CHAR(6), primary_key=True, nullable=False)
    password = Column(VARCHAR(20), nullable=False)
    full_name = Column(VARCHAR(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    postcode = Column(CHAR(6),ForeignKey("data.region_postcodes.postcode", ondelete="CASCADE"), nullable=False)
    number_of_good_deeds = Column(Integer)
    number_of_misdeeds = Column(Integer)


