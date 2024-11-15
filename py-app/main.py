import mysql.connector

con = mysql.connector.connect(		host='localhost',user='root',password='ahmedfarid',	database='store')
cursor=con.cursor()
useremail="ahmed.farid.592002@gmail.com"
upc=None
password="Ahmed@010"
current=None
offset=1
prod=None

def credentialsPrompt():
	email=input("welcome\nPlease enter your email:	enter 0 to cancel   ")
	if email =="0":
		index()
		return
	pw=input("Enter your password:")
	sql="select * from user where email= %s and password = %s ;"
	cursor.execute(sql,(useremail,password))
	global current
	current=cursor.fetchone()
	if current:
		print("Authentication successful")
		home()
	else:
		print("Authentication failed\n try entering correct email and password")
		credentialsPrompt()

def register():
	fn=input("enter your first name")
	ln=input("enter your last name")
	email=	input("Enter your email")
	pw=input("enter your password ")
	dob=input("enter your date of birth in the format yyyy-mm-dd:")
	city=input("your city")
	country=input("your country")
	sql="insert into user(first_name,last_name,email,password,dob,city,country) values ( %s,%s , %s ,%s , %s , %s , %s );"
	try:
		cursor.execute(sql,(fn,ln,email,pw,dob,city,country))
		con.commit()
		print("you have registered successfully")
		index()
	except mysql.connector.errors.DataError as er: 
		print(er)
		register()

def index():
	i=input("""l| Log in
	r| register
		 x|  exit
		""")
	if i=="l":
		credentialsPrompt()
	elif i=="r":
		register()
	elif i=="x":
		print("exiting")
		return
	else:
		index()

def view():
	global offset
	cursor.execute("select upc , name    from product limit 10 offset %s ;",tuple([offset]))
	results=cursor.fetchall()
	for i, t in enumerate(results):
		print(i,t[1])
	i=input("enter n to get the next punsh of results p to get the previous or enter from 0 to 9 to show the corsponding product\n b| go back")
	if i=="n":
		if offset <990:
			offset+=10
			view()
		else:
			print("no more to show")
			view()
	elif  i== "p":
		if offset > 10:
			offset-=10
			view()
		else:
			print("that is the begining")
			view()
	elif i=="b":
		home()
	elif int(i) in range(0,10):
		cursor.execute("select * from product where upc = %s",tuple([results[int(i)][0]]))
		global prod
		prod=cursor.fetchone()
		viewProduct()

def viewProduct():
	print(f"""upc \t{prod[0]}
name \t {prod[1]}
type \t {prod[2]}
category \t {prod[3]}
description \t {prod[4]}
stock \t {prod[5]}
price \t { prod[6]}
tax \t { prod[7]}""")
	i=input("r|  reviews \n w| write a review \n f |mark favourite \n b| back")
	if i=="b":
		view()
	elif i=="r":
		productReviews()
	elif i=="w":
		addReview()
	elif i=="f":
		markFavourite()
	else:
		viewProduct()

def home():
	i=input("v| view products\n f| to view favourites \n r| my reviews \n x| exit")
	if i=="v":
		view()
	elif i== "f" :
		myFavourites()
	elif i=="r":
		myReviews()
	elif i=="x":
		print("exiting")
		return
	else:
		home()

def productReviews():
	cursor.execute("SELECT user.first_name, user.last_name, reviews.review, reviews.rating FROM reviews INNER JOIN user ON reviews.email = user.email WHERE reviews.upc = %s;",tuple([prod[0]]))
	reviews=cursor.fetchall()
	print("reviews of ",prod[1])
	for review in reviews:
		print(review[0],review[1])
		print('rating',review[3])
		print(review[2])
	i=input("a| add review \n b| go back")
	if i=="b":
		viewProduct()
	elif i=="a":
		addReview()
	else:
		productReviews()

def addReview():
	i=input("Enter your review")
	if i =="":
		addReview()
		return
	else:
		r=i
	i = input("Enter your rating from 0 to 5")
	if not  isinstance(int(i),int) :
		print("invalid input \n please input a valid number from 0 to 5 inclusive ")
		addReview()
		return
	else:
		t=i
	try:
		cursor.execute("insert into reviews(email,upc,review,rating) values ( %s , %s , %s , %s );",tuple([current[2],prod[0],r,t]))
		con.commit()
		print("review added")
	except mysql.connector.errors.IntegrityError as er: 
		print(er)
	viewProduct()

def markFavourite():
	try:
		cursor.execute("insert into favourites(email,upc) values ( %s , %s );",tuple([current[2],prod[0]]))
		con.commit()
		print("Product added to favourites")
	except mysql.connector.errors.IntegrityError as er:
		print("Product already added")
	viewProduct()

def myFavourites():
	global prod
	print(f"favourites of {current[0]} {current[1]}")
	cursor.execute("select f.upc , p.name from favourites f inner join product p on f.upc=p.upc where f.email = %s ;",tuple([current[2]]))
	results=cursor.fetchall()
	for i,r in enumerate(results):
		print(i,r[1])
	i=input("b| go back")
	if i=="b":
		home()
	elif int(i) in range(len(results)):
		cursor.execute("select * from product where upc = %s",tuple([results[int(i)][0]]))
		prod=cursor.fetchone()
		viewProduct()

def myReviews():
	print(f"reviews of {current[0]} {current[1]}")
	cursor.execute("select r.upc, r.review, p.name , r.rating from reviews r inner join product p on r.upc=p.upc where r.email = %s ;",tuple([current[2]]))
	results=cursor.fetchall()
	for r in results:
		print(r[2])
		print(r[1])
		print(r[3])
	i=input("b| go back")
	if i=="b":
		home()

index()
