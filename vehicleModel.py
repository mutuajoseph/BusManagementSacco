from main import db

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    plateNo = db.Column(db.String(50), nullable=False)
    seats = db.Column(db.String(120), nullable=True)
    route = db.Column(db.String(50), nullable=False)
    licenseNo = db.Column(db.String(50), nullable=False)
    insuranceCompany = db.Column(db.String(50), nullable=False)
    insuranceExpiryDate = db.Column(db.String(50), nullable=False)
    operatorId = db.Column(db.Integer,db.ForeignKey('operators.id'))
    employees = db.relationship('Employees',backref='vehicle')


    # create
    def create_vehicles(self):
        db.session.add(self)
        db.session.commit()

    # Method for reading data
    @classmethod
    def fetch_all(cls):
        VehiclesRecords = Vehicles.query.all()
        return VehiclesRecords

    # fetch_all
    @classmethod
    def fetch_all(cls):
        records = Vehicles.query.all()
        return records

    # Delete
    @classmethod
    def delete_by_id(cls, id):
        record = Vehicles.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False