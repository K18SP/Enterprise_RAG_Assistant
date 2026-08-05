from database.database import Base
from database.database import engine

from models.user import User


def initialize_database():

    Base.metadata.create_all(

        bind=engine

    )