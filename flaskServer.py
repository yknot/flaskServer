# import flask
from flask import Flask, render_template


# create app
app = Flask(__name__)

# route decorator
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return render_template('api.html')


# run the app
if __name__ == '__main__':
    # reload on change of file
    app.debug = True
    app.run()
