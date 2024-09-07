# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from bin_op4 import sha256
from flask import jsonify
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.debug = True
from flask_cors import CORS, cross_origin

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World' 

@app.route('/sha256')
# ‘/’ URL is bound with hello_world() function.
def hello_sha256():
    d = sha256()
    nd = []
    i = 0
    for k in d:

        nd.append({})
        for k1 in k.keys():
            nd[i][str(k1)] = k[k1]
        i += 1

    return jsonify(nd)

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
