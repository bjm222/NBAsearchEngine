#! -*-coding:utf-8-*-
#!/usr/bin/env python3
import sys
import re
import os
import subprocess
from general_nbaPlayerData import general_playerData, helper_function, career_playerData
import numpy as np
import matplotlib.pyplot as plt
import urllib.request

def main():
    menu = \
    "                                                            \n"\
    "============================================================\n"\
    "=                                                          =\n"\
    "=            Welcome to the NBA search engine              =\n"\
    "=                                                          =\n"\
    "============================================================\n"\
    "                                                            \n"\
    "  OPTIONS:                                                  \n"\
    "  1 = Get general statistics for a NBA player yearly        \n"\
    "  2 = Get career statistics for all NBA players             \n"\
    "  3 = Get similar players for a NBA player in playing style \n"\
    "  4 = Get league leaders statistics for one year            \n"\
    "  5 = Quit                                                  \n"\
    "                                                            \n"\
    "============================================================\n"

    while True:
        sys.stderr.write(menu)
        option = input("Enter Option: ")
        if option == "1":
            get_general_statistics_for_a_player()
        elif option == "2":
            get_career_statistics_for_all_players()
        elif option == "3":
            get_similar_playing_style_players()
        elif option == "4":
            get_leaders_statistics_one_year()
        elif option == "5":
            exit(0)
        else:
            sys.stderr.write("Invalid input\n")

def get_general_statistics_for_a_player():
    """
    Display the statistics for a given player thoughout all career years
    """
    helper = helper_function()
    url = ""
    # check the input name is valid or not(whether in the database)
    while True:
        fname = input("Enter the player first name: ")
        lname = input("Enter the player last name: ")
        url = helper.get_player_page_url(fname, lname)
        if (url != "Not Find"):
            break
        else:
            sys.stderr.write("Invalid input\n")

    gp = general_playerData()
    gp.get_player_data(url)
    print ("-----------------------------------------------------------")
    print ("The player's average statistics throughout all career years")
    print ("-----------------------------------------------------------")
    print ("Average Points from: ", gp.year[0], "to" , gp.year[-2])
    print (str(gp.points)[1:-1])
    
    
    t1 = np.zeros(len(gp.points)) 
    t2 = np.zeros(len(gp.points))
    for x in range(len(gp.points)):
        t1[x] = gp.year[x]
        t2[x] = gp.points[x]

    # plot points, rebounds, assists and steals
    plt.figure(1)
    plt.subplot(221)
    plt.plot(t1, t2, 'r')
    plt.plot(t1, t2, 'bo')
    plt.xlabel('recent years')
    plt.ylabel('average points')

    print ("Average Assist from: ", gp.year[0], "to" , gp.year[-2])
    print (str(gp.assist)[1:-1])
    
    t1 = np.zeros(len(gp.assist)) 
    t2 = np.zeros(len(gp.assist))
    for x in range(len(gp.assist)):
        t1[x] = gp.year[x]
        t2[x] = gp.assist[x]
        
    plt.subplot(222)
    plt.plot(t1, t2, 'r')
    plt.plot(t1, t2, 'bo')
    plt.xlabel('recent years')
    plt.ylabel('average assist')

    print ("Average Rebounds from: ", gp.year[0], "to" , gp.year[-2])
    print (str(gp.rebounds)[1:-1])
    

    t1 = np.zeros(len(gp.rebounds))  
    t2 = np.zeros(len(gp.rebounds))
    for x in range(len(gp.rebounds)):
        t1[x] = gp.year[x]
        t2[x] = gp.rebounds[x]

    plt.subplot(223)
    plt.plot(t1, t2, 'r')
    plt.plot(t1, t2, 'bo')
    plt.xlabel('recent years')
    plt.ylabel('average rebouds')
  
    print ("Average Steals from: ", gp.year[0], "to" , gp.year[-2])
    print (str(gp.steal)[1:-1])
    
    t1 = np.zeros(len(gp.steal))    
    t2 = np.zeros(len(gp.steal))
    for x in range(len(gp.steal)):
        t1[x] = gp.year[x]
        t2[x] = gp.steal[x]
        
    plt.subplot(224)
    plt.plot(t1, t2, 'r')
    plt.plot(t1, t2, 'bo')
    plt.xlabel('recent years')
    plt.ylabel('average steal')

    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
    plt.show()


def get_career_statistics_for_all_players():
    """
    Find and display all the players' career statistics for the given the last name initial
    """
    helper = helper_function()
    # we can uncomment the following line to get the url for all players
    # it costs several hours, so we get the players of specific first character of last name
    #url_list = helper.get_all_player_page_url()
    first_char_of_lname = input("Enter the initial of players' last name for search: ")
    url_list = helper.get_all_player_page_url_with_specific_lname(first_char_of_lname)

    for i in range(0, len(url_list)):
        gp = career_playerData()
        gp.get_player_data(url_list[i])
        print ("(We are displaying player", i + 1, "/", len(url_list), "data)")
        print ("Name:", '{0:7s}'.format(gp.fname), gp.lname)
        print ("Position:", str(gp.position)[1:-1])
        print ("Career Data:", "Points:", gp.cPoints, " Blocks:", gp.cBlock, " Steals:",
         gp.cSteal, " Assits:", gp.cAssist," Rebounds:", gp.cRebound, "\n")

    print ("(Finish displaying data!)", "\n")

def get_similar_playing_style_players():
    """ 
    Given the name of a player, find the top ten similar players in playing style
    PS: In order to save time, we specify the initial of the players' last name for comparison
    """
    helper = helper_function()
    url = ""
    # check the input name is valid or not(whether in the database)
    while True:
        fname = input("Enter the target player first name: ")
        lname = input("Enter the target player last name: ")
        url = helper.get_player_page_url(fname, lname)
        if (url != "Not Find"):
            break
        else:
            sys.stderr.write("Invalid input\n")

    gp = general_playerData()
    gp.get_player_data(url)

    # we can uncomment the following line to get the url for all players
    # it costs several hours, so we get the players of specific first character of last name
    #url_list = helper.get_all_player_page_url()
    first_char_of_lname = input("Enter the initial of players' last name for comparison: ")
    url_list = helper.get_all_player_page_url_with_specific_lname(first_char_of_lname)

    player_list = []
    for i in range(0, len(url_list)):
        cp = career_playerData()
        url = url_list[i]
        cp.get_player_data(url)
        name = cp.fname + " " + cp.lname
        sim = round(helper.consine_sim(gp, cp), 3)
        cp.similarity = sim
        player_list.append(cp)
        print ("(We are collecting player", i + 1, "/", len(url_list), "data)")

    print ("(Finish collecting data!)", "\n")

    # Sort the players according to the similarity
    player_list.sort(key = lambda x: x.similarity, reverse = True)
    print ("Top 10 similar players:")
    print ("Similarity      FirstName       LastName")
    for i in range(0, 10):
        cp = player_list[i]
        print ('{0:.3f}'.format(cp.similarity), "         ", '{0:15s}'.format(cp.fname), cp.lname)

def get_leaders_statistics_one_year():
    """
    Display the statistics for the leaders in each section for a specific year
    """
    year = 2000
    while True:
        year = input("Enter a year you want to check (From 2000 to 2017): ")
        #print (type(year))
        if (int(year) >= 2000 and int(year) <= 2017):
            break
        else:
            sys.stderr.write("Invalid input\n")

    print ("-------------------------------------------------------")
    print ("                    Leader Data")
    print ("-------------------------------------------------------")
    url = "http://www.foxsports.com/nba/stats?season=" + year
    url += "&category=SCORING&group=1&sort=3&time=0&pos=0&team=0&qual=1&sortOrder=0&opp=0"
    html = urllib.request.urlopen(url).read()
    html = html.decode('UTF-8')
    table = html[html.find('<tbody>'):html.find('</tbody>')]
    best_scorer = table.split('</tr>')[0]
    score = get_num(best_scorer.split('</td>')[4])
    
    best_scorer = best_scorer[best_scorer.find('<a'):best_scorer.find('</a>')]
    best_scorer = best_scorer[best_scorer.find('<span>'):best_scorer.find('</span>')]
    print ("The leader in scoring:", '{0:20s}'.format(best_scorer[6:]), "PPG:", score)

    url = "http://www.foxsports.com/nba/stats?season=" + year + "&category=REBOUNDING&group=1&time=0"
    html = urllib.request.urlopen(url).read()
    html = html.decode('UTF-8')
    table = html[html.find('<tbody>'):html.find('</tbody>')]
    best_rebounder = table.split('</tr>')[0]
   
    rebound = get_num(best_rebounder.split('</td>')[9])
    
    best_rebounder = best_rebounder[best_rebounder.find('<a'):best_rebounder.find('</a>')]
    best_rebounder = best_rebounder[best_rebounder.find('<span>'):best_rebounder.find('</span>')]
    print ("The leader in rebound:", '{0:20s}'.format(best_rebounder[6:]), "RPG:", rebound)

    url = "http://www.foxsports.com/nba/stats?season=" + year + "&category=ASSISTS&group=1&time=0"
    html = urllib.request.urlopen(url).read()
    html = html.decode('UTF-8')
    table = html[html.find('<tbody>'):html.find('</tbody>')]
    best_assister = table.split('</tr>')[0]
   
    assist = get_num(best_assister.split('</td>')[5])
    
    best_assister = best_assister[best_assister.find('<a'):best_assister.find('</a>')]
    best_assister = best_assister[best_assister.find('<span>'):best_assister.find('</span>')]
    print ("The leader in assist: ", '{0:20s}'.format(best_assister[6:]), "APG:", assist, "\n")


def get_num(x):
    return float(''.join(ele for ele in x if ele.isdigit() or ele == '.')) 

if __name__=='__main__':
    main()
    
