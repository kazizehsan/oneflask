import uuid

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.base.model_mixins import TimeAudit
from extensions import db
from .signals import user_post_save


class UserBase(db.Model):
    __abstract__ = True

    email = db.Column(db.String(254), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, server_default=text('FALSE'))
    password = db.Column(db.String(128), nullable=True)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)


class User(TimeAudit, UserBase):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    designation = db.Column(db.String(50), nullable=True)
    organization = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, server_default=text('FALSE'))
    api_token = db.relationship(
        "APIToken", backref="user",
        cascade="all, delete", uselist=False
    )

    def save(self, **kw):
        created = False if self.id else True
        db.session.add(self)
        db.session.commit()
        if 'send_signal' in kw and kw['send_signal']:
            user_post_save.send(self, created=created)
        return self

    def update(self, data_update, **kw):
        db.session.query(User).filter(User.id == self.id).update(data_update, synchronize_session=False)
        db.session.commit()
        if 'send_signal' in kw and kw['send_signal']:
            user_post_save.send(self, created=False)
        return self

    def delete(self, **kw):
        db.session.delete(self)
        db.session.commit()
        return True


class APIToken(TimeAudit, db.Model):
    __tablename__ = 'api_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete="CASCADE"))
    jti = db.Column(db.String(36), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    def save(self, **kw):
        created = False if self.id else True
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data_update, **kw):
        db.session.query(APIToken).filter(APIToken.id == self.id).update(data_update, synchronize_session=False)
        db.session.commit()
        return self

    def delete(self, **kw):
        db.session.delete(self)
        db.session.commit()
        return True
