import sqlalchemy
from .db_session import SqlAlchemyBase


class Root(SqlAlchemyBase):
    __tablename__ = 'root'

    id = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    messages = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    root_prof = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                               autoincrement=True)

    def __repr__(self):
        return f"Root(id={self.id},name={self.name},password={self.password},message={self.messages}"
