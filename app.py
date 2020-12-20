from flask import Flask, render_template
from mvc.view import simple_page

app = Flask(__name__)
app.secret_key = 'no secret' # necessary to access session necessary to access flash scope
app.register_blueprint(simple_page)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
