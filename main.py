from dotenv import load_dotenv
import os

from flask import Flask, redirect, session, render_template, request, jsonify, url_for
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy

# Flask App Setup
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# Auth0 Config
app.config['AUTH0_CLIENT_ID']     = os.getenv('AUTH0_CLIENT_ID')
app.config['AUTH0_CLIENT_SECRET'] = os.getenv('AUTH0_CLIENT_SECRET')
app.config['AUTH0_DOMAIN']        = os.getenv('AUTH0_DOMAIN')
app.config['AUTH0_CALLBACK_URL']  = os.getenv('AUTH0_CALLBACK_URL')

oauth = OAuth(app)
oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    server_metadata_url=f"https://{app.config['AUTH0_DOMAIN']}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'}
)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    email   = db.Column(db.String, primary_key=True)
    rate    = db.Column(db.Float, default=0.0)
    devices = db.relationship('Device', backref='owner', cascade='all, delete-orphan')

class Device(db.Model):
    __tablename__  = 'devices'
    id             = db.Column(db.Integer, primary_key=True)
    user_email     = db.Column(db.String, db.ForeignKey('users.email'))
    name           = db.Column(db.String, nullable=False)
    watts          = db.Column(db.Float, nullable=False)
    hours          = db.Column(db.Float, nullable=False)
    category       = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=app.config['AUTH0_CALLBACK_URL'],
        scope='openid profile email',
        prompt='login'
    )

@app.route('/callback')
def callback():
    token   = oauth.auth0.authorize_access_token()
    profile = token.get('userinfo') or token
    session['user'] = profile

    usr = User.query.get(profile['email'])
    if not usr:
        usr = User(email=profile['email'])
        db.session.add(usr)
        db.session.commit()

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/api/rate', methods=['GET', 'PUT'])
def api_rate():
    if 'user' not in session:
        return jsonify({}), 401
    usr = User.query.get(session['user']['email'])
    if request.method == 'GET':
        return jsonify({'rate': usr.rate})
    data = request.get_json()
    usr.rate = float(data.get('rate', usr.rate))
    db.session.commit()
    return jsonify({'rate': usr.rate})

@app.route('/api/devices', methods=['GET', 'POST'])
def api_devices():
    if 'user' not in session:
        return jsonify({}), 401
    usr = User.query.get(session['user']['email'])
    if request.method == 'GET':
        return jsonify([{
            'id': d.id,
            'name': d.name,
            'watts': d.watts,
            'hours': d.hours,
            'category': d.category
        } for d in usr.devices])
    data = request.get_json()
    d = Device(owner=usr,
               name=data['name'],
               watts=float(data['watts']),
               hours=float(data['hours']),
               category=data['category'])
    db.session.add(d)
    db.session.commit()
    return jsonify({'id': d.id})

@app.route('/api/devices/<int:did>', methods=['PUT', 'DELETE'])
def api_device_update(did):
    if 'user' not in session:
        return jsonify({}), 401
    d = Device.query.get_or_404(did)
    if d.user_email != session['user']['email']:
        return jsonify({}), 403

    if request.method == 'DELETE':
        db.session.delete(d)
        db.session.commit()
        return '', 204

    data = request.get_json()
    d.name     = data.get('name', d.name)
    d.watts    = float(data.get('watts', d.watts))
    d.hours    = float(data.get('hours', d.hours))
    d.category = data.get('category', d.category)
    db.session.commit()
    return jsonify({})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
