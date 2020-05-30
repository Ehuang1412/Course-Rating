def qs(s):
	return "\"" + s + "\""

# username,section
import random
for i in range(10,100):
	sid = "username" + str(i)
	sect = ['A', 'B', 'C', 'D'][random.randint(0,3)]
	query = "INSERT INTO enrollment (username, section) VALUES ({},{});".format(qs(sid), qs(sect))
	# print(query)
# INSERT INTO profiles (username, password, role) VALUES ("username4","pwerd4","s");


suggestions = ["No suggestions","Yes", "I want more office hours", "TEACH US SOME","Learn from Haldun", "Just write moreneatly","Continue ignoring me", "I want more office hours", "Cover less topics", "Learn from Haldun", "Just write moreneatly", "I want more office hours", "Yes", "No suggestions", "So continue to be inanttentive", "I think you should be more interactive", "So continue to be inanttentive","Yes", "I want more office hours", "So continue to be inanttentive", "I want more office hours", "More interview question are nice","I have a suggestion", "Please speak louder","Please write legibly", "No comment","I want more office hours"]

reviews = ["This was a great lecture. It was super engaging! Keep it up.", "It could be better","It could be better","THE TEACHER DOES NOT TEACH","10/10 would not take again", "The slow pace is perfect for me to absorb the material he teaches", "I did not understand anything, but I can play", "It was a great lecture","10/10 would not take again","It could be better", "The slow pace is perfect for me to absorb the material he teaches", "I love it", "This was a great lecture. It was super engaging! Keep it up.", "That's the spirit!","I learned a lot", "I think you should be more interactive" ,"I did not understand anything, but I can play"]

dates = ["2018-01-20","2018-01-27","2018-02-03","2018-02-10","2018-02-17","2018-02-24","2018-03-03","2018-03-10","2018-03-17","2018-03-24","2018-03-31","2018-04-07","2018-04-14","2018-04-21","2018-04-28"]

for section in ["A","B","C","D"]:
	ct = 1
	for date in dates:
		lec_id = section + str(ct)
		query = "INSERT INTO lectures (lec_id, date, section) VALUES ({},{},{});".format(qs(lec_id),qs(date),qs(section))
		# print(query)
		ct += 1

