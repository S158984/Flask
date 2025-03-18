from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)

@app.route('/')
def hello_world():
    print("This is first flask app  This is test")
    return 'This is first flask app  This is test'


@app.route('/index',methods=['GET'])
def hello_index():
    print('This is index page of flask app')
    return 'This is index page of flask app'

@app.route('/about')
def hello_about():
    print('This is index page of flask app')
    return 'This is index page of flask app'

@app.route('/form',methods=['GET','POST'])
def form_submit():
    if request.method=='POST':
        fname=request.form['fname']
        return 'hello   '+fname
    return render_template('form.html')


##jinja2 template example 1

@app.route('/success/<int:score>')
def score(score):
    #return 'score is ----> '+score
    res=""
    if score>=60:
        res='Passed'
        #return 'you are  ' + res +' and score is '+ str(score)
    else:
        res='Failed'
    return render_template('result.html',result=res,s=score)
    #return 'you are  ' + res +' and score is '+str(score)

##jinja2 template example 2


@app.route('/marks/<int:score>')
def marks(score):
    res=""
    if score>=60:
        res='Passed'
        #return 'you are  ' + res +' and score is '+ str(score)
    else:
        res='Failed'
    
    exp={'s':score,'res':res}
    return render_template('marks.html',result=exp)   


@app.route('/examscore',methods=['GET','POST'])
def examscore():
    total=0
    if request.method=='POST':
        maths=float(request.form['maths'])
        stats=float(request.form['stats'])
        ai=float(request.form['ai'])
        ml=float(request.form['ml'])
        
        total=(maths+stats+ai+ml)/4
    else:
        return render_template('examscore.html')
    return redirect(url_for('score',score=total))
    


if __name__ == '__main__':
    app.run(debug=True)