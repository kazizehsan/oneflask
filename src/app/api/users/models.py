import uuid
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jti

from extensions import db
from app.api.base.model_mixins import TimeAudit
from .signals import admin_user_post_save, client_user_post_save


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


class AdminUser(TimeAudit, UserBase):
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    designation = db.Column(db.String(50), nullable=True)

    def save(self, **kw):
        created = False if self.id else True
        db.session.add(self)
        db.session.commit()
        if 'send_signal' in kw and kw['send_signal']:
            admin_user_post_save.send(self, created=created)
        return self

    def update(self, data_update, **kw):
        db.session.query(AdminUser).filter(AdminUser.id == self.id).update(data_update, synchronize_session=False)
        db.session.commit()
        if 'send_signal' in kw and kw['send_signal']:
            admin_user_post_save.send(self, created=False)
        return self

    def delete(self, **kw):
        db.session.delete(self)
        db.session.commit()
        return True


class ClientUser(TimeAudit, UserBase):
    __tablename__ = 'client_users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization = db.Column(db.String(50), nullable=True)
    client_token = db.relationship(
        "ClientToken", backref="client_user",
        cascade="all, delete", uselist=False
    )

    def save(self, **kw):
        created = False if self.id else True
        db.session.add(self)
        db.session.commit()
        if 'send_signal' in kw and kw['send_signal']:
            client_user_post_save.send(self, created=created)
            jwt_user_claims = {
                'type': 'api',
                'user': 'client'
            }
            api_token = create_access_token(self.email, expires_delta=False, user_claims=jwt_user_claims)
            client_token = ClientToken()
            client_token.revoked = False
            client_token.client_user = self
            client_token.jti = get_jti(api_token)
            client_token.save()
            return self, api_token
        return self

    def update(self, data_update, **kw):
        db.session.query(ClientUser).filter(ClientUser.id == self.id).update(data_update, synchronize_session=False)
        db.session.commit()
        if 'send_signal' in kw and kw['send_signal']:
            client_user_post_save.send(self, created=False)
        return self

    def delete(self, **kw):
        db.session.delete(self)
        db.session.commit()
        return True


class ClientToken(TimeAudit, db.Model):
    __tablename__ = 'client_tokens'

    id = db.Column(db.Integer, primary_key=True)
    client_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client_users.id', ondelete="CASCADE"))
    jti = db.Column(db.String(36), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    def save(self, **kw):
        created = False if self.id else True
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data_update, **kw):
        db.session.query(ClientToken).filter(ClientToken.id == self.id).update(data_update, synchronize_session=False)
        db.session.commit()
        return self

    def delete(self, **kw):
        db.session.delete(self)
        db.session.commit()
        return True
