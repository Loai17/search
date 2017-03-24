from flask import *
from flask import session as login_session
from model import *
from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='GET':
        owner=None
        if 'id' in login_session:
            owner=session.query(Owner).filter_by(id=login_session['id']).first()
        return render_template('home.html', owner=owner)
    elif request.method=='POST':
        return redirect(url_for('search', s=request.form['s']))

@app.route('/login')
def login():
    if 'id' in login_session:
        flash("You are already logged in")
        return redirect(url_for('owner_profile.html', owner_id=login_session['id']))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "" or password == "":
            flash("Missing Arguements")
            return redirect(url_for('login'))

        owner = session.query(Owner).filter_by(email=email).first()
        if not owner:
            flash("Incorrect password / email combination")
            return redirect(url_for('login'))
        elif verify_password(owner.email, password): 
            flash('Login Successful. Welcome Back, %s' %user.firstname)
            login_session['name'] = owner.name
            login_session['email'] = owner.email
            login_session['id'] = owner.id
            return redirect(url_for('owner_profile.html', owner_id=login_session['id']))


@app.route('/logout', methods = ['POST'])
def logout():
    if 'id' not in login_session:
        flash("You must be logged in order to log out")
        return redirect(url_for('home'))
    del login_session['username']
    del login_session['name']
    del login_session['email']
    del login_session['id']
    flash("Logged out successfully")
    return redirect(url_for('home'))


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        if name == "" or phone == "" or email == "" or dob == "" or  password == "" or confirmpassword == "" :
            flash("Your form is missing arguments")
            return redirect(url_for('signup'))
        if session.query(Owner).filter_by(eamil=eamil). first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('signup')) 
        user = User(name=name, email=email, dob=dob, phone=phone)
        user.hash_password(password)
        session.add(user)
        session.commit()
        flash("User created successfully")
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/search/<string:s>', methods=['GET'])
def search(s):
    search_results=[]
    search_results+=session.query(Business).filter_by(name=str(s)).all()
    search_results+=session.query(Business).filter_by(city=str(s)).all()
    search_results+=session.query(Business).filter_by(address=str(s)).all()
    search_results+=session.query(Business).filter_by(category=str(s)).all()
    for word in str(s).split():
        word=word.capitalize()
        search_results+=session.query(Business).filter_by(name=word).all()
        search_results+=session.query(Business).filter_by(city=word).all()
        search_results+=session.query(Business).filter_by(address=word).all()
        search_results+=session.query(Business).filter_by(category=word).all()
    return render_template('search_results.html',search_results=search_results, search_term=s)

@app.route('/business/<string:business_id>', methods=['GET'])
def business(business_id):
    business=session.query(Business).filter_by(id=business_id).all()
    return render_template('business_profile.html', business=business)

@app.route('/owner', methods=['GET'])
def owner():
    if 'id' not in login_session:
        flash("You must be logged in order to preform this action")
        return redirect(url_for('login'))
    
    business=session.query(Business).filter_by(id=login_session['id']).all()
    return render_template('owner_profile.html', business=business)


if __name__ == '__main__':
    app.run(debug=True)