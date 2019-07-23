from main import db,bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(),nullable=True)

    # Create
    def createUser(self):
        db.session.add(self)
        db.session.commit()

    # fetch the data
    @classmethod
    def fetch_all(cls):
        records = UserModel.query.all()
        return records

    # check if email exists
    @classmethod
    def check_email_exist(cls,email):
        record = UserModel.query.filter_by(email=email)
        if record.first():
            return True
        else:
            return False

    # fetch by email
    @classmethod
    def fetch_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    # authenticate password
    @classmethod
    def check_password(cls,email,password):
        record = UserModel.query.filter_by(email=email).first()

        if record and bcrypt.check_password_hash(record.password,password):
            return True
        else:
            return False

    # Delete
    @classmethod
    def delete_by_id(cls, id):
        record = UserModel.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False