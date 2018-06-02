from flask import Flask, send_file, request
from flask_restful import Resource, Api
from flask import render_template
from Models import *
from Config import dataBaseConfigs
from flask_qrcode import QRcode



from flask_qr import QR #In order to make it work properly, we need to modify the flask_qr.py as it doesn't have parentheses when using print. Also, urllib has no attribute named quote_plus, so we need to import urllib.parse and change urllib.quoute_plus to urllib.parse.quote_plus.

#Login
import requests as rq
from requests import session
#


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  dataBaseConfigs.URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)
db.init_app(app)

db.create_all(app=app)

qr = QR(app, mode="google", errorCorrect="H")


class loginSavio(Resource):
	def post(self):
		if request.method == 'POST':
			usr = request.form.get('usr')
			pwd = request.form.get('pwd')

			# Enviando peticion a savio para login
			url = "http://savio.utbvirtual.edu.co/login/index.php"

			payload = "username="+str(usr)+"&password="+str(pwd)

			headers = { 'Content-Type': "application/x-www-form-urlencoded" }

			r = rq.post(url, headers=headers, data=payload)

			if "\u00c1rea personal" in r.text:
				return {"codigo": usr}

#This method generates a QRcode for the given string, recieved as parameter.
class QR(Resource):
	def get(self):
		data = request.args.get('data', '')
		return qr.qrFor(data, dimension=1200)


class getStudent(Resource):
	def get(self, id):
		st = estudiantes.query.get(id)
		st = { 'name': st.NOMBRES,  'id': st.ID, 'apellidos': st.APELLIDOS }
		return st


#Status' methods:

class statusDescription(Resource):
	def get(self):
		lst = []
		stt = status.query.all()
		for i in stt:
			aux = {'id' : i.id, 'description' : i.descripcion}
			lst.append(aux)
		return lst


class getAttendees(Resource):
	def get(self):
		lst = []
		at = attendees.query.all()
		for i in at:
			aux = {'id': i.idattendees, 'nrc': i.attendeesNRC, 'student': i.students_idstudents, 'status': i.status_idstatus}
			lst.append(aux)
		return lst

class  postAttendee(Resource):
	def post(self):
		if request.method=='POST':
			idattendees = request.form.get('id')
			attendeesNRC = request.form.get('nrc')
			students_idstudents = request.form.get('idst')
			status_idstatus = request.form.get('idstt')
			at = attendees(idattendees=idattendees, attendeesNRC=attendeesNRC, students_idstudents=students_idstudents, status_idstatus=status_idstatus)
			db.session.add(at)
			db.session.commit()
			return 'OK'

#Login method
api.add_resource(loginSavio, '/login')
#Add students methods to the api routes
api.add_resource(getStudents, '/students')
api.add_resource(getStudent, '/students/<id>')
api.add_resource(postStudent, '/addStudent')

#Add status records to the api routes
api.add_resource(statusDescription, '/status')


#Add Attendees methods to the api routes
api.add_resource(getAttendees, '/attendees')
api.add_resource(postAttendee, '/pa')

#qrCode
api.add_resource(QR, '/getTheCodeURL') 

if __name__ == '__main__':
	app.run(debug=True) 
