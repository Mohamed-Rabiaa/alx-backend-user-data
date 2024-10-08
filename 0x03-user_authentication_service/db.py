#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database

        Args:
            email (str): The user's email
            hashed_password (str): The user's hashed password

        Returns:
            (User): A User object
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds the user with the kwargs arttributes

        Args:
            kwargs (dict): a dictionary contains arbitrary keyword
            arguments

        Returns:
            The first row found in the users table as filtered by
            the method’s input arguments
        """
        valid_columns = set(c.name for c in User.__table__.columns)
        for key in kwargs:
            if key not in valid_columns:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the user with the user_id

        Args:
            user_id (str): The id of the user to update
            kwargs (dict): The artributes of the user that
            we will update
        """
        user = self.find_user_by(id=user_id)
        valid_columns = set(c.name for c in User.__table__.columns)
        for key, value in kwargs.items():
            if key in valid_columns:
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
