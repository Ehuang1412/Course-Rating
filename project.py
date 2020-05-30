from flask import Flask, render_template, json, request, session, url_for, redirect, send_file
import pymysql.cursors


def qs(s):
	return "\"" + s + "\""

conn = pymysql.connect(host='localhost',
					   port=8889,
                       user='root',
                       password='root',
                       db='FINAL_PROJECT',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


def average_rating(lec_id):
	query = 'SELECT AVG(star_rating) FROM reviews WHERE lec_id = {}'.format(qs(lec_id))
	cursor = conn.cursor()
	cursor.execute(query)
	returnval = cursor.fetchall()
	return float(returnval[0]['AVG(star_rating)'])

def getdate(lec_id):
	cursor = conn.cursor()
	query = 'SELECT date FROM lectures WHERE lec_id = {}'.format(qs(lec_id))
	cursor.execute(query)
	date = cursor.fetchone()
	m, d, y = date["date"].month, date["date"].day, date["date"].year
	date = "{}-{}-{}".format(m, d, y)
	return date

def lectures_reviewed(username):
	cursor = conn.cursor()
	query = 'SELECT lec_id FROM reviews WHERE username = {}'.format(qs(username))
	cursor.execute(query)
	attended = cursor.fetchall()

	for i, a in enumerate(attended):
		attended[i] = a["lec_id"]#[a["lec_id"],a["date"]]

	query = 'SELECT DISTINCT section FROM enrollment WHERE username = {}'.format(qs(username))
	cursor.execute(query)
	sections = cursor.fetchall()

	for i, s in enumerate(sections):
		sections[i] = s['section']

	unattended = []
	for section in sections:
		query  = 'SELECT lec_id FROM lectures WHERE lec_id LIKE {}'.format(qs(section+'%'))
		cursor.execute(query)
		lecs_unattended = cursor.fetchall()
		for lec in lecs_unattended:
			unattended.append(lec["lec_id"])

	lec_count = len(unattended)

	while len(unattended) + len(attended) > lec_count:
		for i, lec in enumerate(unattended):
			if lec in attended:
				unattended.pop(i)
				break

	return attended, unattended

def insert_review(stars, lec_id, usr, rev, sug):
	ins = 'INSERT INTO reviews(star_rating, lec_id, username, review, suggestion)'
	ins2 = ' VALUES ({},{},{},{},{})'.format(stars,qs(lec_id),qs(usr),qs(rev),qs(sug))
	ins += ins2
	cursor = conn.cursor()
	cursor.execute(ins)
	conn.commit()
	cursor.close()

def lec_dates(lectureslst1, lectureslst2):
	cursor = conn.cursor()
	for i, lecture in enumerate(lectureslst1):
		query = 'SELECT date FROM lectures where lec_id = {}'.format(qs(lecture))
		cursor.execute(query)
		date = cursor.fetchone()
		temp = {}
		temp["lec_id"] = lecture
		temp["date"] = date["date"]
		lectureslst1[i] = temp

	for i, lecture in enumerate(lectureslst2):
		query = 'SELECT date FROM lectures where lec_id = {}'.format(qs(lecture))
		cursor.execute(query)
		date = cursor.fetchone()
		temp = {}
		temp["lec_id"] = lecture
		temp["date"] = date["date"]
		lectureslst2[i] = temp

	return lectureslst1, lectureslst2


def getprofessorclasses(username):
	"""returns list of lists. 1st item section name, next ones are dates"""
	returnval = []
	query = 'SELECT * FROM sections WHERE username = {}'.format(qs(username))
	cursor = conn.cursor()
	cursor.execute(query)
	for item in cursor.fetchall():
		returnval.append(["Section " + item["section"]])
	for item in returnval:
		query = 'SELECT date, lec_id FROM lectures WHERE section = {} ORDER BY date'.format(qs(item[0][-1]))
		print(query)
		cursor.execute(query)
		data = cursor.fetchall()
		for index in range(len(data)):
			m, d, y = data[index]["date"].month, data[index]["date"].day, data[index]["date"].year
			date = "{}-{}-{}".format(m, d, y)
			temp = {}
			temp["date"], temp["lec_id"] = date, data[index]["lec_id"]
			item.append(temp)
		item[1::] = item[1::][::-1]
	return returnval

def student_landing(username):
	reviewed, notreviewed = lectures_reviewed(username)
	reviewed, notreviewed = lec_dates(reviewed, notreviewed)
	bm = ["Welcome to our databases web app!","Click a date on the left to write a","class review or read your old ones.","😃"]
	return render_template('review.html', reviewed=reviewed, notreviewed=notreviewed, dot="", bodymessage=bm)

def professor_landing(username):
	classes = getprofessorclasses(username)
	bm = ["Welcome to our databases web app!","Hover over the side bar to browse reviews",
	"or to add new sections and lectures!","😃"]
	return render_template('professor_main.html', classes=classes, dot="", bodymessage=bm)


@app.route('/home')
def homepage():
	if session.get("username") != False:
		username = session["username"]
		if session.get("role") == "p":
			return professor_landing(username)
		if session.get("role") == "s":
			return student_landing(username)
	return redirect('/')

@app.route('/')
def loginscreen1():
	if session.get("username"):
		query = 'SELECT role FROM profiles WHERE username = {}'.format(qs(session["username"]))
		cursor = conn.cursor()
		cursor.execute(query)
		role = cursor.fetchone()
		if role["role"] == "s":
			return student_landing(session["username"])
		if role["role"] == "p":
			return professor_landing(session["username"])
	else:
		return render_template('login.html')

	return "there was a problem with your request"

@app.route('/login')
def loginscreen():
	return redirect('/')
	# return render_template('login.html')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginauth():
	# lectures_reviewed("username28")
	username = request.form['username']
	password = request.form['password']

	query = 'SELECT * FROM profiles WHERE username = {} and password = {}'.format(qs(username),qs(password))
	cursor = conn.cursor()
	cursor.execute(query)
	data = cursor.fetchall()

	if len(data) == 0:
		return render_template('tryagain1.html')

	if data[0]["role"] == "s":
		session["username"] = username
		session["role"] = "s"
		return student_landing(username)#render_template('review.html')

	if data[0]["role"] == "p":
		session["username"] = username
		session["role"] = "p"
		return professor_landing(username)

	return "THERE WAS A PROBLEM PROCESSING YOUR REQUEST"

@app.route('/reviewfor/lec_id=<id>', methods=['GET','POST'])
def student_lecture_review(id):
	if session.get("username") == False: return render_template('login.html')
	username = session["username"]
	if session["role"] == "p":
		return "Sorry! This page is off limits to professors"

	cursor = conn.cursor()
	query = 'SELECT star_rating, review, suggestion FROM reviews WHERE username = {} AND lec_id = {}'.format(qs(username), qs(id))
	cursor.execute(query)
	lecture_info = cursor.fetchall()
	reviewed, notreviewed = lectures_reviewed(username)
	reviewed, notreviewed = lec_dates(reviewed, notreviewed)
	if len(lecture_info) == 0:
		rf = True
		linf = {}
	else:
		rf = False
		linf = lecture_info[0]
	date = getdate(id)
	return render_template('review.html', reviewed=reviewed, 
		notreviewed=notreviewed, reviewform=rf, topbar=True,
		bodymessage="", review=linf, dot=".", date=date, lec_id=id)

@app.route('/add_section')
def addsect():
	if session.get("username") == False: return render_template('login.html')
	if session["role"] == "s":
		return "Sorry! This page is off limits to students."
	classes = getprofessorclasses(session["username"])
	return render_template('add_sec.html', classes=classes)

@app.route('/add_sect', methods=['POST'])
def add_sect_to_db():
	if session["role"] == "s":
		return "Sorry! This page is off limits to students."
	bm = ["The section has been added!","😃"]
	cursor = conn.cursor()
	ins = 'INSERT INTO sections(section, username) VALUES ({}, {})'.format(qs(request.form['newsec']), qs(session['username']))
	cursor.execute(ins)
	conn.commit()
	cursor.close()
	classes = getprofessorclasses(session["username"])
	return render_template('professor_main.html', classes=classes, dot="", bodymessage=bm)

@app.route('/add_lecture')
def addlect():
	if session.get("username") == False: return render_template('login.html')
	if session["role"] == "s":
		return "Sorry! This page is off limits to students."
	classes = getprofessorclasses(session["username"])
	return render_template('add_lec.html', classes=classes)


@app.route('/add_lect', methods=['POST'])
def add_lect_to_db():
	if session["role"] == "s":
		return "Sorry! This page is off limits to students."
	bm = ["The lecture has been added to the database!","😃"]
	# cursor = conn.cursor()
	# ins = 'INSERT INTO sections(section, username) VALUES ({}, {})'.format(qs(request.form['newsec']), qs(session['username']))
	# cursor.execute(ins)
	# conn.commit()
	# cursor.close()
	classes = getprofessorclasses(session["username"])
	return render_template('professor_main.html', classes=classes, dot="", bodymessage=bm)


@app.route('/prof_reviews/lec_id=<id>', methods=['GET','POST'])
def professor_lecture_reviews(id):
	if session.get("username") == False: return render_template('login.html')
	username = session["username"]
	if session["role"] == "s":
		return "Sorry! This page is off limits to students."
	cursor = conn.cursor()
	query = 'SELECT star_rating, review, suggestion FROM reviews WHERE lec_id = {}'.format(qs(id))
	cursor.execute(query)
	reviews = cursor.fetchall()
	if len(reviews) > 0:
		re = True
	else:
		re = False
	classes = getprofessorclasses(username)
	rc = len(reviews)
	avg = average_rating(id)
	date = getdate(id)
	return render_template('professor_main.html', classes=classes, reviewsexist=re,
				 reviews=reviews, review_count=rc,avg_review=avg,date=date, dot=".", topbar=True)

@app.route('/postreview/lec_id=<id>', methods=['POST'])
def postreview(id):
	if session.get("username") == False: return render_template('login.html')
	username = session["username"]
	rating = int(request.form["group1"])
	explain = request.form["explain"]
	suggestion = request.form["suggestions"]
	insert_review(rating, id, session["username"], explain, suggestion)
	reviewed, notreviewed = lectures_reviewed(username)
	reviewed, notreviewed = lec_dates(reviewed, notreviewed)

	bm = ["Thank you for the review!","Every suggestion helps.", "🙏"]
	return render_template('review.html', reviewed=reviewed, 
		notreviewed=notreviewed, reviewform=False, topbar=False,
		bodymessage=bm, dot=".")
	return("Thank you for the review! {}".format(session["username"]))

@app.route('/icon.png')
def img():
	return send_file('/Users/doronrasis/Desktop/Introduction\ to\ Databases/db\ final\ project/static/icon.png', as_attachment=True)

@app.route('/prof_main')
def profmain():
	classes = getprofessorclasses()
	return render_template('professor_main.html', classes=classes, review_count=20,avg_review=3.8,date="4/20/2018")

@app.route('/signout', methods=["POST"])
def logoff():
	session.pop('username')
	session.pop('role')
	return redirect('/')

app.secret_key = "secret"

if __name__ == "__main__":
	app.run(debug = True)