from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__="contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return "<Contact %r>" % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }

class Todo(db.Model):
    __tablename__="todos"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50),nullable=False)
    done = db.Column(db.Boolean,nullable=False)     

    def __repr__(self):
        return "<Todo %r>" % self.label
    
    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "label": self.label,
            "done": self.done             
        }