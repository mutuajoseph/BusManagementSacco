from main import db


class Contributions(db.Model):
    __tablename__ = 'contributions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    dateTime = db.Column(db.String(30), nullable=True)
    paymentForm = db.Column(db.String(50), nullable=False)
    operator_id = db.Column(db.Integer,db.ForeignKey('operators.id'))
    operator = db.relationship('Operators')


    # create
    def create_contributions(self):
        db.session.add(self)
        db.session.commit()

    # fetch all
    @classmethod
    def fetch_all(cls):
        records = Contributions.query.all()
        return records

    # Method for reading data
    @classmethod
    def fetch_all(cls):
        ContributionsRecords = Contributions.query.all()
        return ContributionsRecords

    # Delete
    @classmethod
    def delete_by_id(cls, id):
        record = Contributions.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False


    # UPDATE

    @classmethod
    def update_by_id(cls, id, newAmount, newDateTime, newPaymentForm, ):
        record = Contributions.query.filter_by(id=id).first()
        if record:
            record.amount = newAmount
            record.dateTime = newDateTime
            record.paymentForm = newPaymentForm
            db.session.commit()
            return True
        else:
            return False