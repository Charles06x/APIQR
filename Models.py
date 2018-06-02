from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class estudiantes(db.Model): #Students's model.
	__tablename__ = 'estudiantes'
	
	ID = db.Column('ID', db.Unicode(45), primary_key = True)
	NOMBRES = db.Column('NOMBRES', db.Unicode((45)))
	APELLIDOS = db.Column('APELLIDOS', db.Unicode(45))

class estado_att(db.Model):
	__tablename__ = 'estado_att'

	id = db.Column('id', db.Integer, primary_key = True)
	descripcion = db.Column('descripcion', db.Unicode(45))

class attendees(db.Model):
	__tablename__ = 'attendees'

	id = db.Column('id', db.Integer, primary_key = True)
	idEstudiante = db.Column(db.Unicode(45), db.ForeignKey('estudiantes.ID'))
	nrc = db.Column('nrc', db.Unicode(45))
	created_at = db.Column('created_at', db.Unicode(45))
	updated_at = db.Column('updated_at', db.Unicode(45))
	estado = db.Column(db.Integer, db.ForeignKey(estado_att.id))