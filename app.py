import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Contact, Todo       

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

Migrate(app, db)

manager = Manager(app)
manager.add_command("db",MigrateCommand)

# @app.route("/")
# def home():
#     return render_template("index.html")
    
# @app.route("/contacts", methods=['GET', 'POST'])
# @app.route("/contacts/<int:id>", methods=['GET', 'PUT', 'DELETE'])


# def contacts(id=None):
#     if request.method =='GET':
#         if id is not None:
#             contact=Contact.query.get(id)
#             if contact:
#                 return jsonify(contact.serialize()), 200
#             else:
#                 return jsonify({"msg":"Contact not found"}), 404
#         else:
#             contacts = Contact.query.all()
#             contacts = list(map(lambda contact: contact.serialize(), contacts))
#             return jsonify(contacts), 200

#     if request.method =='POST':
#         name = request.json.get('name', None)
#         phone = request.json.get('phone', None)

#         if not name:
#             return jsonify({"msg": "name is required"}), 422
#         if not phone:
#             return jsonify({"msg": "phone is required"}), 422  

#         contact = Contact()
#         contact.name = name
#         contact.phone = phone

#         db.session.add(contact)
#         db.session.commit()

#         return jsonify(contact.serialize()), 201

#     if request.method =='PUT':

#         name = request.json.get('name', None)
#         phone = request.json.get('phone', None)

#         if not name:
#             return jsonify({"msg": "name is required"}), 422
#         if not phone:
#             return jsonify({"msg": "phone is required"}), 422  
             
#         contact = Contact.query.get(id)

#         if not contact:                
#                 return jsonify({"msg":"Contact not found"}), 404

#         contact.name = name
#         contact.phone = phone

#         db.session.commit()

#         return jsonify(contact.serialize()), 200

#     if request.method =='DELETE':
#         contact = Contact.query.get(id)

#         if not contact:                
#                 return jsonify({"msg":"Contact not found"}), 404

#         db.session.delete(contact)
#         db.session.commit()

#         return jsonify({"msg":"Contact deleted"}), 200


@app.route("/todos/user/<username>", methods=['GET', 'POST', 'PUT', 'DELETE'])     

def todo(username): 
    if username is None:
            return jsonify({"msg":"Contact not found"}), 404

    if request.method =='GET':     
        tasks = Todo.query.filter_by(usuario=username)
        tasks = list(map(lambda todo: todo.serialize(), tasks))
        return jsonify(tasks), 200

    if request.method =='POST':
        newUser = Todo()
        label = "My Sample Task"
        done = False

        newUser.usuario = username
        newUser.label = label
        newUser.done = done

        db.session.add(newUser)
        db.session.commit()

        return jsonify(newUser.serialize()), 201

    if request.method =='PUT': 
        
        todo = Todo.query.filter_by(usuario=username).all()        
        for task in todo:    
            db.session.delete(task)
        db.session.commit()

        tasks = request.get_json()       
       
        if not tasks:
            return jsonify({"msg": "New tasks are required"}), 422
                  
        for task in tasks:
            updatedUser = Todo()
            updatedUser.usuario = username
            updatedUser.label = task["label"]
            updatedUser.done = task["done"]
            db.session.add(updatedUser)        
            db.session.commit()

        return jsonify({"result": "A list with "+str(len(tasks))+" todos was succesfully saved"}), 200

    if request.method =='DELETE':
        todo = Todo.query.filter_by(usuario=username).all()        
        for task in todo:    
            db.session.delete(task)
        db.session.commit()

        return jsonify({"msg":"User deleted"}), 200


if __name__=="__main__":
    manager.run()