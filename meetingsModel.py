from main import db


class Meetings(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.String(30), nullable=True)
    minutes = db.Column(db.String(), nullable=True)

    # create
    def create_meetings(self):
        db.session.add(self)
        db.session.commit()

    # Method for reading data
    @classmethod
    def fetch_all(cls):
        MeetingRecords = Meetings.query.all()
        return MeetingRecords

    # Delete
    @classmethod
    def delete_by_id(cls, id):
        record = Meetings.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False




class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(45), nullable=True)
    message = db.Column(db.String(500), nullable=True)

    # create
    def create_meetings(self):
        db.session.add(self)
        db.session.commit()

    # Method for reading data
    @classmethod
    def fetch_all(cls):
        MeetingRecords = cls.query.all()
        return MeetingRecords

