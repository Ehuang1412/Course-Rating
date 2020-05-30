query = 'SELECT star_rating FROM class_review Where studentid = %s and lecid = %s'
#Returns star_rating

query = 'SELECT review FROM class_review Where studentid = %s and lecid = %s' 
#Returns review

query = 'SELECT COUNT(*) FROM enrollment WHERE courseid = %s ' 
#Returns how many students are taking a specific course

query = 'SELECT * FROM logins WHERE username = %s and password = %s' 
#Returns username and password to see if it is valid

query = 'SELECT star_rating FROM class_review Where studentid = %s and lecid = %s'
#Returns star_rating

query = 'SELECT review FROM class_review Where studentid = %s and lecid = %s' 
#Returns review

query = 'SELECT COUNT(*) FROM enrollment WHERE courseid = %s ' 
#Returns how many students are taking a specific course

query = 'SELECT COUNT(*) FROM class_review WHERE lecid = %s' 
#Returns the count of reviews of each class

query = 'SELECT AVG(star_rating), lecid FROM class_review GROUP BY lecid' 
#Returns the average review for each class

query = 'SELECT courseid FROM lecture WHERE lecid = (SELECT lecid FROM class_review WHERE studentid = %s)' 
#Returns which classes a student has reviewed

query = 'SELECT courseid FROM lecture WHERE lecid NOT IN(SELECT lecid FROM class_review WHERE studentid = %s)' 
#Returns which classes a student has not reviewed

query = 'SELECT fname,lname FROM student WHERE studentid IN(SELECT studentid FROM enrollment WHERE courseid = %s)'
#Returns full name of students taking a specific course

query = 'SELECT fname,lname FROM professor WHERE professorid IN(SELECT professorid FROM course WHERE courseid = %s)'
#Returns full name of professor teaching a specific course

ins = 'INSERT INTO class_review (review, star_rating, studentid, lecid) VALUES (%s, %s, %s, %s)' 
#inserts reviews

ins = 'INSERT INTO logins (username, passwords, professorid, studentid) VALUES (%s, %s, %s, %s)' 
#inserts users username and password

ins = 'INSERT INTO course (courseid, timeslot, professorid, coursesection) VALUES (%s, %s, %s, %s)' 
#inserts new class for professor

ins = 'INSERT INTO lecture (lecid, date, courseid, course_section) VALUES (%s, %s, %s, %s)' 
#inserts new lecture

ins = 'INSERT INTO student (fname, lname, studentid) VALUES (%s, %s, %s)' 
#inserts new student

ins = 'INSERT INTO professor (fname, lname, professorid) VALUES (%s, %s, %s)' 
#inserts new professor

