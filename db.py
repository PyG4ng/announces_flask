from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DSN = 'postgresql+psycopg2://django:django@localhost:5432/announces'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
