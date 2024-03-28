from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='system',db='flaskblog')
with mysql.connector.connect(host='localhost',user='root',password='system',db='flaskblog'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(50) primary key,mobile varchar(20) unique,email varchar(50) unique,address varchar(50),password varchar(20))")
    cursor.execute("create table if not exists posts(id INT NOT NULL AUTO_INCREMENT,title VARCHAR(255) DEFAULT NULL,content TEXT,date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,slug VARCHAR(255) DEFAULT NULL,poster_id VARCHAR(50) DEFAULT NULL,PRIMARY KEY (id),KEY poster_id (poster_id),CONSTRAINT fk_poster_id FOREIGN KEY(poster_id) REFERENCES registration(username))")
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route('/')
def home():
    return render_template('homepage.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        print(username)
        print(mobile)
        print(address)
        print(email)
        print(password)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insret into registration values(%s,%s,%s,%s,%s)',[username,mobile,address,email,password])
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('registration.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password'] 
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]   
        print(data)
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('homepage'))
        else:
            return "Invalid Username and Password"
    return render_template('login.html')
@app.route('/logout') 
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))      
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/addpost',methods=['GET','POST'])
def addpost():
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts(title,content,slug) VALUES (%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM POSTS WHERE id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewpost'))
@app.route('/updatepost/<int:id>',methods=['GET','POST'])
def updatepost(id):
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        cursor=mydb.cursor(buffered=True)
        cursor.execute('UPDATE posts SET title=%s,content=%s,slug=%s WHERE id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
    else:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone()
        return render_template('updatepost.html',post=post)
app.run()
