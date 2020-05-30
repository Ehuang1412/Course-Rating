import random
import pymysql.cursors

conn = pymysql.connect(host='localhost',
					   port=8889,
                       user='root',
                       password='root',
                       db='FINAL_PROJECT',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

cursor = conn.cursor()

def qs(s):
	return "\"" + s + "\""

query = "SELECT * FROM enrollment"

cursor.execute(query)

# 
students = cursor.fetchall()

# print(result)

# star_rating, lec_id, username, review, suggestion


lectureopt1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lectureopt2 = [7, 8, 9, 10, 11, 12, 13, 14, 15]
lectureopt3 = [2, 4, 6, 8, 10, 12, 14]
lectureopt4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
lectureopt5 = [2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15]
lectureoptions = [lectureopt1, lectureopt2, lectureopt3, lectureopt4, lectureopt5]


for student in students:
	lecsattended = lectureoptions[random.randint(0,4)]
	section = student["section"]
	un = student["username"]
	for lec in lecsattended:
		sr = random.randint(1,5)
		rv = reviews[random.randint(0, len(reviews)-1)]
		sg = suggestions[random.randint(0, len(suggestions)-1)]
		lec_id = section + str(lec)
		query = 'INSERT INTO reviews (star_rating, lec_id, username, review, suggestion) VALUES ({}, {}, {}, {}, {});'.format(sr, qs(lec_id), qs(un), qs(rv), qs(sg))
		print(query)
