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

from deta import Deta

from PIL import Image




# Enable the cache by providing the name of the cache folder
#ff1.Cache.clear_cache('cache')
ff1.Cache.enable_cache('cache') 

# Database setup
DETA_KEY = "b0c6conepbn_sCXCz4BFP3tTzQbqRvoWT55PjD33V8hJ"
deta = Deta(DETA_KEY)
db = deta.Base("competitors_db")

DRIVER_ORDER = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'RIC', 'DEV']
DRIVER_ORDERnodev = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'RIC']
TEAM_COLOR_RGB = [(0.078, 0.122, 0.702, 1), (0.078, 0.122, 0.702, 1), (1, 0.008, 0.008, 1), (1, 0.008, 0.008, 1), (0.4, 0.929, 0.929, 1), (0.4, 0.929, 0.929, 1), (0.059, 0.451, 0.251, 1), (0.059, 0.451, 0.251, 1), (1, 0.341, 0.827,1), (1, 0.341, 0.827, 1), (1, 0.494, 0, 1), (1, 0.494, 0, 1),
              (0.612, 0.612, 0.612, 1), (0.612, 0.612, 0.612, 1), (0.251, 0.439, 1, 1), (0.251, 0.439, 1, 1), (0, 0.91, 0.078, 1), (0, 0.91, 0.078, 1), (0, 0.012, 1, 1), (0, 0.012, 1, 1), (0, 0.012, 1, 1) ]
TEAM_COLOR = ['darkblue', 'darkblue', 'red', 'red', 'turquoise', 'turquoise', 'seagreen', 'seagreen', 'hotpink', 'hotpink', 'darkorange', 'darkorange', 'silver', 'silver', 'royalblue', 'royalblue', 'lime', 'lime', 'blue', 'blue', 'blue']
TEAM_ORDER = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "McLaren", "McLaren", "Haas", "Haas", "Williams", "Williams", "Alfa Romeo", "Alfa Romeo", "Alpha Tauri", "Alpha Tauri","Alpha Tauri"]
TEAM_ORDERnodev = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "McLaren", "McLaren", "Haas", "Haas", "Williams", "Williams", "Sauber", "Sauber", "RB", "RB"]
DRIVER_NUM = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
DRIVER_DICT = { 'VER':'Max Verstappen - Red Bull', 'PER': 'Sergio Perez - Red Bull', 'LEC':'Charles Leclerc - Ferrari' , 'SAI':'Carlos Sainz - Ferrari' , 'HAM': 'Lewis Hamilton - Mercedes', 'RUS':'George Russell - Mercedes', 'ALO':'Fernando Alonso - Aston Martin', 'STR':'Lance Stroll - Aston Martin', 'GAS':'Pierre Gasly - Alpine', 'OCO':'Esteban Ocon - Alpine',
                'NOR':"Lando Norris - Mclaren", 'PIA':"Oscar Piastri - Mclaren", 'MAG':'Kevin Magnussen - Haas', 'HUL':'Nico Hulkenburg - Haas', 'ALB':'Alex Albon - Williams', 'SAR':'Logan Sargeant - Williams', 'BOT':'Valtteri Bottas - Stake', 'ZHO':'Zhou Guanyu - Stake', 'TSU':'Yuki Tsunoda - RB' , 'RIC':'Daniel Ricciardo - RB' , 'DEV':'Nyck Devries - RB' }
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
    results = results[["Abbreviation", "ClassifiedPosition"]]
    print(results)
    #abshere = ['VER', 'PER', 'LEC', 'PIA', 'ALO', 'RUS', 'BEA', 'NOR', 'HAM', 'HUL', 'ALB', 'MAG', 'OCO', 'SAR', 'TSU', 'RIC', 'BOT', 'ZHO', 'STR', 'GAS']
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
def get_leaderboard(comp):
    for player in comp.get_competitors_names():
        points = get_total_points_db(player)
        print("Total points for " + player + ": " + str(points))

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


#points for all races for 1 person  
def get_total_points_db(name):
    persondb = comp.get_competitor_by_name(name)
    
    pointsdb = persondb["points"]
    
    tot = 0
    for i in range(len(pointsdb)):
        tot += pointsdb[i]
    return tot

def get_total_points_db24(name):
    persondb = comp.get_competitor_by_name(name)
    
    pointsdb = persondb["points24"]
    
    tot = 0
    for i in range(len(pointsdb)):
        tot += pointsdb[i]
    return tot

def set_guess_db(name, gp, guess):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses"]
    guessdb[gp-1] = guess
    db.update({"guesses": guessdb}, name)

def set_guess_db24(name, gp, guess):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses24"]
    guessdb[gp-1] = guess
    db.update({"guesses24": guessdb}, name)

def get_guess_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses"]
    return guessdb[gp-1]

def get_guess_db24(name, gp):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses24"]
    return guessdb[gp-1]

#points for 1 race for 1 person
def set_points_db(name, gp, n):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points"]
    pointsdb[gp-1] = n
    db.update({"points" : pointsdb}, name)

def set_points_db24(name, gp, n):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points24"]
    pointsdb[gp-1] = n
    db.update({"points24" : pointsdb}, name)

#points for 1 race for 1 person
def get_points_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points"]
    return pointsdb[gp-1]

def get_points_db24(name, gp):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points24"]
    return pointsdb[gp-1]

def set_coll_points_db(name, gp, arr):
    persondb = comp.get_competitor_by_name(name)
    arrdb = persondb["pointsdriver"]
    arrdb[gp-1] = arr
    db.update({"pointsdriver": arrdb}, name)

def set_coll_points_db24(name, gp, arr):
    persondb = comp.get_competitor_by_name(name)
    arrdb = persondb["pointsdriver24"]
    arrdb[gp-1] = arr
    db.update({"pointsdriver24": arrdb}, name)

def get_coll_points_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    arrdb = persondb["pointsdriver"]
    return arrdb[gp-1]

def get_coll_points_db24(name, gp):
    persondb = comp.get_competitor_by_name(name)
    arrdb = persondb["pointsdriver24"]
    return arrdb[gp-1]



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
        return db.put({"key": person.get_name(), "points": np.array(person.get_points()).tolist(), "guesses": np.array(person.get_guesses()).tolist(), "pointsdriver": ["" for x in range(23)],
                       "points24": np.array(person.get_points24()).tolist(), "guesses24": ["" for x in range(24)], "pointsdriver24": ["" for x in range(24)]})
        #TODO figure out solution for putting list in database

    def get_competitors(self):
        #return self.competitors
        res = db.fetch()
        items = res.items
        competitors = [item["key"] for item in items]
        return competitors

    
    def remove_competitor(self, person):
        self.competitors.remove(person)
        db.delete("person")

    def get_competitors_names(self):
        #namelist = []
        
        #for x in self.competitors:
        #    namelist.append(x.get_name())
        #return namelist

        competitors = self.get_competitors()
        return competitors


        
    
    def get_competitor_by_name(self, name):
        #for x in self.competitors:
        #    if name == x.get_name():
        #        return x
        competitor = db.get(name)
        return competitor
    
    def get_competitors_points(self):
        res = db.fetch()
        items = res.items
        points = [item["points"] for item in items]
        return points
    
    def get_competitors_points24(self):
        res = db.fetch()
        items = res.items
        points = [item["points24"] for item in items]
        return points

            


#-------MAIN---------


comp = Competition()




#set_guess_db('Abigail', 20, "LEC, NOR, PIA, SAI, HAM, OCO, RIC, RUS, PER, TSU, GAS, ALO, HUL, BOT, ALB, MAG, SAR, ZHO, STR, VER")

#calculate_points(comp.get_competitors_names(), 2024, 2)







#------ Frontend with streamlit ----------------------------

#Set up page and title
st.set_page_config(page_title='Formula 1 Race Predictions',page_icon = ':racing_car:', layout = "centered")
#st.title('F1 Predictions' + " " + ':racing_car:')
im = Image.open('photos/f1predictions.png')
st.image(im)
st.markdown("""
    <style>
        .st-emotion-cache-1y4p8pa {
            width: 100%;
            padding: 3rem 1rem 10rem;
            max-width: 46rem;
        }
        .sortable-item, .sortable-item:hover {
            margin: 5px;
            background-color: #a65050;
            color: #fff;
            padding-top: 3px;
            padding-bottom: 3px;
            height: 100%;
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
    tabs = st.tabs(["Enter Guess", "Your Results", "View Leaderboard", "Race Trends", "2023", "Admin View"])

    



    tabs_guess = tabs[0]

    #---------Enter Guess Tab-------------------------------------
    with tabs_guess:
        
        #userstouse = comp.get_competitors_names()
        #users = [""]
        #for i in userstouse:
            #users.append(i)
        gps = ["China", "Miami", "Imola", "Monaco", "Canada", "Spain", "Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'RIC',]
        driversRICTOLAW = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'LAW',]
        driversOrder = ['Max Verstappen - Red Bull', 'Sergio Perez - Red Bull', 'Charles Leclerc - Ferrari', 'Carlos Sainz - Ferrari', 'Lewis Hamilton - Mercedes', 'George Russell - Mercedes', 'Fernando Alonso - Aston Martin', 'Lance Stroll - Aston Martin', 'Pierre Gasly - Alpine', 'Esteban Ocon - Alpine', "Lando Norris - Mclaren", "Oscar Piastri - Mclaren", 'Kevin Magnussen - Haas', 'Nico Hulkenburg - Haas', 'Alex Albon - Williams', 'Logan Sargeant - Williams', 'Valtteri Bottas - Stake', 'Zhou Guanyu - Stake', 'Yuki Tsunoda - RB', 'Daniel Ricciardo - RB']
        drivdict = {'Max Verstappen - Red Bull': 'VER', 'Sergio Perez - Red Bull': 'PER', 'Charles Leclerc - Ferrari': 'LEC', 'Carlos Sainz - Ferrari': 'SAI', 'Lewis Hamilton - Mercedes':'HAM', 'George Russell - Mercedes':'RUS', 'Fernando Alonso - Aston Martin':'ALO', 'Lance Stroll - Aston Martin':'STR', 'Pierre Gasly - Alpine':'GAS', 'Esteban Ocon - Alpine':'OCO',
                    "Lando Norris - Mclaren":'NOR', "Oscar Piastri - Mclaren":'PIA', 'Kevin Magnussen - Haas':'MAG', 'Nico Hulkenburg - Haas':'HUL', 'Alex Albon - Williams':'ALB', 'Logan Sargeant - Williams':'SAR', 'Valtteri Bottas - Stake':'BOT', 'Zhou Guanyu - Stake': 'ZHO', 'Yuki Tsunoda - RB': 'TSU', 'Daniel Ricciardo - RB': 'RIC'}

        teams = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "McLaren", "McLaren", "Haas", "Haas", "Williams", "Williams", "Alfa Romeo", "Alfa Romeo", "Alpha Tauri", "Alpha Tauri"]
        daf = pd.DataFrame({'drivers': driversOrder, 'abb': drivers}, columns=['drivers', 'abb'])


        
        st.header("Enter Guess for " + st.session_state['user'])

        with st.form("entry_form", clear_on_submit = True):
            
            #user = st.selectbox("Select Competitor:", users)
            gp = st.selectbox("Select a Grand Prix:", gps)
            
        
            st.write("Drag and dop to reorder the drivers below (If no drivers are shown, please refresh page):")
            col1, col2 = st.columns([10,12])
            
            with col1:
                items = [
                    {'header': 'Drivers', 'items': driversOrder}
                    ]
                sorted_items = sort_items(driversOrder, direction = 'vertical')
                
            st.markdown("""
            <style>
                .sortable-item, .sortable-item:hover {
                    margin: 5px;
                    background-color: #a65050;
                    color: #fff;
                    padding-top: 3px;
                    padding-bottom: 3px;
                    height: 100%;
                }
                

            </style>""", unsafe_allow_html=True)
            submitted = st.form_submit_button("Enter")
            if submitted:
                    gp_num = -1
                    for x in range(len(gps)):
                        if gp == gps[x]:
                            
                            gp_num = x + (24-len(gps)) + 1
                            
                    if gp_num == -1: #removed user
                        st.error('Select a user and Grand Prix to enter a guess')
                    else:
                        guessList = []
                        
                        #guessList = np.vectorize(drivdict.get)(sample)
                        
                        for v in range(20):
                            additem = drivdict.get(sorted_items[v])
                            guessList.append(additem)
                        ##guess_concat = p1 + ", " + p2 + ", " + p3 + ", " + p4 + ", " + p5 + ", " + p6 + ", " + p7 + ", " + p8 + ", " + p9 + ", " + p10 + ", " + p11 + ", " + p12 + ", " + p13 + ", " + p14 + ", " + p15 + ", " + p16 + ", " + p17 + ", " + p18 + ", " + p19 + ", " + p20
                        guess_concat = ', '.join(guessList)
                        #print(guess_concat)
                        set_guess_db24(st.session_state['user'], gp_num, guess_concat)
                        st.success("Guess Entered for " + st.session_state['user'] + " for the " + gp + " Grand Prix")




    tabs_results = tabs[1]

    #--------------- Your Results Tab--------------------
    with tabs_results:
        
        
        #userstouse = comp.get_competitors_names()
        #users = [""]
        #for i in userstouse:
            #users.append(i)
        gps = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Imola", "Monaco", "Canada", "Spain", "Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        #userSelect = st.selectbox("Select Competitor:", users)
        st.header("View Results for "+ st.session_state['user'])
        gpSelect = st.selectbox("Select a Grand Prix:", gps)

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
            plt.bar_label(bars)
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
        
        gps2 = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Imola", "Monaco", "Canada", "Spain", "Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        gp3 = st.selectbox("Select Grand Prix:", gps2)
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
        gps = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Imola", "Monaco", "Canada", "Spain", "Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
        
    
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
            for ind in range(len(arr)):
                driv = df['Driver'][ind]
                color =  ""
                #if driv == 'RIC':
                    #color =  ff1.plotting.driver_color('DEV')
                #else:
                color = ff1.plotting.driver_color(driv)
                ax.plot(gps[:len(arr[ind])], arr[ind], label = driv, color = color,)
            ax.legend(bbox_to_anchor=(1.0, 1.02))
            plt.xticks(rotation=90)
            plt.suptitle("Points for each driver")
            
            st.pyplot(fig)
        else:
            st.error("Sorry, not enough data yet!")


    tabs_2023 = tabs[4]

    #-----------2023 Results-------------------------------------
    with tabs_2023:
        st.header(f"Leaderboard")
        fig, ax = plt.subplots()
        
        names_plot = comp.get_competitors_names()
        points_plot = np.sum(comp.get_competitors_points(), axis = 1)
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

        gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        #userSelect = st.selectbox("Select Competitor:", users)
        st.header("View Results for "+ st.session_state['user'])
        gpSelect2 = st.selectbox("Choose a Grand Prix:", gps)

        st.subheader(gpSelect2 + " Guess")
        gp_num = 0
        for x in range(len(gps)):
            if gpSelect2 == gps[x]:
                gp_num = x + (23-len(gps))
        if gp_num == 0: #removed user == ''
            st.error('Select a Grand Prix to view a guess')
        elif get_guess_db(st.session_state['user'], gp_num) == None:
            st.error('No guess has been entered for this Grand Prix')
        else:
            #st.write('**Points: ' + str(get_points_db(userSelect, gp_num)) + '**')
            #st.write('**Guess:**')
            col1, col2, col3 = st.columns([2,2,1])
            gs = get_guess_db(st.session_state['user'], gp_num)
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

        st.subheader(gpSelect2 + " Race Points")
        
            #userstouse = comp.get_competitors_names()
            #users = [""]
            #for i in userstouse:
                #users.append(i)
        #gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        #userSelect = st.selectbox("Select Competitor:", users)
        #gpSelect2 = st.selectbox("Select a Grand Prix:", gps)
        
        
        gp_num = 0
        for x in range(len(gps)):
            if gpSelect2 == gps[x]:
                gp_num = x + (23-len(gps))
        if gp_num == 0: #removed user
            st.error('Select a Grand Prix to view a guess')
        elif get_guess_db(st.session_state['user'], gp_num) == None or get_guess_db(st.session_state['user'], gp_num) == "":
            st.error('No guess has been entered for this Grand Prix')
        elif get_points_db(st.session_state['user'], gp_num) == 0:
            st.error('Sorry, points have not been calculated yet')
        else:
            st.write('**Points: ' + str(get_points_db(st.session_state['user'], gp_num)) + '**')
            
            gs = get_coll_points_db(st.session_state['user'], gp_num)
            gs = str_to_arr(gs)
            df = pd.DataFrame(
                {'Driver': DRIVER_ORDER, 'Points': gs, 'Color': TEAM_COLOR, 'Num': DRIVER_NUM},
                columns=['Driver', 'Points', 'Color', 'Num']
            )
            df = df.sort_values(by=['Points', 'Num'], ascending=[True,False])
            
            fig, ax = plt.subplots()
            bars = plt.barh(df['Driver'], df['Points'], color=df['Color'])
            plt.grid(False)
            plt.bar_label(bars)
            for spine in plt.gca().spines.values():
                spine.set_visible(False)
            plt.tick_params(left = False, right = False , labelleft = True , labelbottom = False, bottom = False)
            st.pyplot(fig)

        #gp_num = 0
        #for x in range(len(gps)):
            #if gp == gps[x]:
                #gp_num = x + (23-len(gps))
        st.subheader(gpSelect2 + " Race Leaderboard")
        if gp_num == 0:
            st.error('Select a Grand Prix')
        else:
            fig, ax = plt.subplots()

            gpval = gp_num - 1
            points2 = np.array(comp.get_competitors_points())
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




    tabs_admin = tabs[5]

    #-------------- Admin View Tab -----------------------------------
    with tabs_admin:
        admin_enter = st.text_input('Enter Admin Password', '')
        if admin_enter == ADMIN_PASS:
            st.header("Calculate Points")
            with st.form("admin_form",clear_on_submit = False):
                gps = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Imola", "Monaco", "Canada", "Spain", "Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Baku", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
                gp = st.selectbox("Select a Grand Prix:", gps)
                submitted = st.form_submit_button("Enter")
                if submitted:
                    gp_num = 0
                    for x in range(len(gps)):
                        if gp == gps[x]:
                            gp_num = x + (24-len(gps)) + 1
                    try:
                        calculate_points(comp.get_competitors_names(), 2024, gp_num)
                        st.success("all done")
                    except:
                        st.error("Something went wrong")

        else:
            st.error("Please enter correct password")

    




                
            
            







