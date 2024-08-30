from flask import Flask
from flask_cors import CORS
import routes.dataplot as dataplot

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})

app.register_blueprint(dataplot.ppd)
@app.route('/', methods=['GET'])
def hello_world():
    return 'railmat project'


if __name__ == '__main__':
    app.run(debug=True)