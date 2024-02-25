import sqlalchemy as db
from sqlalchemy.orm import relationship, Mapped
from sql_alchemy.database import Base, sync_engine


class TagsOrm(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    problems = relationship('ProblemsOrm', back_populates='tag', lazy='selectin')
    
class ProblemsOrm(Base):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    solved_count = db.Column(db.Integer)
    rating = db.Column(db.Integer, nullable=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    tag = relationship('TagsOrm', back_populates='problems', lazy='selectin')

# , lazy='selectin'
Base.metadata.create_all(sync_engine)