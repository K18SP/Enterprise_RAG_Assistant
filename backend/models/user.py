from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    username = Column(

        String,

        unique=True,

        nullable=False,

        index=True

    )

    email = Column(

        String,

        unique=True,

        nullable=False,

        index=True

    )

    password_hash = Column(

        String,

        nullable=False

    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )