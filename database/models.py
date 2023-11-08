from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Text
from sqlalchemy.orm import declarative_base, Session

engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5431/production"
)
connect = engine.connect()
Base = declarative_base()
session = Session(engine)

cars = Table(
    'cars',
    Base.metadata,
    Column("pk", Integer, primary_key=True, autoincrement=True),
    Column("brand", Text, nullable=False),
    Column("model", Text, nullable=False),
    Column("year_of_issue", Integer, nullable=False),
    Column("vin_code", Text, nullable=False, unique=True)
)

clients = Table(
    'clients',
    Base.metadata,
    Column('pk', Integer, primary_key=True, nullable=False, autoincrement=True),
    Column('first_name', Text, nullable=False),
    Column('last_name', Text, nullable=False),
    Column('address', Text, nullable=False, unique=True),
    Column('number', Text, nullable=False, unique=True)
)

orders = Table(
    'orders',
    Base.metadata,
    Column('pk', Integer, nullable=False, unique=True, autoincrement=True),
    Column('car_pk', Integer, ForeignKey('cars.pk'), nullable=False, unique=True),
    Column('client_pk', Integer, ForeignKey('clients.pk'), nullable=False),
    Column('date', Text, nullable=False),
    Column('description', Text),
    Column('status', Text, nullable=False)
)
