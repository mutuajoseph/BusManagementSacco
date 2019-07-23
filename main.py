from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt
import africastalking
import pygal
# from  vehicleModel import Vehicles


# Connecting our site to database(Postgres)
DB_URL = "postgresql://postgres:Jose.2018@127.0.0.1:5432/busmanagementsacco"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='some-secret-string'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from employeesmodel import Employees
from meetingsModel import Meetings
from contributionsModel import Contributions
from operatorsModel import Operators
from vehicleModel import Vehicles
from userModel import UserModel

@app.before_first_request
def createTables():
    db.create_all()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized! Please log in', 'danger')
            return redirect(url_for('login',next=request.url))
    return wrap



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if email exist
        if UserModel.check_email_exist(email=email):
           # if the email exists check if password is correct
           if UserModel.check_password(email=email,password=password):
               session['logged_in'] = True
               session['username'] = UserModel.fetch_by_email(email).username
               return redirect(request.form['next'] or url_for('dashboard'))
           else:
               flash('Incorrect password','danger')
               return render_template('login.html')
        else:

            flash('Email does not exist','danger')
    return render_template('login.html')


@app.route('/operator/login',methods=['POST','GET'])
def loginOperator():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if email exist
        if Operators.check_email_exist(email=email):
           # if the email exists check if password is correct
           if Operators.check_password(email=email,password=password):
               session['logged_in'] = True
               session['operator'] = Operators.fetch_by_email(email).firstname
               session['mail'] = Operators.fetch_by_email(email).email
               return redirect(request.form['next'] or url_for('operatorPage'))
           else:
               flash('Incorrect password','danger')
               return render_template('operatorlogin.html')
        else:
            flash('Email does not exist','danger')
    return render_template('operatorlogin.html')

@app.route('/manageUsers', methods=['POST','GET'])
@login_required
def manageUsers():

    displayAll = UserModel.fetch_all()
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            role = request.form['role']
            password = request.form['password']

            if UserModel.check_email_exist(email):
                flash('Email exist','danger')
                return redirect(request.url)
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                manageusers = UserModel(username=username,email=email,role=role,password=hashed_password)
                manageusers.createUser()

            flash('Employee successfully added', 'success')

            return redirect(url_for('manageUsers'))
        except Exception as e:
            print(e)
    return  render_template('users.html',allUsers=displayAll)

# admin /secretary routes
@app.route('/')
@login_required
def home():

    vehicle_records = Vehicles.fetch_all()
    records = Employees.fetch_all()
    contribs = Contributions.fetch_all()
    totalcontributions = 0
    for each in contribs:
        totalcontributions += each.amount



    status = [x.role for x in records]
    print(status)
    pie_chart = pygal.Pie()
    pie_chart.title = 'Drivers vs Conductors'
    pie_chart.add('Drivers',status.count('driver'))
    pie_chart.add('Conductors',status.count('conductor'))
    graph = pie_chart.render_data_uri()

    return render_template('index.html',graph=graph,employee_count = len(records),vehicle_count = len(vehicle_records),totalcontributions=totalcontributions)


@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('home'))

@app.route('/employees',methods=['POST','GET'])
@login_required
def employees():
    displayAll = Employees.fetch_all()

    vehicles = Vehicles.fetch_all()
    if request.method == 'POST':
        try:
            email = request.form['email']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            staffId = request.form['staffId']
            role = request.form['role']
            vehicle_id = request.form['vehicleId']

            employee = Employees(email=email, firstName=firstName,lastName=lastName,staff_id=staffId,role=role,vehicleId=vehicle_id)
            employee.create_employees()

            flash('Employee successfully added','success')
            return redirect(url_for('employees'))
        except Exception as e:
            print(e)

    return render_template('employees.html',vehicles=vehicles,allEmployees=displayAll)

@app.route('/operators', methods=['POST','GET'])
@login_required
def operators():

    displayAll = Operators.fetch_all()

    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            firstname = request.form['firstName']
            lastname = request.form['lastName']
            gender = request.form['gender']
            telephoneno = request.form['telephoneNo']

            operator = Operators(firstname=firstname,lastname=lastname,gender=gender,telephoneNo=telephoneno,email=email,password=password)
            operator.create_operators()

            flash('Operator succesfully added','success')
            return redirect(url_for('operators'))
        except Exception as e:
            print(e)

    operators = Operators.fetch_all()
    return render_template('operators.html', operators=operators,allOperators=displayAll)

@app.route('/contributions', methods=['POST','GET'])
@login_required
def contributions():

    displayAll = Contributions.fetch_all()

    if request.method == 'POST':
        try:
            amount = request.form['amount']
            dateTime = request.form['dateTime']
            paymentForm = request.form['paymentForm']
            operator = request.form['operatorId']

            contributions = Contributions(amount=amount,dateTime=dateTime,paymentForm=paymentForm,operator_id=operator)
            contributions.create_contributions()

            flash('Monthly Contributions paid','success')
            return redirect(url_for('contributions'))
        except Exception as e:
            print(e)

    operators = Operators.fetch_all()

    return render_template('contributions.html',operators=operators,allContributions=displayAll)

@app.route('/vehicles',methods=['POST','GET'])
@login_required
def vehicles():
    displayAll = Vehicles.fetch_all()

    if request.method == 'POST':
        try:
            plateno = request.form['plateno']
            seats = request.form['seats']
            route = request.form['route']
            licenseNo = request.form['licenseNo']
            insuranceCompany = request.form['insuranceCompany']
            insuranceExpiryDate = request.form['expirydate']
            operatorId = request.form['operatorId']

            vehicle = Vehicles(plateNo=plateno,seats=seats,route=route,licenseNo=licenseNo,insuranceCompany=insuranceCompany,insuranceExpiryDate=insuranceExpiryDate,operatorId=operatorId)
            vehicle.create_vehicles()

            flash('Vehicle successfully added','success')
            return redirect(url_for('vehicles'))
        except Exception as e:
            print(e)

    operators = Operators.fetch_all()


    return render_template('vehicles.html',operators=operators,allvehicles=displayAll)

@app.route('/meetings',methods=['POST','GET'])
@login_required
def meetings():

    displayAll = Meetings.fetch_all()

    if request.method =='POST':
        try:
            dateTime = request.form['dateTime']
            minutes = request.form['message']

            meeting = Meetings(dateTime=dateTime,minutes=minutes)
            meeting.create_meetings()

            flash('Minute successfully uploaded','success')
            return redirect(url_for(meetings))
        except Exception as e:
            print(e)
    return render_template('meetings.html',allMeetings = displayAll)

@app.route('/message', methods=['POST','GET'])
def sendMessage():
    # Initialize SDK
    username = "Bus"
    api_key = "1d988c1ab828a49631413ae985e9ee72d6533458d18cc3b9570033e398c261b0"
    africastalking.initialize(username, api_key)

    # Initialize a service
    sms = africastalking.SMS

    if request.method == 'POST':
        try:
            phonenumber = request.form['phonenumber']
            fullNumber = "+254" + phonenumber
            message = request.form['message']

            response = sms.send(message, [fullNumber])
            print(response)
            flash('Message successfully sent','success')

        except Exception as e:
            flash('Error! Unable to send message','danger')
            print(e)

    return redirect(url_for('operators'))


@app.route('/notifications',methods=['POST','GET'])
def notification():
    # Initialize SDK
    username = "Bus"
    api_key = "1d988c1ab828a49631413ae985e9ee72d6533458d18cc3b9570033e398c261b0"
    africastalking.initialize(username, api_key)

    # Initialize a service
    sms = africastalking.SMS

    if request.method == 'POST':
        try:
            # fetch all records
            allRecords = Operators.fetch_all()

            # get the phone numbers(number.telephoneNo)
            for number in allRecords:
                # convert to a string
                newNumbers = str(number.telephoneNo)
                # add +254 to each number
                allNumbers = ['+254'+newNumbers]

                # send the message/Notification to all phone numbers
                for x in allNumbers:
                    message = request.form['message']
                    # send the message
                    response = sms.send(message,[x])
                    print(response)

            flash('Message sent successfully','success')

        except Exception as e:
            flash('Error! Unable to send message','danger')
            print(e)

    return redirect(url_for('dashboard'))

# Log Out route
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','Success')

    return redirect(url_for('login'))

# Log Out route
@app.route('/logoutOperator')
def logoutOperator():
    session.clear()
    flash('You are now logged out','success')

    return redirect(url_for('loginOperator'))


@app.route('/meetings/delete/<int:id>', methods=['POST'])
def deleteRecordMeetings(id):
    deleted = Meetings.delete_by_id(id)
    if deleted:
        flash('Deleted Successfully','success')
        return redirect(url_for('meetings'))
    else:
        flash('Record not found')
        return redirect(url_for('meetings'))


@app.route('/operators/delete/<int:id>', methods=['POST'])
def deleteRecord(id):
    deleted = Operators.delete_by_id(id)
    if deleted:
        flash('Deleted Successfully')
        return redirect(url_for('operators'))
    else:
        flash('Record not found')
        return redirect(url_for('operators'))

@app.route('/users/delete/<int:id>', methods=['POST'])
def deleteRecordUsers(id):
    deleted = UserModel.delete_by_id(id)
    if deleted:
        flash('Deleted Successfully')
        return redirect(url_for('manageUsers'))
    else:
        flash('Record not found')
        return redirect(url_for('manageUsers'))

@app.route('/employees/delete/<int:id>', methods=['POST'])
def deleteRecordEmployees(id):
    deleted = Employees.delete_by_id(id)
    if deleted:
        flash('Deleted Successfully')
        return redirect(url_for('employees'))
    else:
        flash('Record not found')
        return redirect(url_for('employees'))

@app.route('/vehicles/delete/<int:id>', methods=['POST'])
def deleteRecordVehicles(id):
    deleted = Vehicles.delete_by_id(id)
    if deleted:
        flash('Deleted Successfully')
        return redirect(url_for('vehicles'))
    else:
        flash('Record not found')
        return redirect(url_for('vehicles'))


@app.route('/operators/edit/<int:id>', methods=['POST','GET'])
def editRecord(id):
    newEmail = request.form['email']
    newPassword = request.form['password']
    newFirstname = request.form['firstName']
    newLastname = request.form['lastName']
    newGender = request.form['gender']
    newTelephoneNo = request.form['telephoneNo']
    update = Operators.update_by_id(id=id,newEmail=newEmail,newPassword=newPassword,newFirstname=newFirstname,newLastname=newLastname,
                                    newGender=newGender,newTelephoneNo=newTelephoneNo)

    if update:
        flash('Update Succesful','success')
        return redirect(url_for('operators'))
    else:
        flash('Record not found')
        return redirect(url_for('operators'))

@app.route('/contributions/edit/<int:id>', methods=['POST','GET'])
def editRecordContributions(id):
    newAmount = request.form['amount']
    newDateTime = request.form['dateTime']
    newPaymentForm = request.form['paymentForm']
    update = Contributions.update_by_id(id=id,newAmount=newAmount,newDateTime=newDateTime,newPaymentForm=newPaymentForm)

    if update:
        flash('Update Succesful','success')
        return redirect(url_for('contributions'))
    else:
        flash('Record not found')
        return redirect(url_for('contributions'))

@app.route('/contributions/delete/<int:id>', methods=['POST'])
def deleteRecordContributions(id):
    deleted = Contributions.delete_by_id(id)
    if deleted:
        flash('Deleted Successfully')
        return redirect(url_for('contributions'))
    else:
        flash('Record not found')
        return redirect(url_for('contributions'))


# operators routes

@app.route('/operator')
def operatorPage():
    try:
        if session:
            if session['operator']:
                operator = Operators.fetch_by_email(session['mail'])

                for each in operator.vehicles:
                     print(each.plateNo)

                totalcontribs = 0
                for each in operator.contributions:
                    totalcontribs += each.amount

                return render_template('operatorsusers.html',operator = operator,totalcontribs=totalcontribs)
            else:
                return redirect(url_for('loginOperator'))
        else:
            return redirect(url_for('loginOperator'))
    except KeyError:
        return redirect(url_for('loginOperator'))











if __name__ == "__main__":
    app.run(debug=True)