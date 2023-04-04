
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

from const import Cfg

engine = create_engine(f'sqlite:///{Cfg.root_path}/sqlite3.db')
engine.connect()

Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    course_path = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    course_id_gb = Column(Integer, unique=True)
    lessons = relationship("Lesson", cascade="all, delete")

    def __str__(self):
        return f'{self.course_id_gb} {self.title}'


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    title = Column(String(700), nullable=False)
    lesson_path = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    course = Column(Integer, ForeignKey('courses.id'))
    content = relationship("Content", cascade="all, delete")


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    title = Column(String(700), nullable=False)
    content_path = Column(String(100), nullable=False)
    filename = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    lesson = Column(Integer, ForeignKey('lessons.id'))


# Base.metadata.create_all(engine)    # создание таблиц
# Base.metadata.drop_all(engine)      # удаление

session = Session(bind=engine)



