import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

import streamlit as st

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

from datetime import datetime

import numpy as np
import pandas as pd

from deta import Deta

# Enable the cache by providing the name of the cache folder
#ff1.Cache.clear_cache('cache')
ff1.Cache.enable_cache('cache') 

# Database setup
DETA_KEY = "b0c6conepbn_sCXCz4BFP3tTzQbqRvoWT55PjD33V8hJ"
deta = Deta(DETA_KEY)
db = deta.Base("competitors_db")

#-----METHODS----------

#calculates the points for a grand prix for all the players in a competition
def calculate_points(competitors, year, grand_prix):

    #load session results
    session = ff1.get_session(year, grand_prix, 'R')
    session.load()
    laps = session.laps
    results = session.results
    results = results[["Abbreviation", "ClassifiedPosition"]]
   
    #calculate points for ccompetitors
    for x in competitors:
       
        my_guess = str_to_arr(get_guess_db(x, grand_prix))
       
        if len(my_guess) != 20:
            print("wrong length")
        else:
            my_total = 0
            print('Points for the ' + str(year) + ' ' + session.event.EventName + ' ')
            for i in range(20):
                curr_row = results.loc[results["Abbreviation"] == my_guess[i]]
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
            
            print("Points for " + x + ": " + str(my_total))
            set_points_db(x, grand_prix, my_total)


#converts guess string to array
def str_to_arr(str):
    return str.split(', ')

#gets total points for all people in a competition
def get_leaderboard(comp):
    for player in comp.get_competitors_names():
        points = get_total_points_db(player)
        print("Total points for " + player.get_name() + ": " + str(points))

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



#------DATABASE-METHODS------

#def get_competetitor_by_name():
    
def get_total_points_db(name):
    persondb = comp.get_competitor_by_name(name)
    
    pointsdb = persondb["points"]
    
    tot = 0
    for i in range(len(pointsdb)):
        tot += pointsdb[i]
    return tot

def set_guess_db(name, gp, guess):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses"]
    guessdb[gp-1] = guess
    db.update({"guesses": guessdb}, name)

def get_guess_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses"]
    return guessdb[gp-1]

def set_points_db(name, gp, n):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points"]
    pointsdb[gp-1] = n
    db.update({"points" : pointsdb}, name)

def get_points_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points"]
    return pointsdb[gp-1]



#------Classes--------

#competitor class for each user
class Competitor:
    def __init__(self, name):
        self.name = name
        self.points = np.zeros(23)
        #s = (23)
        self.guesses = ["" for x in range(23)]

    def get_points(self):
        return self.points
    
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
        return db.put({"key": person.get_name(), "points": np.array(person.get_points()).tolist(), "guesses": np.array(person.get_guesses()).tolist()})
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

            


#-------MAIN---------


comp = Competition()


#flo_guess = "PER, VER, LEC, HAM, SAI, ALO, NOR, RUS, ALB, SAR, OCO, MAG, GAS, STR, HUL, PIA, BOT, ZHO, TSU, DEV"
#sof_guess = "VER, PER, SAI, ALO, NOR, LEC, HAM, ALB, OCO, RUS, HUL, STR, GAS, PIA, MAG, BOT, TSU, SAR, DEV, ZHO"
#luk_guess = "VER, PER, ALO, SAI, HAM, LEC, ALB, RUS, STR, NOR, OCO, SAR, PIA, GAS, HUL, ZHO, BOT, DEV, TSU, MAG"
#abi_guess = "VER, PER, ALO, HAM, SAI, LEC, RUS, STR, OCO, NOR, GAS, HUL, ALB, PIA, BOT, ZHO, TSU, MAG, SAR, DEV"

#flo_guess2 = "VER, PER, ALO, LEC, HAM, SAI, RUS, OCO, NOR, STR, GAS, ALB, BOT, PIA, SAR, HUL, RIC, TSU, ZHO, MAG"
#sof_guess2 = "VER, NOR, PER, ALO, LEC, RUS, HAM, SAI, HUL, STR, BOT, PIA, OCO, TSU, ALB, GAS, MAG, ZHO, RIC, SAR"
#luk_guess2 = "VER, ALO, PER, HAM, RUS, NOR, SAI, LEC, STR, ALB, PIA, SAR, OCO, RIC, GAS, HUL, BOT, TSU, ZHO, MAG"
#abi_guess2 = "ALO, PER, NOR, PIA, RUS, SAI, HAM, LEC, RIC, STR, MAG, OCO, ALB, BOT, GAS, ZHO, HUL, SAR, TSU, VER"

#set_guess_db("Florence", 11, flo_guess2)
#set_guess_db("Sofia", 11, sof_guess2)
#set_guess_db("Luke", 11, luk_guess2)
#set_guess_db("Abigail", 11, abi_guess2)
#calculate_points(comp.get_competitors_names(), 2023, 11)

#get_leaderboard(comp)




#------ Frontend with streamlit
st.set_page_config(page_title='Formula 1 Race Predictions',page_icon = ':racing_car:', layout = "centered")
st.title('Formula 1 Race Predictions' + " " + ':racing_car:')

tabs = st.tabs(["Enter Guess", "Your Results", "View Leaderboard", "Manage Game", "Race Stats"])

tabs_guess = tabs[0]

with tabs_guess:
    userstouse = comp.get_competitors_names()
    users = [""]
    for i in userstouse:
        users.append(i)
    gps = ["Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
    drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'RIC']
    st.header(f"Enter your guess")
    with st.form("entry_form", clear_on_submit = True):
        user = st.selectbox("Select Person:", users)
        gp = st.selectbox("Select a Grand Prix:", gps)
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.selectbox("p1:", drivers)
            p2 = st.selectbox("p2:", drivers)
            p3 = st.selectbox("p3:", drivers)
            p4 = st.selectbox("p4:", drivers)
            p5 = st.selectbox("p5:", drivers)
            p6 = st.selectbox("p6:", drivers)
            p7 = st.selectbox("p7:", drivers)
            p8 = st.selectbox("p8:", drivers)
            p9 = st.selectbox("p9:", drivers)
            p10 = st.selectbox("p10:", drivers)
        with col2:
            p11 = st.selectbox("p11:", drivers)
            p12 = st.selectbox("p12:", drivers)
            p13 = st.selectbox("p13:", drivers)
            p14 = st.selectbox("p14:", drivers)
            p15 = st.selectbox("p15:", drivers)
            p16 = st.selectbox("p16:", drivers)
            p17 = st.selectbox("p17:", drivers)
            p18 = st.selectbox("p18:", drivers)
            p19 = st.selectbox("p19:", drivers)
            p20 = st.selectbox("p20:", drivers)
        submitted = st.form_submit_button("Enter")
        if submitted:
                gp_num = 0
                for x in range(len(gps)):
                    if gp == gps[x]:
                        gp_num = x + (23-len(gps))
                if user == '' or gp_num == 0:
                    st.write('Select a user and Grand Prix to enter a guess')
                else:
                    guess_concat = p1 + ", " + p2 + ", " + p3 + ", " + p4 + ", " + p5 + ", " + p6 + ", " + p7 + ", " + p8 + ", " + p9 + ", " + p10 + ", " + p11 + ", " + p12 + ", " + p13 + ", " + p14 + ", " + p15 + ", " + p16 + ", " + p17 + ", " + p18 + ", " + p19 + ", " + p20
                    set_guess_db(user, gp_num, guess_concat)
                    st.write("Guess Entered for " + user + " for the " + gp + " Grand Prix")

                
tabs_results = tabs[1]

with tabs_results:
    st.header(f"View your Guess and Race Points")
    with st.form("view_form", clear_on_submit = False):
        userstouse = comp.get_competitors_names()
        users = [""]
        for i in userstouse:
            users.append(i)
        gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        userSelect = st.selectbox("Select Person:", users)
        gpSelect = st.selectbox("Select a Grand Prix:", gps)
        submitted2 = st.form_submit_button("Enter")
        if submitted2:
                gp_num = 0
                for x in range(len(gps)):
                    if gpSelect == gps[x]:
                        gp_num = x + (23-len(gps))
                if userSelect == '' or gp_num == 0:
                    st.write('Select a user and Grand Prix to view a guess')
                elif get_guess_db(userSelect, gp_num) == None:
                    st.write('No guess has been entered for this Grand Prix')
                else:
                    st.write('**Points: ' + str(get_points_db(userSelect, gp_num)) + '**')
                    st.write('**Guess:**')
                    col1, col2 = st.columns(2)
                    gs = get_guess_db(userSelect, gp_num)
                    gs = str_to_arr(gs)
                    gs1 = gs[:10]
                    gs2 = gs[-10:]
                    tick = 1
                    with col1:
                        for i in gs1:
                            st.write(str(tick) + ': ' + str(i))
                            tick = tick + 1
                    tick = 11
                    with col2:
                        for i in gs2:
                            st.write(str(tick) + ': ' + str(i))
                            tick = tick + 1

    st.header(f"Race Trends")
    st.write("coming soon!")

tabs_leaderboard = tabs[2]

with tabs_leaderboard:
    st.header(f"Leaderboard")
    fig, ax = plt.subplots()
    
    for player in comp.get_competitors_names():
        points = get_total_points_db(player)
        st.write("Total points for " + player + ": " + str(points))

        plt.barh(
            y=player,
            width=points,
            edgecolor="black",
            fill=True
        )
    plt.xlabel("Points")
    plt.ylabel("Competitor")
    plt.grid(False)
    plt.suptitle("Total Points")
    st.pyplot(fig)

    st.header(f"Leaderboard per Race")
    with st.form("res_form", clear_on_submit = False):
        gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        gp = st.selectbox("Select a Grand Prix:", gps)
        submitted = st.form_submit_button("Enter")
        if submitted:
                gp_num = 0
                for x in range(len(gps)):
                    if gp == gps[x]:
                        gp_num = x + (23-len(gps))
                if gp_num == 0:
                    st.write('Select a Grand Prix')
                else:
                    fig, ax = plt.subplots()
        
                    for player in comp.get_competitors_names():
                        points = get_points_db(player, gp_num)
                        st.write("Points for " + player + ": " + str(points))

                        plt.barh(
                            y=player,
                            width=points,
                            edgecolor="black",
                            fill=True
                        )
                    plt.xlabel("Points")
                    plt.ylabel("Competitor")
                    plt.grid(False)
                    plt.suptitle(gp + ' Grand Prix Prediction Results')
                    st.pyplot(fig)
                    



tabs_manage = tabs[3]

with tabs_manage:
    competitor_name = st.text_input('Enter Competitor Name', '')
    if st.button("Add Competitor"): 
        if competitor_name in comp.get_competitors_names():
            st.write("Sorry, this name is taken")
        else:
            comp.add_competitor(Competitor(competitor_name))
            st.write("Competitor Added, Refresh Page to See Competitor")
            #st.write(str(comp.get_competitors_names()))


tabs_stats = tabs[4]

with tabs_stats:
    st.write("coming soon!")

    
    
    




                
            
            






