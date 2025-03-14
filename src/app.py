from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def hello_world():
    print("This is first flask app  This is test")
    return 'This is first flask app  This is test'


@app.route('/index')
def hello_index():
    print('This is index page of flask app')
    return 'This is index page of flask app'



if __name__ == '__main__':
    app.run(debug=True)