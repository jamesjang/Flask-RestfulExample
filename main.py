from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import random, string

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'userdb.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(240), unique = True)
    level = db.Column(db.String(10), unique = False)
    device_id = db.Column(db.String(240), unique = True)
    transfer_code = db.Column(db.String(240), unique = True)

    def __init__(self, player_name, level, device_id, transfer_code):
        self.player_name = player_name
        self.level = level
        self.device_id = device_id
        self.transfer_code = transfer_code


class UserSchema(ma.Schema):
    class Meta:
        fields = ('player_name', 'level', 'device_id', 'transfer_code')

user_schema = UserSchema()
users_schema = UserSchema(many=True)



@app.route('/user/create', methods =["PUT"])
def create_user():
    player_name = request.json['player_name']
    level = request.json['level']
    device_id = request.json['device_id']
    transfer_code = request.json['transfer_code']

    transfer_code ="".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

    new_user = Users(player_name, level, device_id, transfer_code)

    db.session.add(new_user)
    db.session.commit()

    return 'created new user'

@app.route('/user/getall', methods =["GET"])
def get_all_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route('/user/<device_id>', methods =["GET"])
def get_user_by_deviceid (device_id):
    user = Users.query.filter_by(device_id=device_id).first()
    return user_schema.jsonify(user)

@app.route('/user/transfer/<transfer_code>', methods =["GET"])
def transfer_user (transfer_code):
    user = Users.query.filter_by(transfer_code=transfer_code).first()
    return user_schema.jsonify(user)

if __name__ =='__main__':
    app.debug = True
    app.run()
