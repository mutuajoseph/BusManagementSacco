from main import db


class Operators(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    telephoneNo =  db.Column(db.Integer, nullable=True)
    vehicles = db.relationship('Vehicles',backref='operator')
    contributions = db.relationship('Contributions',backref='operatorname')



    # create
    def create_operators(self):
        db.session.add(self)
        db.session.commit()

    # Method for reading data
    @classmethod
    def fetch_all(cls):
        OperatorsRecords = Operators.query.all()
        return OperatorsRecords

    # fetch all
    @classmethod
    def fetch_all(cls):
        records = Operators.query.all()
        return records

    # Method for reading data
    @classmethod
    def fetch_by_email(cls,email):
        OperatorsRecord = Operators.query.filter_by(email=email).first()
        return OperatorsRecord


    @classmethod
    def check_password(cls,email,password):
        record = Operators.query.filter_by(email=email).first()

        if record:
            return True
        else:
            return  False

    # Delete
    @classmethod
    def delete_by_id(cls,id):
        record = Operators.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False

    # UPDATE
    @classmethod
    def update_by_id(cls,id,newEmail,newPassword,newFirstname,newLastname,newGender,newTelephoneNo):
        record = Operators.query.filter_by(id=id).first()
        if record:
            record.email = newEmail
            record.password = newPassword
            record.firstname = newFirstname
            record.lastname = newLastname
            record.gender = newGender
            record.telephoneNo = newTelephoneNo
            db.session.commit()
            return True
        else:
            return False

    # check if email exists
    @classmethod
    def check_email_exist(cls, email):
        record = Operators.query.filter_by(email=email)
        if record.first():
            return True
        else:
            return False

    # authenticate password
    @classmethod
    def check_password(cls, email, password):
        record = Operators.query.filter_by(email=email).first()
        if record.password == password:
             return True
        else:
            return False
