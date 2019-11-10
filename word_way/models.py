from sqlalchemy import Column, Unicode

from .orm import Base


__all__ = 'Test',


class Test(Base):

    id = Column(Unicode, nullable=False, primary_key=True)

    __tablename__ = 'Test'
