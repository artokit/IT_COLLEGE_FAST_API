import sqlite3
connect = sqlite3.connect('db.sqlite', check_same_thread=False)
cursor = connect.cursor()


class DefaultDBTable:
    table_name = None
    fields = ('pk', 'brand', 'model', 'year_of_issue', 'vin_code')

    @classmethod
    def get_all(cls):
        res = cursor.execute(f'SELECT {",".join(cls.fields)} FROM {cls.table_name}').fetchall()
        return [dict(zip(cls.fields, i)) for i in res]

    @classmethod
    def create(cls, **kwargs):
        keys = ", ".join(kwargs.keys())
        values_questions = "?,".join([""]*len(kwargs.values())) + '?'
        cursor.execute(f'INSERT INTO {cls.table_name} ({keys}) VALUES ({values_questions})', tuple(kwargs.values()))
        connect.commit()
        kwargs['pk']: cursor.lastrowid
        return kwargs

    @classmethod
    def get_by_pk(cls, pk):
        res = cursor.execute(f'SELECT * FROM {cls.table_name} WHERE pk = ?', (pk, ))
        return res.fetchone()

    @classmethod
    def delete_by_pk(cls, pk):
        cursor.execute(f'DELETE FROM {cls.table_name} where pk = ?', (pk, ))
        connect.commit()
        return pk

    @classmethod
    def update_by_pk(cls, pk, **kwargs):
        set_text = ', '.join([f'''{i} = {kwargs[i] if isinstance(kwargs[i], int) else f"'{kwargs[i]}'"}'''
                              for i in kwargs if kwargs[i]])
        print(f'UPDATE {cls.table_name} SET {set_text} where pk = {pk}')
        cursor.execute(f'UPDATE {cls.table_name} SET {set_text} where pk = ?', (pk, ))
        connect.commit()


class Car(DefaultDBTable):
    table_name = 'cars'
    fields = ('pk', 'brand', 'model', 'year_of_issue', 'vin_code')

    @classmethod
    def get_cars(cls, ids: list[int]):
        print(f'SELECT * FROM {cls.table_name} WHERE `pk` in ({",".join(map(str, ids))}')
        res = cursor.execute(
            f'SELECT * FROM {cls.table_name} WHERE `pk` in (?)', (','.join(map(str, ids)),)
        ).fetchall()
        return [dict(zip(cls.fields, i)) for i in res]


class Order(DefaultDBTable):
    table_name = 'orders'
    fields = ('pk', 'car_pk', 'client_pk', 'date', 'description', 'status')

    @classmethod
    def get_by_client_pk(cls, pk):
        res = cursor.execute('SELECT * FROM ORDERS WHERE client_pk = ?', (pk, )).fetchall()
        return [dict(zip(cls.fields, i)) for i in res]


class Client(DefaultDBTable):
    table_name = 'clients'

    @classmethod
    def get_all(cls):
        return
