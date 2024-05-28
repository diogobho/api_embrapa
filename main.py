from flask import Flask,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
import os
from flask_cors import CORS


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_pyfile('config.py')
    
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors= CORS(app)

@app.route('/swagger')
def swagger_ui():
    return render_template('swaggerui.html')

@app.route('/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('static', 'openapi.yaml')


from views.scraping import *
from views.autenticacao import *
  
if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.run(host=host, port=port, debug=True)