import sqlalchemy as db
from sqlalchemy.orm import relationship, Mapped
from sql_alchemy.database import Base, sync_engine


class TagsOrm(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    tag_problems: Mapped[list['ProblemsOrm']] = relationship(
        back_populates='problem_tags', 
        secondary='problems_tags',
        lazy='selectin')
    
class ProblemsOrm(Base):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    solved_count = db.Column(db.Integer)
    rating = db.Column(db.Integer, nullable=True)
    problem_tags: Mapped[list['TagsOrm']] = relationship(
        back_populates='tag_problems', 
        secondary='problems_tags',
        lazy='selectin')

class ProblemsTagsOrm(Base):
    __tablename__ = 'problems_tags'
    tag_id = db.Column(db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    problem_id = db.Column(db.ForeignKey('problems.id', ondelete='CASCADE'), primary_key=True)
            
Base.metadata.create_all(sync_engine)