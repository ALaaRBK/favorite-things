from flask import render_template,Flask,url_for,redirect
from forms import RegistrationForm,LoginForm

app=Flask(__name__)

app.config['SECRET_KEY']= 'c1a76c58367bdeaf12f088c272d0daf7'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
@app.route('/')
def home():
    return render_template('index.html',title='Favorite Things')

@app.route('/about')
def about():
    return render_template('about.html',title='about')


@app.route('/register',methods=['POST','GET'])
def register():
    form=RegistrationForm()
    return render_template('register.html',title='Register',form=form)
    

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
