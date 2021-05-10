from datetime import date
from flask import Flask, redirect, request, url_for, render_template, flash, session
import sqlite3
from bs4 import BeautifulSoup
import requests
import sys

app = Flask(__name__)       # our Flask app
app.secret_key="supersecretkey"
DB_FILE = 'mydb.db'    		# file for our Database


@app.route("/index")
def Index():
    page = requests.get("https://www.bbc.co.uk/weather/0/292223") #to extract seven-day forecast
    soup = BeautifulSoup(page.content, 'html.parser')
    date = soup.findAll("div", class_="wr-day__title wr-js-day-content-title", limit=7)
    temp = soup.select(".wr-day-temperature__high-value .wr-value--temperature--c")

    temparray = []
    dailyarray = []
    for t in temp : #to print each date/day
        temparray.append(str(t.get_text()))

    for day in date: #to print each date/day
        dailyarray.append(str(day.get("aria-label")))

    dailytemp = list(zip(dailyarray, temparray)) #function used to store both arrays
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM weather")
    rv = cursor.fetchall()
    connection.commit()
    cursor.close()

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM weather")
    rv = cursor.fetchall()
    connection.commit()
    cursor.close()

    for item in dailytemp:
        add_cast(item[0], item[1])
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM weather")
    rv = cursor.fetchall()
    connection.commit()
    cursor.close()    
    return render_template("index.html", entries=rv)
#function that will store weather data on SQL
def add_cast(day, temprature):
	"""
	put a new entry in the database
	"""
	params = {'day':day, 'temprature':temprature}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into weather VALUES (:day, :temprature)",params)
	connection.commit()
	cursor.close()
	
@app.route("/home")
def Home():
    return render_template("home.html")

@app.route("/about")
def About():
    return render_template("about.html")
	
@app.route("/pl", methods=['POST', 'GET'])
def Pl():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usrComments")
    rv = cursor.fetchall()
    cursor.close()

    page = requests.get ('https://www.skysports.com/premier-league-table') #To extract the Premier League table
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find('tbody')
    row = matches.findAll('td',class_="standing-table__row")

    rankarray = []
    teamarray = []
    pointsarray = []
    #The extracted data is stored in an array
    rank = soup.select (".standing-table__row > .standing-table__cell:nth-of-type(1)")
    for i in rank:
        rankarray.append(i.get_text(strip=True))#The .append() stores the scraped data in an array
        
    team = soup.select (".standing-table__row > .standing-table__cell:nth-of-type(2)")
    for i in team:
        teamarray.append(i.get_text(strip=True))

    points = soup.select (".standing-table__row :nth-of-type(10)")
    for i in points:
        pointsarray.append(i.get_text(strip=True))

    Table = list(zip(rankarray, teamarray, pointsarray))
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM plTable")
    rv3 = cursor.fetchall()
    connection.commit()
    cursor.close()

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM plTable")
    rv3 = cursor.fetchall()
    connection.commit()
    cursor.close()

    for item in Table:
        add_cast3(item[0], item[1], item[2])
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM plTable")
    rv3 = cursor.fetchall()
    connection.commit()
    cursor.close()

    return render_template("pl.html",entries=rv, entries3=rv3)
# function made to insert the elements into SQL table
def add_cast3(Rank, Team, Points):
	"""
	put a new entry in the database
	"""
	params = {'Rank':Rank, 'Team':Team, 'Points':Points}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into plTable VALUES (:Rank, :Team, :Points)",params)
	connection.commit()
	cursor.close()


@app.route('/post_comment_pl', methods=['POST', 'GET'])
def post_comment_pl():
	"""
	Accepts POST requests, and processes the form;
	Redirect to PL page when completed.
	"""
	insert_comment(request.form['Username'], request.form['Comment'])
	
	return redirect(url_for('Pl'))

def insert_comment(Username, Comment):
	"""
	put a new entry in the database
	"""
	params = {'Username':Username, 'Comment':Comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into usrComments VALUES (:Username, :Comment)",params)
	connection.commit()
	cursor.close()   
	
@app.route("/bun", methods=['POST', 'GET'])
def Bun():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usrCommentsbun")
    rv = cursor.fetchall()
    cursor.close()
    #This is to scrape the top scorers in the bundesliga
    page = requests.get ('https://www.worldfootball.net/goalgetter/bundesliga-2019-2020/')
    soup = BeautifulSoup(page.content, 'html.parser')

    headerar = []
    rankar = []
    playerar = []
    teamar = []
    countryar = []
    goalsar = []

    header = soup.select ("tr > th:nth-of-type(1)")
    for i in header:
        headerar.append(i.get_text(strip=True))
    header1 = soup.select ("tr > th:nth-of-type(2)")
    for i in header1:
        headerar.append(i.get_text(strip=True))
    header3 = soup.select ("tr > th:nth-of-type(3)")
    for i in header3:
        headerar.append(i.get_text(strip=True))
    header4 = soup.select ("tr > th:nth-of-type(4)")
    for i in header4:
        headerar.append(i.get_text(strip=True))
        
    header5 = soup.select ("tr > th:nth-of-type(5)")
    for i in header5:
        headerar.append(i.get_text(strip=True)) 
    rank = soup.select ("tr > td:nth-of-type(1)",limit=10)
    for i in rank:
        rankar.append(i.get_text(strip=True))
        
    player = soup.select ("td > a:nth-of-type(1)",limit=20)
    for i in player:
        if (i.get_text(strip=True) != ""):
            playerar.append(i.get_text(strip=True))

    team = soup.select (".hell :nth-of-type(2)",limit=10)
    for i in team:
        teamar.append(i.get_text(strip=True))

    country = soup.select ("td > img",limit=10)
    for i in country:
        countryar.append(i.get("title"))   

    goals = soup.select ("tr > td:nth-of-type(6)" ,limit=10)
    for i in goals:
        goalsar.append(i.get_text(strip=True))
   
    Scorers = list(zip(headerar, rankar, playerar, teamar, countryar, goalsar))
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bundScorers")
    rv2 = cursor.fetchall()
    connection.commit()
    cursor.close()

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM bundScorers")
    rv2 = cursor.fetchall()
    connection.commit()
    cursor.close()

    for item in Scorers:
        add_cast2(item[0], item[1], item[2], item[3], item[4], item[5])
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bundScorers")
    rv2 = cursor.fetchall()
    connection.commit()
    cursor.close()    

    return render_template("bun.html",entries=rv, entries2=rv2)
#Function made to store the data in an SQL table
def add_cast2(Header, Rank, Name, Team, Country, Goals):
        """
        put a new entry in the database
        """
        params = {'Header':Header, 'Rank':Rank, 'Name':Name, 'Country':Country, 'Team':Team , 'Goals':Goals}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()  
        cursor.execute("insert into bundScorers VALUES (:Header, :Rank, :Name, :Country, :Team, :Goals)",params)
        connection.commit()
        cursor.close()

@app.route('/post_comment_bun', methods=['POST', 'GET'])
def post_comment_bun():
	"""
	Accepts POST requests, and processes the form;
	Redirect to Bundesliga page when completed.
	"""
	insert_comment_bun(request.form['Username'], request.form['Comment'])
	
	return redirect(url_for('Bun'))

def insert_comment_bun(Username, Comment):
	"""
	put a new entry in the database
	"""
	params = {'Username':Username, 'Comment':Comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into usrCommentsbun VALUES (:Username, :Comment)",params)
	connection.commit()
	cursor.close()
	
@app.route("/ered", methods=['POST', 'GET'])
def Ered():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usrCommentsered")
    rv = cursor.fetchall()
    cursor.close()
    eredObject = Eredivise.eredDesc() #To access the function inside the class
    desc = eredObject

    return render_template("ered.html",entries=rv, desc=desc)
#Made a class, that includes the function that will scrape the description of the Dutch League
class Eredivise():
    def eredDesc():
            try:
                    page = requests.get("https://www.definitions.net/definition/eredivisie")
                    soup = BeautifulSoup(page.content, 'html.parser')
                    first = soup.find('p', class_="desc")
                    desc = first.get_text()
                    return desc
            except:
                    return render_template("error.html", msg=sys.ecx_info())
        
@app.route('/post_comment_eredi', methods=['POST', 'GET'])
def post_comment_eredi():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	insert_comment_ered(request.form['Username'], request.form['Comment'])
	
	return redirect(url_for('Ered'))

def insert_comment_ered(Username, Comment):
	"""
	put a new entry in the database
	"""
	params = {'Username':Username, 'Comment':Comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into usrCommentsered VALUES (:Username, :Comment)",params)
	connection.commit()
	cursor.close()
	
@app.route("/laliga", methods=['POST', 'GET'])
def Laliga():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usrCommentsliga")
    rv = cursor.fetchall()
    cursor.close()
    ligaObject = ligaDesc.laliga_desc() #this is to access a function inside a class
    desc = ligaObject
    
    return render_template("laliga.html",entries=rv, desc=desc)
#the function is stored in a class
class ligaDesc():
    def laliga_desc(): #function that scrapes the description about LaLiga
        page = requests.get("https://www.quora.com/What-is-La-Liga-soccer")
        soup = BeautifulSoup(page.content, 'html.parser')

        first = soup.find('div', class_="ui_qtext_expanded").p
        desc = first.get_text()
        return desc
    
@app.route('/post_comment_liga', methods=['POST', 'GET'])
def post_comment_liga():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	insert_comment_liga(request.form['Username'], request.form['Comment'])
	
	return redirect(url_for('Laliga'))

def insert_comment_liga(Username, Comment):
	"""
	put a new entry in the database
	"""
	params = {'Username':Username, 'Comment':Comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into usrCommentsliga VALUES (:Username, :Comment)",params)
	connection.commit()
	cursor.close()
	
@app.route("/serie", methods=['POST', 'GET'])
def Serie():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usrCommentsser")
    rv = cursor.fetchall()
    cursor.close()
    #This is made to scrape the rules of VAR
    page = requests.get("https://www.telegraph.co.uk/football/0/var-premier-league-explained-does-work-decisions-can-changed/")
    soup = BeautifulSoup(page.content, 'html.parser')
    arr = []
    var = soup.find_all('p', limit=15)

    for p_tag in var:
            arr.append(p_tag.text)
            arr.append(p_tag.next_sibling)

    return render_template("serie.html",entries=rv,array1=arr)

@app.route('/post_comment_serie', methods=['POST', 'GET'])
def post_comment_serie():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	insert_comment_serie(request.form['Username'], request.form['Comment'])
	
	return redirect(url_for('Serie'))

def insert_comment_serie(Username, Comment):
	"""
	put a new entry in the database
	"""
	params = {'Username':Username, 'Comment':Comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into usrCommentsser VALUES (:Username, :Comment)",params)
	connection.commit()
	cursor.close()

@app.route("/signup", methods=["GET", "POST"])
def Sign():
    if request.method == "POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        confirmpw=request.form["confirmpw"]

        if password==confirmpw:
            params={"username":username, "email":email, "password":password}
            connection1 = sqlite3.connect(DB_FILE)
            cursor1 = connection1.cursor()
            cursor1.execute("insert into users VALUES (:username, :email, :password)", params)
            connection1.commit()
            cursor1.close()

            return redirect (url_for('Index'))
        else:
            return render_template("signup.html")

    return render_template("signup.html") 

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        query = "select * from users where username = '" + request.form['Username']
        query = query + "' and password = '" + request.form['Password'] + "';"
        connection = sqlite3.connect(DB_FILE)
        cur = connection.execute(query)
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 1:
           
            session['username'] = request.form['Username']
            session['logged in'] = True

            return redirect("index")
        else:
            return render_template('login.html', msg="Username/Password Incorrect!")
    else:
        return render_template('login.html')

# logout

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged in'] = False
    return redirect("index")


def _insert(name, age, comment):
	"""
	put a new entry in the database
	"""
	params = {'name':name, 'age':age, 'comment':comment}
	connection = sqlite3.connect(DB_FILE)
	cursor = connection.cursor()  
	cursor.execute("insert into guestbook VALUES (:name, :age, :comment)",params)
	connection.commit()
	cursor.close()

@app.route('/intro' , methods = ['POST', 'GET'])
def Guestbook():
	""" 
	An input form for signing the guestbook  
	"""
	try:
		connection = sqlite3.connect(DB_FILE)
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM guestbook")
		rv = cursor.fetchall()
		#print(rv)
		temp = weather_()
		cursor.close()
		return render_template("intro.html", entries=rv, temp=temp)
	except:
		return render_template("error.html", msg=sys.ecx_info())

def weather_():
        page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
        soup = BeautifulSoup(page.content, 'html.parser')
        seven_day = soup.find(id="seven-day-forecast")
        forecast_items = seven_day.find_all(class_="tombstone-container")
        tonight = forecast_items[0]
        print(tonight.prettify())

	## Extracting forecast data
        period = tonight.find(class_='period-name').get_text()
        short_desc = tonight.find(class_='short-desc').get_text()
        temp = tonight.find(class_='temp').get_text()
        return temp
    
@app.route('/sign', methods=['POST'])
def sign():
	"""
	Accepts POST requests, and processes the form;
	Redirect to index when completed.
	"""
	_insert(request.form['name'], request.form['age'], request.form['comment'])
	
	return redirect(url_for('Guestbook'))

if __name__ == "__main__":
    app.run(debug=True)
