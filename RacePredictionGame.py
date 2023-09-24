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
TEAM_ORDER = ["Red Bull", "Red Bull", "Ferrari", "Ferrari", "Mercedes", "Mercedes", "Aston Martin", "Aston Martin", "Alpine", "Alpine", "McLaren", "McLaren", "Haas", "Haas", "Williams", "Williams", "Alfa Romeo", "Alfa Romeo", "Alpha Tauri", "Alpha Tauri","Alpha Tauri"]


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
            coll_points = np.zeros(21, dtype = int)
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
                for y in range(21):
                    if my_guess[i] == DRIVER_ORDER[y]:
                        coll_points[y] = int(points)
            
            print("Points for " + x + ": " + str(my_total))
            set_points_db(x, grand_prix, my_total)
            set_coll_points_db(x, grand_prix, points_driver_to_string(coll_points))


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

def set_guess_db(name, gp, guess):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses"]
    guessdb[gp-1] = guess
    db.update({"guesses": guessdb}, name)

def get_guess_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    guessdb = persondb["guesses"]
    return guessdb[gp-1]

#points for 1 race for 1 person
def set_points_db(name, gp, n):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points"]
    pointsdb[gp-1] = n
    db.update({"points" : pointsdb}, name)

#points for 1 race for 1 person
def get_points_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    pointsdb = persondb["points"]
    return pointsdb[gp-1]

def set_coll_points_db(name, gp, arr):
    persondb = comp.get_competitor_by_name(name)
    arrdb = persondb["pointsdriver"]
    arrdb[gp-1] = arr
    db.update({"pointsdriver": arrdb}, name)

def get_coll_points_db(name, gp):
    persondb = comp.get_competitor_by_name(name)
    arrdb = persondb["pointsdriver"]
    return arrdb[gp-1]



#------Classes--------

#competitor class for each user
#maybe get rid of this???
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
        return db.put({"key": person.get_name(), "points": np.array(person.get_points()).tolist(), "guesses": np.array(person.get_guesses()).tolist(), "pointsdriver": ["" for x in range(23)]})
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




#set_guess_db('Lindsey', 15, "VER, SAI, LEC, RUS, HAM, PER, GAS, ALO, NOR, PIA, OCO, ALB, STR, LAW, TSU, MAG, HUL, BOT, ZHO, SAR")

#calculate_points(comp.get_competitors_names(), 2023, 15)





#------ Frontend with streamlit ----------------------------

#Set up page and title
st.set_page_config(page_title='Formula 1 Race Predictions',page_icon = ':racing_car:', layout = "centered")
st.title('Formula 1 Race Predictions' + " " + ':racing_car:')

# Set Tabs
tabs = st.tabs(["Enter Guess", "Your Results", "View Leaderboard", "Add Competitor", "Race Stats", "Race Analysis"])





tabs_guess = tabs[0]

#---------Enter Guess Tab-------------------------------------
with tabs_guess:
    userstouse = comp.get_competitors_names()
    users = [""]
    for i in userstouse:
        users.append(i)
    gps = ["Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
    drivers = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'RIC',]
    driversRICTOLAW = ['VER', 'PER', 'LEC', 'SAI', 'HAM', 'RUS', 'ALO', 'STR', 'GAS', 'OCO', 'NOR', 'PIA', 'MAG', 'HUL', 'ALB', 'SAR', 'BOT', 'ZHO',  'TSU', 'LAW',]
    st.header(f"Enter your guess")
    with st.form("entry_form", clear_on_submit = True):
        user = st.selectbox("Select Competitor:", users)
        gp = st.selectbox("Select a Grand Prix:", gps)
        
       
        st.write("Drag and dop to reorder the drivers below (If no drivers are shown, please refresh page):")
        col1, col2 = st.columns([2,3])
        with col1:
            items = [
                {'header': 'Drivers', 'items': driversRICTOLAW}
                ]
            sorted_items = sort_items(driversRICTOLAW, direction = 'vertical')
        submitted = st.form_submit_button("Enter")
        if submitted:
                gp_num = 0
                for x in range(len(gps)):
                    if gp == gps[x]:
                        gp_num = x + (23-len(gps))
                if user == '' or gp_num == 0:
                    st.error('Select a user and Grand Prix to enter a guess')
                else:
                    guessList = []
                    
                    for v in range(20):
                        guessList.append(sorted_items[v])
                    ##guess_concat = p1 + ", " + p2 + ", " + p3 + ", " + p4 + ", " + p5 + ", " + p6 + ", " + p7 + ", " + p8 + ", " + p9 + ", " + p10 + ", " + p11 + ", " + p12 + ", " + p13 + ", " + p14 + ", " + p15 + ", " + p16 + ", " + p17 + ", " + p18 + ", " + p19 + ", " + p20
                    guess_concat = ', '.join(guessList)
                    #print(guess_concat)
                    set_guess_db(user, gp_num, guess_concat)
                    st.success("Guess Entered for " + user + " for the " + gp + " Grand Prix")




tabs_results = tabs[1]

#--------------- Your Results Tab--------------------
with tabs_results:
    st.header(f"View your Guess")
    with st.form("view_form", clear_on_submit = False):
        userstouse = comp.get_competitors_names()
        users = [""]
        for i in userstouse:
            users.append(i)
        gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        userSelect = st.selectbox("Select Competitor:", users)
        gpSelect = st.selectbox("Select a Grand Prix:", gps)
        submitted2 = st.form_submit_button("Enter")
        if submitted2:
                gp_num = 0
                for x in range(len(gps)):
                    if gpSelect == gps[x]:
                        gp_num = x + (23-len(gps))
                if userSelect == '' or gp_num == 0:
                    st.error('Select a user and Grand Prix to view a guess')
                elif get_guess_db(userSelect, gp_num) == None:
                    st.error('No guess has been entered for this Grand Prix')
                else:
                    #st.write('**Points: ' + str(get_points_db(userSelect, gp_num)) + '**')
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

    st.header(f"View your Race Points")
    with st.form("view2_form", clear_on_submit = False):
        userstouse = comp.get_competitors_names()
        users = [""]
        for i in userstouse:
            users.append(i)
        gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        userSelect = st.selectbox("Select Competitor:", users)
        gpSelect = st.selectbox("Select a Grand Prix:", gps)
        submitted2 = st.form_submit_button("Enter")
        if submitted2:
                gp_num = 0
                for x in range(len(gps)):
                    if gpSelect == gps[x]:
                        gp_num = x + (23-len(gps))
                if userSelect == '' or gp_num == 0:
                    st.error('Select a user and Grand Prix to view a guess')
                elif get_guess_db(userSelect, gp_num) == None or get_guess_db(userSelect, gp_num) == "":
                    st.error('No guess has been entered for this Grand Prix')
                elif get_points_db(userSelect, gp_num) == 0:
                    st.error('Sorry, points have not been calculated yet')
                else:
                    st.write('**Points: ' + str(get_points_db(userSelect, gp_num)) + '**')
                    st.write('**Points by Driver:**')
                    #col1, col2 = st.columns(2)
                    gs = get_coll_points_db(userSelect, gp_num)
                    gs = str_to_arr(gs)
                    #gs1 = gs[:10]
                    #gs2 = gs[-11:]
                    #tick = 0
                    #with col1:
                    #    for i in gs1:
                    #        st.write(DRIVER_ORDER[tick] + ': ' + str(i))
                    #        tick = tick + 1
                    #tick = 10
                    #with col2:
                    #    for i in gs2:
                    #        st.write(DRIVER_ORDER[tick] + ': ' + str(i))
                    #        tick = tick + 1
                    data = np.array([TEAM_ORDER, DRIVER_ORDER, gs])
                    data = data.transpose()
                    df = pd.DataFrame(
                        data,
                        columns=['Team', 'Driver', 'Points']
                    )
                    st.dataframe(
                        df,
                        hide_index=True,
                        height = 775
                    )

                    
    st.header(f"Race Trends")
    #st.write("coming soon!")
    with st.form("view3_form", clear_on_submit = False):
        userstouse = comp.get_competitors_names()
        users = [""]
        for i in userstouse:
            users.append(i)
        userSelect = st.selectbox("Select Competitor:", users)
        gps = ["Silverstone", "Hungary", "Spa", "Zandvoort", "Monza", "Singapore", "Japan", "Qatar", "USA", "Mexico", "Brazil", "Las Vegas", "Abu Dhabi"]
        submitted3 = st.form_submit_button("Enter")
        if submitted3:
            st.write("Loading")
            if userSelect == '':
                    st.error('Select a user to view a guess')
            else:
                data = np.array([TEAM_ORDER, DRIVER_ORDER])
                data = data.transpose()
                df = pd.DataFrame(
                    data,
                    columns=['Team', 'Driver']
                )
                arr = []
                xarr = [1,2,3,4,5,6,7,8,9,10,11,12,13]
                for i in range(10,23):
                    if get_points_db(userSelect, i) != 0:
                        ppd = get_coll_points_db(userSelect, i)
                        ppd = str_to_arr(ppd)
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
                        if driv == 'RIC':
                            color =  ff1.plotting.driver_color('DEV')
                        else:
                            color = ff1.plotting.driver_color(driv)
                        ax.plot(gps[:len(arr[ind])], arr[ind], label = driv, color = color,)
                    ax.legend(bbox_to_anchor=(1.0, 1.02))
                    plt.suptitle("Points for each driver")
                    
                    st.pyplot(fig)
                else:
                    st.error("Sorry, not enough data yet!")




tabs_leaderboard = tabs[2]

#------------ Leaderboard Tab ---------------------------------
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
                    st.error('Select a Grand Prix')
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

#------------Manage Game Tab-----------------------------------
with tabs_manage:
    competitor_name = st.text_input('Enter Competitor Name', '')
    if st.button("Add Competitor"): 
        if competitor_name in comp.get_competitors_names():
            st.error("Sorry, this name is taken")
        else:
            comp.add_competitor(Competitor(competitor_name))
            st.success("Competitor Added, Refresh Page to See Competitor")
            #st.write(str(comp.get_competitors_names()))




tabs_stats = tabs[4]

#------------- Race Stats Tab -----------------------------------
with tabs_stats:
    st.write("coming soon!")

    

tabs_analysis = tabs[5]

#------------ Race Analysis Tab ---------------------------------
with tabs_analysis:
    with st.expander("Spa Grand Prix Analysis"):
        image = Image.open('photos/fueladjustracepagebelgium.png')
        st.image(image)
        image2 = Image.open('photos/tirestratbelgium.png')
        st.image(image2, caption = 'Tire Strategy')
        image3 = Image.open('photos/PositionChanges2023Spa.png')
        st.image(image3, caption = 'Position Changes')

    




                
            
            







