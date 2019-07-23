from main import db


class Employees(db.Model):
      __tablename__= 'employees'
      id = db.Column(db.Integer, primary_key=True)
      email = db.Column(db.String(100), nullable=False, unique=True)
      firstName = db.Column(db.String(120), nullable=False,)
      lastName = db.Column(db.String(120), nullable=False,)
      staff_id = db.Column(db.Integer, nullable=True, unique=True)
      role = db.Column(db.String(50), nullable=False)
      vehicleId = db.Column(db.Integer,db.ForeignKey('vehicles.id'),nullable=True)



      # create
      def create_employees(self):
          db.session.add(self)
          db.session.commit()

      # Method for reading data
      @classmethod
      def fetch_all(cls):
          EmployeesRecords = Employees.query.all()
          return EmployeesRecords

      # fetching the data
      @classmethod
      def fetch_all(cls):
          record = Employees.query.all()
          return record

      @classmethod
      def fetch_by_email(cls,email):
          return cls.query.filter_by(email=email).first()

     # Delete
      @classmethod
      def delete_by_id(cls, id):
          record = Employees.query.filter_by(id=id)
          if record.first():
              record.delete()
              db.session.commit()
              return True
          else:
              return False




