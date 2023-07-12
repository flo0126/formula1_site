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
       
        my_guess = str_to_arr(x.get_guess(grand_prix))
       
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
            
            print("Points for " + x.get_name() + ": " + str(my_total))
            x.set_points(grand_prix, my_total)


#converts guess string to array
def str_to_arr(str):
    return str.split(', ')

#gets total points for all people in a competition
def get_leaderboard(comp):
    for player in comp.get_competitors():
        points = player.get_total_points()
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
        return self.competitors
        #res = db.fetch()
        #return res.items
    
    def remove_competitor(self, person):
        self.competitors.remove(person)

    def get_competitors_names(self):
        namelist = []
        
        for x in self.competitors:
            namelist.append(x.get_name())
        return namelist
    
    def get_competitor_by_name(self, name):
        for x in self.competitors:
            if name == x.get_name():
                return x
            


#-------MAIN---------
u1 = Competitor('Florence')
u2 = Competitor('Sofia')
u3 = Competitor('Luke')
u4 = Competitor('Abigail')
comp = Competition()
comp.add_competitor(u1)
comp.add_competitor(u2)
comp.add_competitor(u3)
comp.add_competitor(u4)

flo_guess = "PER, VER, LEC, HAM, SAI, ALO, NOR, RUS, ALB, SAR, OCO, MAG, GAS, STR, HUL, PIA, BOT, ZHO, TSU, DEV"
sof_guess = "VER, PER, SAI, ALO, NOR, LEC, HAM, ALB, OCO, RUS, HUL, STR, GAS, PIA, MAG, BOT, TSU, SAR, DEV, ZHO"
luk_guess = "VER, PER, ALO, SAI, HAM, LEC, ALB, RUS, STR, NOR, OCO, SAR, PIA, GAS, HUL, ZHO, BOT, DEV, TSU, MAG"
abi_guess = "VER, PER, ALO, HAM, SAI, LEC, RUS, STR, OCO, NOR, GAS, HUL, ALB, PIA, BOT, ZHO, TSU, MAG, SAR, DEV"

u1.set_guess(10, flo_guess)
u2.set_guess(10, sof_guess)
u3.set_guess(10, luk_guess)
u4.set_guess(10, abi_guess)
#calculate_points(comp.get_competitors(), 2023, 9)
calculate_points(comp.get_competitors(), 2023, 10)

get_leaderboard(comp)



#------ Frontend with streamlit
st.set_page_config(page_title='Formula 1 Race Predictions',page_icon = ':racing_car:', layout = "centered")
st.title('Formula 1 Race Predictions' + " " + ':racing_car:')

tabs = st.tabs(["Enter Guess", "View Leaderboard", "Manage Game"])

tabs_guess = tabs[0]

with tabs_guess:
    userstouse = comp.get_competitors_names()
    users = [""]
    for i in userstouse:
        users.append(i)
    gps = ["Austria", "Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
    drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'DEV']
    st.header(f"Enter your guess")
    with st.form("entry_form", clear_on_submit = True):
        user = st.selectbox("Select Person:", users)
        gp = st.selectbox("Select a Grand Prix:", gps)
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
                        print(gp_num)
                if user == ' ' or gp_num == 0:
                    st.write('Select a user and Grand Prix to enter a guess')
                else:
                    userComp = comp.get_competitor_by_name(user)
                    guess_concat = p1 + ", " + p2 + ", " + p3 + ", " + p4 + ", " + p5 + ", " + p6 + ", " + p7 + ", " + p8 + ", " + p9 + ", " + p10 + ", " + p11 + ", " + p12 + ", " + p13 + ", " + p14 + ", " + p15 + ", " + p16 + ", " + p17 + ", " + p18 + ", " + p19 + ", " + p20
                    userComp.set_guess(gp_num, guess_concat)
                    print(userComp.get_guess(gp_num))
                    st.write("Guess Entered for " + user + " for the " + gp + " Grand Prix")

                
                ##
                #calculate_points(comp.get_competitors(), 2023, 9)


tabs_leaderboard = tabs[1]

with tabs_leaderboard:
    fig, ax = plt.subplots()
    
    for player in comp.get_competitors():
        points = player.get_total_points()
        st.write("Total points for " + player.get_name() + ": " + str(points))

        plt.barh(
            y=player.get_name(),
            width=points,
            edgecolor="black",
            fill=True
        )
    plt.xlabel("Points")
    plt.ylabel("Competitor")
    plt.grid(False)
    st.pyplot(fig)

tabs_manage = tabs[2]

with tabs_manage:
    competitor_name = st.text_input('Competitor Name', 'name')
    if st.button("Add Competitor"): 
        if competitor_name in comp.get_competitors_names():
            st.write("Sorry, this name is taken")
        else:
            comp.add_competitor(Competitor(competitor_name))
            st.write("Competitor Added")
            st.write(str(comp.get_competitors_names()))

#----Why does this button refesh the whole page? How to avoid this?
    
    
    




                
            
            







