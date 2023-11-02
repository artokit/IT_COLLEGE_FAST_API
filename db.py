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
# Base.metadata.create_all(engine)


class DefaultDBTable:
    table = None
    fields = None

    @classmethod
    def create(cls, **kwargs):
        session.execute(cls.table.insert().values(**kwargs))
        session.commit()
        kwargs['pk'] = session.query(cls.table).order_by(cls.table.c.pk).first()[0]
        return kwargs

    @classmethod
    def get_by_pk(cls, pk):
        res = cls.table.select().where(cls.table.c.pk == pk)
        return session.execute(res).fetchone()

    @classmethod
    def delete_by_pk(cls, pk):
        session.execute(cls.table.delete().where(cls.table.c.pk == pk))
        session.commit()
        return pk

    @classmethod
    def update_by_pk(cls, pk, **kwargs):
        kwargs = {i: kwargs[i] for i in kwargs if kwargs[i] is not None}
        session.execute(cls.table.update().values(**kwargs).where(cls.table.c.pk == pk))
        session.commit()


class Car(DefaultDBTable):
    table = cars
    fields = ('pk', 'brand', 'model', 'year_of_issue', 'vin_code')

    @classmethod
    def get_cars(cls, ids: list[int]):
        res = session.execute(cls.table.select().where(cars.c.pk.in_(tuple(ids)))).fetchall()
        return [dict(zip(cls.fields, i)) for i in res]


class Order(DefaultDBTable):
    table = orders
    fields = ('pk', 'car_pk', 'client_pk', 'date', 'description', 'status')

    @classmethod
    def get_by_client_pk(cls, pk):
        res = session.execute(cls.table.select().where(cls.table.c.client_pk == pk)).fetchall()
        return [dict(zip(cls.fields, i)) for i in res]


class Client(DefaultDBTable):
    table = clients
