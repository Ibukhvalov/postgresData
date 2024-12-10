from random import randint

from sqlalchemy import create_engine, MetaData, Column, CHAR, Integer, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import random

engine = create_engine(
    'postgresql+psycopg2://postgres:345672176@localhost/xmas',
    echo = True,
)

Base = declarative_base()
metadata = MetaData()

class region_postcodes(Base):
    __tablename__ = 'region_postcodes'

    postcode = Column(CHAR(6), primary_key = True)
    region_id = Column(Integer)

    def __init__(self, region_id, postcode):
        self.region_id = region_id
        self.postcode = postcode

    def __repr__(self):
        return f'{self.postcode} relates to {self.region_id}'

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)

region_id_list = [i+1 for i in range(22)]
print(region_id_list)


def generate_postcodes(number_of_postcodes):
    if number_of_postcodes > 10e6:
        return []

    result = []

    inserted_region_id = set()
    for i in range(number_of_postcodes):
        while(True):
            postcode = randint(0, int(999999))
            if postcode not in inserted_region_id:
                inserted_region_id.add(postcode)
                break
        postcode = str(postcode)
        while(len(postcode) < 6):
            postcode = '0'+postcode

        result.append(postcode)

    return result


number_of_postcodes = 200

    

with Session() as session:

    postcodes = generate_postcodes(number_of_postcodes)
    for postcode in postcodes:
        rel = region_postcodes(randint(1,22), postcode)
        session.add(rel)
    session.commit()