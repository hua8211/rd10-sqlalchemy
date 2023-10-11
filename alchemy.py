from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
print(engine)

from sqlalchemy import Table, Column, Integer, String, MetaData
metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
print(repr(user_table.c.id))
print(repr(user_table.c.keys()))
print(repr(user_table.primary_key))


address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

metadata_obj.create_all(engine)

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

Base.metadata
Base.registry


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
sandy = User(name="sandy", fullname="Sandy Cheeks")
print(sandy)

print('Creating tables from Base metadata')
Base.metadata.create_all(engine)

squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

spongebob = User(name="spongebob", fullname="Spongebob Squarepants")
sandy = User(name="sandy", fullname="Sandy Cheeks")
patrick = User(name="patrick", fullname="Patrick Star")

print(squidward)

from sqlalchemy.orm import Session
from sqlalchemy import select
session = Session(engine)

session.add(squidward)
session.add(krabs)
session.add(spongebob)
session.add(sandy)
session.add(patrick)

print(session.new)

session.flush()

print(krabs)

some_squidward = session.get(User, 1)
print(some_squidward)
print(some_squidward is squidward)
session.commit()
print(some_squidward)
sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
print(sandy)
sandy.fullname = "Sandy Squirrel"
print(sandy)
print(sandy in session.dirty)
session.flush()
print(sandy in session.dirty)

patrick = session.get(User, 3)
print(patrick)

from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "spongebob")
print("STMT")
print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)

print(select(User))
row = session.execute(select(User)).first()
print(row)
print(row[0])
user = session.scalars(select(User)).first()
print(user)


print(select(User.name, User.fullname))
print('test')
row = session.execute(select(User.name, User.fullname)).first()
print(row)
result = session.execute(
    select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
).all()
print(result)