from gino import Gino
from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Integer, Float, Date
import sqlalchemy as sa
from typing import List
import config

db = Gino()
dbb = Gino()


class BaseModel(db.Model, dbb.Model):
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



class City(BaseModel):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)


class Base(BaseModel):
    __tablename__ = "base"

    id = Column(BigInteger, primary_key=True)
    city = Column(Integer, ForeignKey("city.id"), nullable=False)
    name = Column(String, nullable=False)

class User(BaseModel):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(Integer, ForeignKey("city.id"), nullable=False)
    base = Column(Integer, ForeignKey("base.id"), nullable=False)
    mode = Column(Integer, nullable=False)
    workdays = Column(Integer, nullable=True)
    last_km = Column(Integer, nullable=True)
    last_fuel = Column(Float, nullable=True)


class Time(BaseModel):
    __tablename__ = "time"

    id = Column(Integer, primary_key=True)
    driver = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    c = Column(Float, nullable=False)
    total = Column(Float, nullable=False)


class Auto(BaseModel):
    __tablename__ = "auto"

    id = Column(BigInteger, primary_key=True)
    city = Column(Integer, ForeignKey("city.id"), nullable=False)
    name = Column(String(40), unique=True, nullable=False)
    consumption = Column(Float, nullable=False)
    tank = Column(Integer, nullable=False)


class Contacts(BaseModel):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    city = Column(Integer, ForeignKey("city.id"), nullable=False)
    position = Column(String(50), nullable=False)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    middle_name = Column(String(25))
    comment = Column(String(100))
    phone = Column(String(12), nullable=False, unique=True)


class Turnover(BaseModel):
    __tablename__ = "turnover"

    id = Column(Integer, primary_key=True)
    driver = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    cash = Column(Float, nullable=False)
    date = Column(Date, nullable=False)


class Fuel(BaseModel):
    __tablename__ = "fuel"

    id = Column(Integer, primary_key=True)
    driver = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    milleage = Column(Integer, nullable=False)
    fuel_delta = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)


async def db_bind():
    await db.set_bind(config.POSTGRES_URI)


async def db_reset():
    await db.gino.drop_all()
    await db.gino.create_all()