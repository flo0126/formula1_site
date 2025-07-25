#------SETUP---------------------------------

import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

import streamlit as st

from streamlit_sortables import sort_items


from matplotlib import pyplot as plt
from matplotlib.pyplot import figure


from datetime import datetime

import numpy as np
import pandas as pd

#from deta import Deta

from PIL import Image


from sqlalchemy.sql import text

import psycopg2
conn2 = psycopg2.connect("postgresql://competitors_owner:GMOeQ51NiFwp@ep-polished-snow-a5xqn4ws.us-east-2.aws.neon.tech/competitors?sslmode=require")
cursor = conn2.cursor()




#hello



# Enable the cache by providing the name of the cache folder
#ff1.Cache.clear_cache('cache')
ff1.Cache.enable_cache('cache') 

# Database setup
#DETA_KEY = "b0c6conepbn_sCXCz4BFP3tTzQbqRvoWT55PjD33V8hJ"
#deta = Deta(DETA_KEY)
#db = deta.Base("competitors_db")
#rrdb = deta.Base("raceround_db")

DRIVER_ORDER = ['VER', 'LAW', 'LEC', 'HAM', 'NOR', 'PIA', 'ANT', 'RUS', 'ALO', 'STR', 'GAS', 'DOO', 'OCO', 'BEA', 'ALB', 'SAI', 'HUL', 'BOR',  'TSU', 'HAD', 'COL']
DRIVER_ORDERnodev = ['VER', 'LAW', 'LEC', 'HAM', 'NOR', 'PIA', 'ANT', 'RUS', 'ALO', 'STR', 'GAS', 'DOO', 'OCO', 'BEA', 'ALB', 'SAI', 'HUL', 'BOR',  'TSU', 'HAD']
TEAM_COLOR_RGB = [(0.078, 0.122, 0.702, 1), (0.078, 0.122, 0.702, 1), (1, 0.008, 0.008, 1), (1, 0.008, 0.008, 1), (0.4, 0.929, 0.929, 1), (0.4, 0.929, 0.929, 1), (0.059, 0.451, 0.251, 1), (0.059, 0.451, 0.251, 1), (1, 0.341, 0.827,1), (1, 0.341, 0.827, 1), (1, 0.494, 0, 1), (1, 0.494, 0, 1),
              (0.612, 0.612, 0.612, 1), (0.612, 0.612, 0.612, 1), (0.251, 0.439, 1, 1), (0.251, 0.439, 1, 1), (0, 0.91, 0.078, 1), (0, 0.91, 0.078, 1), (0, 0.012, 1, 1), (0, 0.012, 1, 1), (0, 0.012, 1, 1) ]
TEAM_COLOR = ['darkblue', 'darkblue', 'red', 'red', 'darkorange', 'darkorange', 'turquoise', 'turquoise', 'seagreen', 'seagreen', 'hotpink', 'hotpink', 'silver', 'silver', 'royalblue', 'royalblue', 'lime', 'lime', 'blue', 'blue', 'blue']
TEAM_ORDER = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "McLaren", "McLaren", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "Haas", "Haas", "Williams", "Williams", "Alfa Romeo", "Alfa Romeo", "Alpha Tauri", "Alpha Tauri","Alpha Tauri"]
TEAM_ORDERnodev = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "McLaren", "McLaren", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "Haas", "Haas", "Williams", "Williams", "Sauber", "Sauber", "RB", "RB"]
DRIVER_NUM = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
DRIVER_DICT = { 'VER':'Max Verstappen - Red Bull', 'LAW': 'Liam Lawson - Red Bull', 'LEC':'Charles Leclerc - Ferrari' , 'HAM':'Lewis Hamilton - Ferrari' , 'ANT': 'Kimi Antonelli - Mercedes', 'RUS':'George Russell - Mercedes', 'ALO':'Fernando Alonso - Aston Martin', 'STR':'Lance Stroll - Aston Martin', 'GAS':'Pierre Gasly - Alpine', 'DOO':'Jack Doohan - Alpine',
                'NOR':'Lando Norris - Mclaren', 'PIA':'Oscar Piastri - Mclaren', 'OCO':'Esteban Ocon - Haas', 'BEA':'Ollie Bearman - Haas', 'ALB':'Alex Albon - Williams', 'SAI':'Carlos Sainz - Williams', 'HUL':'Nico Hulkenberg - Stake', 'BOR':'Gabriel Bortoleto - Stake', 'TSU':'Yuki Tsunoda - VCARB' , 'HAD':'Isack Hadjar - VCARB' , 'DEV':'Nyck Devries - RB', 'COL': 'Franco Colapinto - Williams'}

ADMIN_PASS = "jamesitsvaltteri"

#-----METHODS----------

#calculates the points for a grand prix for all the players in a competition
def calculate_points(competitors, year, grand_prix):

    #load session results
    ff1.set_log_level('DEBUG')
    session = ff1.get_session(year, grand_prix, 'R')
    session.load()
    #laps = session.laps
    results = session.results
    print(results)
    results = results[["Abbreviation", "ClassifiedPosition"]]
    print(results)
    
    #abshere = ['PIA', 'NOR', 'RUS', 'VER', 'OCO', 'ANT', 'ALB', 'BEA', 'STR', 'SAI', 'HAD', 'LAW', 'DOO', 'BOR', 'HUL', 'TSU', 'ALO', 'LEC', 'HAM', 'GAS']
    #cp = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

    #results = pd.DataFrame({'Abbreviation': abshere, "ClassifiedPosition": cp}, columns=['Abbreviation', "ClassifiedPosition"])
    
    
   
    #calculate points for ccompetitors
    for x in competitors:
       
        my_guess = str_to_arr(get_guess_db24(x, grand_prix))
        #print(my_guess)
       
        if len(my_guess) != 20:
            print("wrong length")
        else:
            my_total = 0
            coll_points = np.zeros(21, dtype = int)
            print('Points for the ' + str(year) + ' ' + session.event.EventName + ' ')
            for i in range(20):
                try:
                    curr_row = results.loc[results["Abbreviation"] == my_guess[i]]
                    #if my_guess[i] == 'SAI':
                        #curr_row = results.loc[results["Abbreviation"] == 'BEA']
                    curr_pos = curr_row.iat[0,1]
                    act_pos = i + 1
                    points = 0
                    if curr_pos == 'R' or '':
                        curr_pos = '10000' #DNF
                    if abs(act_pos - int(curr_pos)) == 2:
                        points =  1
                    if abs(act_pos - int(curr_pos)) == 1:
                        points = 2
                    if abs(act_pos - int(curr_pos)) == 0:
                        points = 3
                    my_total = my_total + points
                    print(my_guess[i] + ": " + str(points))
                    for y in range(21):
                        if my_guess[i] == DRIVER_ORDER[y]:
                            coll_points[y] = int(points)
                except:
                    print(my_guess[i] + " did not start race")
            
            print("Points for " + x + ": " + str(my_total))
            set_points_db24(x, grand_prix, my_total)
            set_coll_points_db24(x, grand_prix, points_driver_to_string(coll_points))


#converts guess string to array
def str_to_arr(str):
    if str == None:
        return []
    return str.split(', ')

#gets total points for all people in a competition
#def get_leaderboard(comp):
    #for player in comp.get_competitors_names():
        #points = get_total_points_db(player)
        #print("Total points for " + player + ": " + str(points))

#checks it is valid to enter a guess and sets guess
def enter_guess(gp, competitor, guess):
    #load seession
    session = ff1.get_session(2023, gp, 'Q')
    session.load()

    #get gp date
    gpdate = session.date
    gpdt = gpdate.to_pydatetime()

    #get todays date
    today = datetime.now()

    #compare dates
    if today<gpdt:
        competitor.set_guess(gp, guess)
    else:
        print('Cannot enter a prediction after qualifying occurs')

def points_driver_to_string(arr):
    return ', '.join(str(v) for v in arr)

#------DATABASE-METHODS------
def get_round_db():
    #cf = rrdb.fetch()
    #r = cf.items
    #round = [item["round"] for item in r]
    #return round[0]
    cursor.execute('SELECT id FROM round_db')
    round = cursor.fetchone()[0]
    return int(round)

def set_round_db(round):
    #rrdb.update({"round": round}, "current round")
    cursor.execute('UPDATE round_db SET id='+ str(round))
    conn2.commit()

#points for all races for 1 person  
#def get_total_points_db(name):
#    persondb = comp.get_competitor_by_name(name)
#   
#    pointsdb = persondb["points"]
#    
#    tot = 0
#    for i in range(len(pointsdb)):
#        tot += pointsdb[i]
#    return tot

def get_total_points_db24(name):
    #persondb = comp.get_competitor_by_name(name)
    
    #pointsdb = persondb["points24"]

    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    pointsdb = cursor.fetchone()[2]
    pointsdb = np.array(pointsdb)
    
    tot = 0
    for i in range(len(pointsdb)):
        tot += pointsdb[i]
    return tot

#def set_guess_db(name, gp, guess):
#    persondb = comp.get_competitor_by_name(name)
#    guessdb = persondb["guesses"]
#    guessdb[gp-1] = guess
#    db.update({"guesses": guessdb}, name)

def set_guess_db24(name, gp, guess):
    #persondb = comp.get_competitor_by_name(name)
    #guessdb = persondb["guesses24"]
    #guessdb[gp-1] = guess
    #db.update({"guesses24": guessdb}, name)
   
    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    guesses = cursor.fetchone()[1]
    guesses[gp-1] = guess

    sqlstatement2 = 'UPDATE competitors_db SET guesses24=ARRAY' + str(guesses) + ' WHERE name = '+ namemine
    cursor.execute(sqlstatement2)
    conn2.commit()
    


#def get_guess_db(name, gp):
#    persondb = comp.get_competitor_by_name(name)
#    guessdb = persondb["guesses"]
#    return guessdb[gp-1]

def get_guess_db24(name, gp):
    #persondb = comp.get_competitor_by_name(name)
    #guessdb = persondb["guesses24"]
    #return guessdb[gp-1]
    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    me = cursor.fetchone()[1]
    me = np.array(me)
    return me[gp-1]

#points for 1 race for 1 person
#def set_points_db(name, gp, n):
#    persondb = comp.get_competitor_by_name(name)
#    pointsdb = persondb["points"]
#    pointsdb[gp-1] = n
#    db.update({"points" : pointsdb}, name)

def set_points_db24(name, gp, n):
    #persondb = comp.get_competitor_by_name(name)
    #pointsdb = persondb["points24"]
    #pointsdb[gp-1] = n
    #db.update({"points24" : pointsdb}, name)

    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    pointsdb = cursor.fetchone()[2]
    pointsdb[gp-1] = n

    sqlstatement2 = 'UPDATE competitors_db SET points24=ARRAY' + str(pointsdb) + ' WHERE name = '+ namemine
    cursor.execute(sqlstatement2)
    conn2.commit()


#points for 1 race for 1 person
#def get_points_db(name, gp):
#    persondb = comp.get_competitor_by_name(name)
#    pointsdb = persondb["points"]
#    return pointsdb[gp-1]

def get_points_db24(name, gp):
    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    pointsdb = cursor.fetchone()[2]
    pointsdb = np.array(pointsdb)
    return pointsdb[gp-1]

#def set_coll_points_db(name, gp, arr):
    #persondb = comp.get_competitor_by_name(name)
    #arrdb = persondb["pointsdriver"]
    #arrdb[gp-1] = arr
    #db.update({"pointsdriver": arrdb}, name)

def set_coll_points_db24(name, gp, arr):
    #persondb = comp.get_competitor_by_name(name)
    #arrdb = persondb["pointsdriver24"]
    #arrdb[gp-1] = arr
    #db.update({"pointsdriver24": arrdb}, name)

    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    pointsdb = cursor.fetchone()[3]
    pointsdb[gp-1] = arr

    sqlstatement2 = 'UPDATE competitors_db SET pointsdriver=ARRAY' + str(pointsdb) + ' WHERE name = '+ namemine
    cursor.execute(sqlstatement2)
    conn2.commit()


#def get_coll_points_db(name, gp):
    #persondb = comp.get_competitor_by_name(name)
    #arrdb = persondb["pointsdriver"]
    #return arrdb[gp-1]

def get_coll_points_db24(name, gp):
    #persondb = comp.get_competitor_by_name(name)
    #arrdb = persondb["pointsdriver24"]
    #return arrdb[gp-1]

    namemine = "'" + name + "'" 
    sqlstatement = 'Select * from competitors_db where name=' + namemine
    cursor.execute(sqlstatement)
    pointsdb = cursor.fetchone()[3]
    pointsdb = np.array(pointsdb)
    return pointsdb[gp-1]




#------Classes--------

#competitor class for each user
#maybe get rid of this???
class Competitor:
    def __init__(self, name):
        self.name = name
        self.points = np.zeros(23)
        self.points24 = np.zeros(24)
        #s = (23)
        self.guesses = ["" for x in range(23)]

    def get_points(self):
        return self.points
    
    def get_points24(self):
        return self.points24
    
    def set_points(self, gp, n):
        self.points[gp-1] = n

    def get_total_points(self):
        tot = 0
        for i in range(23):
            tot += self.points[i]
        return tot
    
    def get_gp_points(self, gp):
        return self.points[gp-1]
    
    def set_guess(self, gp, guess):
        self.guesses[gp-1] = guess
    
    def get_guess(self, gp):
        return self.guesses[gp-1]
    
    def get_guesses(self):
        return self.guesses
    
    def get_name(self):
        return self.name
    
#competition class for a game
class Competition:
    def __init__(self):
        self.competitors = []

    def add_competitor(self, person):
        self.competitors.append(person)
        toadd = (person.get_name(), ["" for x in range(24)], np.array(person.get_points24()).tolist(), ["" for x in range(24)])
        cursor.execute('INSERT INTO competitors_db VALUES (%s, %s, %s, %s)', toadd)
        conn2.commit()
        #return db.put({"key": person.get_name(), "points": np.array(person.get_points()).tolist(), "guesses": np.array(person.get_guesses()).tolist(), "pointsdriver": ["" for x in range(23)],
                       #"points24": np.array(person.get_points24()).tolist(), "guesses24": ["" for x in range(24)], "pointsdriver24": ["" for x in range(24)]})
        
        

    def get_competitors(self):
        #return self.competitors
        #res = db.fetch()
        #items = res.items
        #competitors = [item["key"] for item in items]
        #return competitors

        cursor.execute('SELECT name FROM competitors_db ORDER BY name')
        thenames = cursor.fetchall()
        nameslist = []
        for singlename in thenames:
            nameslist.append(singlename[0])
        return nameslist

    
    #def remove_competitor(self, person):
        #self.competitors.remove(person)
        #db.delete("person")

    def get_competitors_names(self):
        #namelist = []
        
        #for x in self.competitors:
        #    namelist.append(x.get_name())
        #return namelist

        competitors = self.get_competitors()
        return competitors


    
    #def get_competitor_by_name(self, name):
        #for x in self.competitors:
        #    if name == x.get_name():
        #        return x
        #competitor = db.get(name)
        #return competitor
    
   #def get_competitors_points(self):
        #res = db.fetch()
        #items = res.items
        #points = [item["points"] for item in items]
        #return points
    
    def get_competitors_points24(self):
        #res = db.fetch()
        #items = res.items
        #points = [item["points24"] for item in items]
        #print(points)
        #print(type(points[0]))
        cursor.execute('SELECT points24 FROM competitors_db ORDER BY name')
        everypoints = cursor.fetchall()
        allpoints = []
        for onething in everypoints:
            allpoints.append(onething[0])
        return allpoints
        #return points

            


#-------MAIN---------


comp = Competition()




#set_guess_db('Abigail', 20, "LEC, NOR, PIA, SAI, HAM, OCO, RIC, RUS, PER, TSU, GAS, ALO, HUL, BOT, ALB, MAG, SAR, ZHO, STR, VER")

#set_guess_db24('Sofia', 14, "VER, PER, LEC, SAI, HAM, RUS, ALO, STR, GAS, OCO, NOR, PIA, MAG, HUL, ALB, SAR, BOT, ZHO, TSU, RIC")
#set_guess_db24('Alex', 17, "VER, PER, LEC, SAI, HAM, RUS, ALO, STR, GAS, OCO, NOR, PIA, MAG, HUL, ALB, SAR, BOT, ZHO, TSU, RIC")
#set_guess_db24('Alex', 17, "VER, PER, LEC, SAI, HAM, RUS, ALO, STR, GAS, OCO, NOR, PIA, MAG, HUL, ALB, SAR, BOT, ZHO, TSU, RIC")
#set_guess_db24('test', 14, "VER, PER, LEC, SAI, HAM, RUS, ALO, STR, GAS, OCO, NOR, PIA, MAG, HUL, ALB, SAR, BOT, ZHO, TSU, RIC")


#calculate_points(comp.get_competitors_names(), 2025, 2)
#rrdb.put({"key": "current round", "round": 5})
#for i in comp.get_competitors_names():
    #print(get_round_db)
    #print(i)
    #print(get_guess_db24(i,17))








#------ Frontend with streamlit ----------------------------

#Set up page and title
st.set_page_config(page_title='Formula 1 Race Predictions',page_icon = ':racing_car:', layout = "centered")
#st.title('F1 Predictions' + " " + ':racing_car:')
conn = st.connection("neon", type="sql")


names_from_neon = conn.query('SELECT name FROM competitors_db ORDER BY name')
#st.text(names_from_neon)


st.write('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

im = Image.open('photos/f1predictions.png')
st.image(im)

st.markdown("""
    <style>
        .st-emotion-cache-1y4p8pa {
            width: 100%;
            padding: 3rem 1rem 10rem;
            max-width: 46rem;
        }
        
        
        

    </style>""", unsafe_allow_html=True)
if 'user' not in st.session_state:
    st.session_state['user'] = 'Invalid'

##login
logincont = st.empty()
createcont = st.empty()
amlog = False
with logincont.form("login form"):
    #st.header("Log in")
    userstouse = comp.get_competitors_names()
    useSel = st.selectbox("Select Competitor:", userstouse)
    submittedLogin = st.form_submit_button("Enter")
    if submittedLogin:
        st.session_state['user'] = useSel

with createcont.expander("New to the game? Create an account"):
    competitor_name = st.text_input('Enter Your Competitor Name', '')
    if st.button("Add New Competitor"): 
        if competitor_name in comp.get_competitors_names():
            st.error("Sorry, this name is taken")
        else:
            comp.add_competitor(Competitor(competitor_name))
            st.session_state['user'] = competitor_name


if st.session_state['user'] != 'Invalid':
    logincont.empty()
    createcont.empty()
    

    # Set Tabs
    tabs = st.tabs(["Enter Guess", "Your Results", "View Leaderboard", "Race Trends", "Admin View"])

    



    tabs_guess = tabs[0]

    #---------Enter Guess Tab-------------------------------------
    with tabs_guess:
        
        #userstouse = comp.get_competitors_names()
        #users = [""]
        #for i in userstouse:
            #users.append(i)
        #gps = ["China", "Miami", "Imola", "Monaco", "Canada", "Spain", "Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        allGps = ["Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco", "Spain", "Canada", "Austria", "Silverstone", "Spa", "Hungary", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]

        #drivers abbreviation
        drivers = ['VER', 'LAW', 'LEC', 'HAM', 'NOR', 'PIA', 'ANT', 'RUS', 'ALO', 'STR', 'GAS', 'DOO', 'OCO', 'BEA', 'ALB', 'SAI', 'HUL', 'BOR',  'TSU', 'HAD']
        driversRICTOLAW = ['VER', 'LAW', 'LEC', 'HAM', 'NOR', 'PIA', 'ANT', 'RUS', 'ALO', 'STR', 'GAS', 'DOO', 'OCO', 'BEA', 'ALB', 'SAI', 'HUL', 'BOR',  'TSU', 'HAD']
        
        #drivers with teams
        driversOrder = ['Max Verstappen - Red Bull', 'Liam Lawson - Red Bull', 'Charles Leclerc - Ferrari', 'Lewis Hamilton - Ferrari', 'Kimi Antonelli - Mercedes', 'George Russell - Mercedes', 'Fernando Alonso - Aston Martin', 'Lance Stroll - Aston Martin', 'Pierre Gasly - Alpine', 'Jack Doohan - Alpine', "Lando Norris - Mclaren", "Oscar Piastri - Mclaren", 'Esteban Ocon - Haas', 'Ollie Bearman - Haas', 'Alex Albon - Williams', 'Carlos Sainz - Williams', 'Nico Hulkenberg - Stake', 'Gabriel Bortoleto - Stake', 'Yuki Tsunoda - RB', 'Isack Hadjar - RB']
        drivdict = { 'VER':'Max Verstappen - Red Bull', 'LAW': 'Liam Lawson - Red Bull', 'LEC':'Charles Leclerc - Ferrari' , 'HAM':'Lewis Hamilton - Ferrari' , 'ANT': 'Kimi Antonelli - Mercedes', 'RUS':'George Russell - Mercedes', 'ALO':'Fernando Alonso - Aston Martin', 'STR':'Lance Stroll - Aston Martin', 'GAS':'Pierre Gasly - Alpine', 'DOO':'Jack Doohan - Alpine',
                'NOR':'Lando Norris - Mclaren', 'PIA':'Oscar Piastri - Mclaren', 'OCO':'Esteban Ocon - Haas', 'BEA':'Ollie Bearman - Haas', 'ALB':'Alex Albon - Williams', 'SAI':'Carlos Sainz - Williams', 'HUL':'Nico Hulkenberg - Stake', 'BOR':'Gabriel Bortoleto - Stake', 'TSU':'Yuki Tsunoda - VCARB' , 'HAD':'Isack Hadjar - VCARB' , 'DEV':'Nyck Devries - RB', 'COL': 'Franco Colapinto - Williams'}

        #without teams
        #driversOrder2 = ['Max Verstappen', 'Sergio Perez', 'Charles Leclerc', 'Carlos Sainz', 'Lewis Hamilton', 'George Russell', 'Fernando Alonso', 'Lance Stroll', 'Pierre Gasly', 'Esteban Ocon', "Lando Norris", "Oscar Piastri", 'Kevin Magnussen', 'Nico Hulkenberg', 'Alex Albon', 'Logan Sargeant', 'Valtteri Bottas', 'Zhou Guanyu', 'Yuki Tsunoda', 'Daniel Ricciardo']
        #drivdict2 = { 'VER':'Max Verstappen', 'LAW': 'Liam Lawson', 'LEC':'Charles Leclerc' , 'HAM':'Lewis Hamilton' , 'ANT': 'Kimi Antonelli', 'RUS':'George Russell', 'ALO':'Fernando Alonso', 'STR':'Lance Stroll', 'GAS':'Pierre Gasly', 'DOO':'Jack Doohan',
        #        'NOR':"Lando Norris", 'PIA':"Oscar Piastri", 'OCO':'Esteban Ocon', 'BEA':'Ollie Bearman', 'ALB':'Alex Albon', 'SAI':'Carlos Sainz', 'HUL':'Nico Hulkenberg', 'BOR':'Gabriel Bortoleto', 'TSU':'Yuki Tsunoda' , 'HAD':'Isack Hadjar' , 'DEV':'Nyck Devries', 'COL': 'Franco Colapinto'}
        drivdict2 = { 'Max Verstappen':'VER', 'Liam Lawson': 'LAW', 'Charles Leclerc':'LEC' , 'Lewis Hamilton':'HAM' , 'Kimi Antonelli':'ANT' , 'George Russell':'RUS', 'Fernando Alonso':'ALO', 'Lance Stroll':'STR', 'Pierre Gasly':'GAS', 'Jack Doohan':'DOO',
                'Lando Norris':'NOR', 'Oscar Piastri':'PIA', 'Esteban Ocon':'OCO', 'Ollie Bearman':'BEA', 'Alex Albon':'ALB', 'Carlos Sainz':'SAI', 'Nico Hulkenberg':'HUL', 'Gabriel Bortoleto':'BOR', 'Yuki Tsunoda':'TSU', 'Isack Hadjar':'HAD', 'Franco Colapinto':'COL' }



        driversOrder3 = ['Max Verstappen', 'Liam Lawson', 'Charles Leclerc', 'Lewis Hamilton', 'Lando Norris', 'Oscar Piastri', 'Kimi Antonelli', 'George Russell', 'Fernando Alonso', 'Lance Stroll', 'Pierre Gasly', 'Jack Doohan', 'Esteban Ocon', 'Ollie Bearman', 'Alex Albon', 'Carlos Sainz', 'Nico Hulkenberg', 'Gabriel Bortoleto', 'Yuki Tsunoda', 'Isack Hadjar']
        #drivdict3 = {'Max Verstappen': 'VER', 'Sergio Perez': 'PER', 'Charles Leclerc': 'LEC', 'Carlos Sainz': 'SAI', 'Lewis Hamilton':'HAM', 'George Russell':'RUS', 'Fernando Alonso':'ALO', 'Lance Stroll':'STR', 'Pierre Gasly':'GAS', 'Esteban Ocon':'OCO',
        #            "Lando Norris":'NOR', "Oscar Piastri":'PIA', 'Kevin Magnussen':'MAG', 'Nico Hulkenberg':'HUL', 'Alex Albon':'ALB', 'Franco Colapinto':'COL', 'Valtteri Bottas':'BOT', 'Zhou Guanyu': 'ZHO', 'Yuki Tsunoda': 'TSU', 'Daniel Ricciardo': 'RIC'}

        teams = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "McLaren", "McLaren", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "Haas", "Haas", "Williams", "Williams", "Alfa Romeo", "Alfa Romeo", "Alpha Tauri", "Alpha Tauri"]
        daf = pd.DataFrame({'drivers': driversOrder, 'abb': drivers}, columns=['drivers', 'abb'])

        round = get_round_db()
        
        st.header("Enter Guess for " + st.session_state['user'])
        st.subheader("Round "+ str(round) + ": " + allGps[round-1])

        #sorted_items2 = sort_items(driversOrder2, direction = 'vertical')

        #with st.form("entry_form", clear_on_submit = False):
            
            
            #gp = st.selectbox("Select a Grand Prix:", gps)
            
            
        
        st.write("Drag and dop to reorder the drivers below (If no drivers are shown, please refresh page):")
        col1, col2 = st.columns([10,12])
            
        with col1:
            sitems = sort_items(driversOrder3, direction="vertical")
            
                
                #gp = st.selectbox("Select a Grand Prix:", gps)
            
        
                #st.write("Drag and dop to reorder the drivers below (If no drivers are shown, please refresh page):")

                #st.write("Drag and dop to reorder the drivers below (If no drivers are shown, please refresh page):")
                #si1 = sort_items(['a','b','c','d'], direction='vertical')
                #items = [
                    #{'header': 'Drivers', 'items': driversOrder}
                    #]
                
            #sorted_items = sort_items(driversOrder2, direction = 'vertical')
                
            
            
        submitted = st.button("Enter")
        if submitted:
                
                gp_num = round
                #for x in range(len(gps)):
                #    if gp == gps[x]:
                #        
                #        gp_num = x + (24-len(gps)) + 1
                        
                if gp_num == -1: #removed user
                    st.error('Select a user and Grand Prix to enter a guess')
                else:
                    guessList = []
                    
                    #guessList = np.vectorize(drivdict.get)(sample)
                    
                    for v in range(20):
                        additem = drivdict2.get(sitems[v])
                        guessList.append(additem)
    
                    
                    ##guess_concat = p1 + ", " + p2 + ", " + p3 + ", " + p4 + ", " + p5 + ", " + p6 + ", " + p7 + ", " + p8 + ", " + p9 + ", " + p10 + ", " + p11 + ", " + p12 + ", " + p13 + ", " + p14 + ", " + p15 + ", " + p16 + ", " + p17 + ", " + p18 + ", " + p19 + ", " + p20
                    guess_concat = ', '.join(guessList)
                    #print(guess_concat)
                    set_guess_db24(st.session_state['user'], gp_num, guess_concat)
                    st.success("Guess Entered for " + st.session_state['user'] + " for the " + allGps[round-1] + " Grand Prix")
        s = sort_items([], direction="vertical")



    tabs_results = tabs[1]

    #--------------- Your Results Tab--------------------
    with tabs_results:
        
        
        #userstouse = comp.get_competitors_names()
        #users = [""]
        #for i in userstouse:
            #users.append(i)
        gps = ["Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco", "Spain", "Canada", "Austria", "Silverstone", "Spa", "Hungary", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        #userSelect = st.selectbox("Select Competitor:", users)
        st.header("View Results for "+ st.session_state['user'])
        round = get_round_db()
        index = 0
        if round > 2:
            index = round - 2
        gpSelect = st.selectbox("Select a Grand Prix:", gps, index=index)

        st.subheader(gpSelect + " Guess")
        gp_num = 0
        for x in range(len(gps)):
            if gpSelect == gps[x]:
                gp_num = x + (24-len(gps)) + 1
        if gp_num == 0: #removed user == ''
            st.error('Select a Grand Prix to view a guess')
        elif get_guess_db24(st.session_state['user'], gp_num) == None:
            st.error('No guess has been entered for this Grand Prix')
        else:
            #st.write('**Points: ' + str(get_points_db(userSelect, gp_num)) + '**')
            #st.write('**Guess:**')
            col1, col2, col3 = st.columns([2,2,1])
            gs = get_guess_db24(st.session_state['user'], gp_num)
            gs = str_to_arr(gs)
            gs1 = gs[:10]
            gs2 = gs[-10:]
            tick = 1


            with col1:
                for i in gs1:
                    st.write(str(tick) + ': ' + str(DRIVER_DICT.get(i)))
                    tick = tick + 1
            tick = 11
            with col2:
                for i in gs2:
                    st.write(str(tick) + ': ' + str(DRIVER_DICT.get(i)))
                    tick = tick + 1

        st.write(" -- ")

        st.subheader(gpSelect + " Race Points")
        
            #userstouse = comp.get_competitors_names()
            #users = [""]
            #for i in userstouse:
                #users.append(i)
        #gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        #userSelect = st.selectbox("Select Competitor:", users)
        #gpSelect2 = st.selectbox("Select a Grand Prix:", gps)
        
        
        gp_num = 0
        for x in range(len(gps)):
            if gpSelect == gps[x]:
                gp_num = x + (24-len(gps)) + 1
        if gp_num == 0: #removed user
            st.error('Select a Grand Prix to view a guess')
        elif get_guess_db24(st.session_state['user'], gp_num) == None or get_guess_db24(st.session_state['user'], gp_num) == "":
            st.error('No guess has been entered for this Grand Prix')
        elif get_points_db24(st.session_state['user'], gp_num) == 0:
            st.error('Sorry, points have not been calculated yet')
        else:
            st.write('**Points: ' + str(get_points_db24(st.session_state['user'], gp_num)) + '**')
            
            gs = get_coll_points_db24(st.session_state['user'], gp_num)
            gs = str_to_arr(gs)
            df = pd.DataFrame(
                {'Driver': DRIVER_ORDER, 'Points': gs, 'Color': TEAM_COLOR, 'Num': DRIVER_NUM},
                columns=['Driver', 'Points', 'Color', 'Num']
            )
            df = df.sort_values(by=['Points', 'Num'], ascending=[True,False])
            
            fig, ax = plt.subplots()
            bars = plt.barh(df['Driver'], df['Points'], color=df['Color'])
            plt.grid(False)
            #plt.bar_label(bars)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.tick_params(left = False, right = False , labelleft = True , labelbottom = False, bottom = False)
            st.pyplot(fig)


                        
        



    tabs_leaderboard = tabs[2]

    #------------ Leaderboard Tab ---------------------------------
    with tabs_leaderboard:
        st.header(f"Leaderboard")
        fig, ax = plt.subplots()
        
        names_plot = comp.get_competitors_names()
        points_plot = np.sum(comp.get_competitors_points24(), axis = 1)
        df = pd.DataFrame({'name': names_plot, 'points': points_plot}, columns = ['name', 'points'])
        df = df.sort_values(by=['points'], ascending=True)
        color = (0.918, 0.047, 0.047, 1)
        bars = plt.barh(df['name'], df['points'], color=color)
        plt.grid(False)
        plt.bar_label(bars)
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        plt.tick_params(left = False, right = False , labelleft = True , labelbottom = False, bottom = False)
        st.pyplot(fig)

        st.header(f"Leaderboard per Race")
        
        
        gps2 = ["Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco", "Spain", "Canada", "Austria", "Silverstone", "Spa", "Hungary", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        round = get_round_db()
        index = 0
        if round > 2:
            index = round - 2
        gp3 = st.selectbox("Select Grand Prix:", gps2, index=index)
        #submitted = st.form_submit_button("Enter")
        
        gp_num = 0
        for x in range(len(gps)):
            if gp3 == gps[x]:
                gp_num = x + (24-len(gps)) + 1
        if gp_num == 0:
            st.error('Select a Grand Prix')
        else:
            fig, ax = plt.subplots()

            gpval = gp_num - 1
            points2 = np.array(comp.get_competitors_points24())
            points2 = points2[:, gpval]
            
            df2 = pd.DataFrame({'name': names_plot, 'points': points2}, columns = ['name', 'points'])
            df2 = df2.sort_values(by=['points'], ascending=True)
            color = (0.918, 0.047, 0.047, 1)
            bars = plt.barh(df2['name'], df2['points'], color=color)
            plt.grid(False)
            plt.bar_label(bars)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.tick_params(left = False, right = False , labelleft = True , labelbottom = False, bottom = False)
            st.pyplot(fig)
                        

    tabs_trends = tabs[3]

    #----------Race trends--------------------
    with tabs_trends:
        st.header(f"Your Race Trends")
        #st.write("coming soon!")
    
        #userstouse = comp.get_competitors_names()
        #users = [""]
        #for i in userstouse:
            #users.append(i)
        #userSelect = st.selectbox("Select Competitor:", users)
        #gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        gps = ["Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco", "Spain", "Canada", "Austria", "Silverstone", "Spa", "Hungary", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        
    
        data = np.array([TEAM_ORDERnodev, DRIVER_ORDERnodev])
        data = data.transpose()
        df = pd.DataFrame(
            data,
            columns=['Team', 'Driver']
        )
        arr = []
        #xarr = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        xarr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        for i in range(1,24):
            if get_points_db24(st.session_state['user'], i) != 0:
                ppd = get_coll_points_db24(st.session_state['user'], i)
                ppd = str_to_arr(ppd)
                
                ppd.pop() #remove last one bc only 20 drivers

                ppd = list(map(int,ppd))
                arr.append(ppd)
        
        
        if len(arr) > 1:
            arr = [list(i) for i in zip(*arr)]
            arr = np.array(arr)
            for a in range(len(arr)):
                arr[a] = arr[a].cumsum()
            #st.dataframe(df, hide_index = True)
            #TODO: not dataframe, this should be a graph of some sort
            fig, ax = plt.subplots()
            sess = ff1.get_session(2025,1,'R')
            for ind in range(len(arr)):
                driv = df['Driver'][ind]
                color =  ""
                #if driv == 'BOR':
                    #color =  ff1.plotting.get_driver_color('VER')
                #else:
                color = ff1.plotting.get_driver_color(driv,sess)
                print(color)
                ax.plot(gps[:len(arr[ind])], arr[ind], label = driv, color = color,)
            ax.legend(bbox_to_anchor=(1.0, 1.02))
            plt.xticks(rotation=90)
            plt.suptitle("Points for each driver")
            
            st.pyplot(fig)
        else:
            st.error("Sorry, not enough data yet!")


    tabs_2023 = tabs[4]

    #-----------2023 Results-------------------------------------
    #tabs_manage = tabs[5]

    #------------Manage Game Tab-----------------------------------
    #with tabs_manage:
    #    competitor_name = st.text_input('Enter Competitor Name', '')
    #    if st.button("Add Competitor"): 
    #        if competitor_name in comp.get_competitors_names():
    #            st.error("Sorry, this name is taken")
    #        else:
    #            comp.add_competitor(Competitor(competitor_name))
    #            st.success("Competitor Added, Refresh Page to See Competitor")
    #            #st.write(str(comp.get_competitors_names()))




    tabs_admin = tabs[4]

    #-------------- Admin View Tab -----------------------------------
    with tabs_admin:
        admin_enter = st.text_input('Enter Admin Password', '')
        if admin_enter == ADMIN_PASS:
            st.header("Calculate Points")
            with st.form("admin_form",clear_on_submit = False):
                gps = ["Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco", "Spain", "Canada", "Austria", "Silverstone", "Spa", "Hungary", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
                gp = st.selectbox("Select a Grand Prix:", gps)
                submitted = st.form_submit_button("Enter")
                if submitted:
                    gp_num = 0
                    for x in range(len(gps)):
                        if gp == gps[x]:
                            gp_num = x + (24-len(gps)) + 1
                    try:
                        calculate_points(comp.get_competitors_names(), 2025, gp_num)
                        st.success("all done")
                    except:
                        st.error("Something went wrong")
            st.header("Change Round")
            with st.form("admin_form_round", clear_on_submit = False):
                curr = get_round_db()
                gps = ["Australia", "China", "Japan", "Bahrain", "Saudi Arabia", "Miami", "Imola", "Monaco", "Spain", "Canada", "Austria", "Silverstone", "Spa", "Hungary", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
                #st.write("Current Round: " + gps[curr - 1])
                round = st.selectbox("Select Current Round:", gps)
                submitted = st.form_submit_button("Enter")
                if submitted:
                    gp_num = 0
                    for x in range(len(gps)):
                        if round == gps[x]:
                            gp_num = x + (24-len(gps)) + 1
                            set_round_db(gp_num)
                            st.success("round changed to "+ gps[gp_num - 1])


        else:
            st.error("Please enter correct password")

    




                
            
            







