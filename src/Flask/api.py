from flask import Flask, request, render_template,jsonify
app = Flask(__name__)

@app.route('/api')
def intitial():
    return 'This is the initial page for api flow'
    
    
if __name__=='__main__':
    app.run(debug=True)