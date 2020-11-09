from sqlalchemy.ext.declarative import declared_attr
from extensions import db


class TimeAudit(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=db.func.now(), onupdate=db.func.now())
