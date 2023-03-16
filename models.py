from gino import Gino
from sqlalchemy import Column, BigInteger, String, ForeignKey, Date, Time, Integer, Float
import sqlalchemy as sa
from typing import List
import config

db = Gino()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

class User(BaseModel):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    number = Column(BigInteger, nullable=True)
    worktime = Column(Integer, nullable=True)

class Time(BaseModel):
    __tablename__ = "time"

    driver = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    date = Column(Date, nullable=False)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)


class Auto(BaseModel):
    __tablename__ = "auto"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)
    consumption = Column(Float, nullable=False)
    tank = Column(Integer, nullable=False)


async def on_dbstartup():
    await db.set_bind(config.POSTGRES_URI)
    print("Connected to database succesfully!")
    if config.resetdb == 1:
        await db.gino.drop_all()
        await db.gino.create_all()
        print("Database was reseted")