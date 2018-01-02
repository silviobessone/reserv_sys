from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Cioccolocanda!"


@app.route('/template')
def template_test():
    data = {
            "my_string": "Chocolate!",
            "my_list": [7, 4, 8, 6, 1, 5, 3, 0, 2, 9]
           }
    return render_template('template.html', **data)


if '__name__' == '__main__':
    app.run(debug=True)
