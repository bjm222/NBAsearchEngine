#! -*-coding:utf-8-*-
#!/usr/bin/env python3

import urllib.request, urllib.error
from abc import ABCMeta, abstractmethod
import math

class general_playerData:
    """
    This class is used for collecting one player's general statistics up to now
    """
    def __init__(self):
        # Initialize the global data for storing the player's statistics
        # instance variable
        self.points = []
        self.fouls = []
        self.rebounds = []
        self.steal = []
        self.assist = []
        self.block = []
        self.turnOver = []
        self.year = []

        self.cPoints = 0
        self.cFoul = 0
        self.cRebound = 0
        self.cSteal = 0
        self.cAssist = 0
        self.cBlock = 0
        self.cTurnOver = 0
        self.lname = ""
        self.fname = ""
        self.position = []
 
    def get_player_data(self, url):
        # Give the url of the player's web page, extract the general statistics
        try:
            request = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # not find
                print ("Not Find")
        else:
            html = request.read().decode('UTF-8')
            table = html[html.find('<tbody>'):html.find('</tbody>')]
            performance_perYear = table.split('</tr>')

            playerInfo = html[html.find('http://schema.org/Person'):html.find('birthDate')]
            playerName = playerInfo.split('</h1>')[0].split(" ")
   
            self.lname = playerName[-1]
            self.fname = playerName[-2]
            self.fname = self.fname[self.fname.find('>')+1:]
            if "Point Guard" in playerInfo:
                self.position.append(1)
            if "Shooting Guard" in playerInfo:
                self.position.append(2)
            if "Small Forward" in playerInfo:
                self.position.append(3)
            if "Power Forward" in playerInfo:
                self.position.append(4)
            if "Center" in playerInfo:
                self.position.append(5)

            career = html[html.find('<tfoot>'):html.find('</tfoot>')]
            career = career[career.find('<tr >'):career.find('</tr>')]
            careerData = career.split('</td>')

            self.cPoints = self.get_num(careerData[-2])
            self.cFoul = self.get_num(careerData[-3])
            self.cRebound = self.get_num(careerData[-8])
            self.cSteal = self.get_num(careerData[-6])
            self.cAssist = self.get_num(careerData[-7])
            self.cBlock = self.get_num(careerData[-5])
            self.cTurnOver = self.get_num(careerData[-4])

            for i in range(0,len(performance_perYear)):
                player_data = performance_perYear[i].split('</td>')
                flag = 0
                for j in range(0, len(player_data)):
                    if "Did Not Play&nbsp" in player_data[j]:
                        flag = 1

                if flag == 0:
                    self.year.append(player_data[0].replace("<tbody>","")[18:22])
                    for j in range(22,len(player_data)):
                        if j==22:
                            self.rebounds.append(self.get_num(player_data[j]))
                        elif j ==28:
                            self.points.append(self.get_num(player_data[j]))
                        elif j ==27:
                            self.fouls.append(self.get_num(player_data[j]))
                        elif j ==26:
                            self.turnOver.append(self.get_num(player_data[j]))
                        elif j ==25:
                            self.block.append(self.get_num(player_data[j]))
                        elif j ==24:
                            self.steal.append(self.get_num(player_data[j]))
                        elif j ==23:
                            self.assist.append(self.get_num(player_data[j]))


    def get_num(self, x):
        # Extract the digit from a given string
        if any(char.isdigit() for char in x):
            return float(''.join(ele for ele in x if ele.isdigit() or ele == '.')) 
        else:
            return 0.0

class career_playerData:
    """
    This class is used for collecting one player's career statistics given the player's url
    """
    def __init__(self):
        # Initialize the global data for storing the player's statistics
        self.cPoints = 0
        self.cFoul = 0
        self.cRebound = 0
        self.cSteal = 0
        self.cAssist = 0
        self.cBlock = 0
        self.cTurnOver = 0
        self.lname = ""
        self.fname = ""
        self.position = []
        self.similarity = 0
 
    def get_player_data(self, url):
        # Give the url of the player's web page, extract the career statistics
        try:
            request = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # not find
                print ("Not Find")
        else:
            html = request.read().decode('UTF-8')
            table = html[html.find('<tbody>'):html.find('</tbody>')]
            performance_perYear = table.split('</tr>')

            playerInfo = html[html.find('http://schema.org/Person'):html.find('birthDate')]
            playerName = playerInfo.split('</h1>')[0].split(" ")
   
            self.lname = playerName[-1]
            self.fname = playerName[-2]
            self.fname = self.fname[self.fname.find('>')+1:]
            if "Point Guard" in playerInfo:
                self.position.append(1)
            if "Shooting Guard" in playerInfo:
                self.position.append(2)
            if "Small Forward" in playerInfo:
                self.position.append(3)
            if "Power Forward" in playerInfo:
                self.position.append(4)
            if "Center" in playerInfo:
                self.position.append(5)

            career = html[html.find('<tfoot>'):html.find('</tfoot>')]
            career = career[career.find('<tr >'):career.find('</tr>')]
            careerData = career.split('</td>')

            self.cPoints = self.get_num(careerData[-2])
            self.cFoul = self.get_num(careerData[-3])
            self.cRebound = self.get_num(careerData[-8])
            self.cSteal = self.get_num(careerData[-6])
            self.cAssist = self.get_num(careerData[-7])
            self.cBlock = self.get_num(careerData[-5])
            self.cTurnOver = self.get_num(careerData[-4])

    # Extract the digit from a given string
    def get_num(self, x):
        if any(char.isdigit() for char in x):
            return float(''.join(ele for ele in x if ele.isdigit() or ele == '.')) 
        else:
            return 0.0                                

class helper_function:
    """
    This is a class including helper functions as following:
    (1) Given the name of the player, return the url for its statistics page
    (2) Return urls of the statistics page for all players
    (3) Return urls of the statistics page for players with specified initial of last name
    (4) Helper function for finding the position of the nth sub string in the big string
    (5) Helper function for calculating the similarity value according to the cosine method
    """
    def __init__(self):
        # instance variable
        pass

    def get_player_page_url(self, first_name, last_name):
        # Given the name of the player, return the url for its statistics page
        base_url = "http://www.basketball-reference.com/players/"
        player_name = first_name + " " + last_name
        cur_url = base_url + last_name[0].lower() + "/"

        try:
            request = urllib.request.urlopen(cur_url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # not find
                return "Not Find"
        else:
            html = request.read().decode('UTF-8').lower()
            url_data = html[html.find('<tbody>') + 7 : html.find('</tbody>')]
            if player_name in url_data:
                each_url = url_data.split('</tr>')
                for j in range(0, len(each_url) - 1):
                    if player_name in each_url[j]:
                        if "<strong>" in each_url[j]:
                            player_url = each_url[j][self.find_nth(each_url[j], "<", 4):self.find_nth(each_url[j], ">", 4)]
                        else:
                            player_url = each_url[j][self.find_nth(each_url[j], "<", 3):self.find_nth(each_url[j], ">", 3)]
                        player_url = player_url[9:-1]
                        player_url = "http://www.basketball-reference.com" + player_url
                        #print (player_url)
                        return player_url
                    else:
                        continue

                # not find
                return "Not Find"

            # not find
            return "Not Find"

    def get_all_player_page_url(self):
        #Return urls of the statistics page for all players
        result = []
        base_url = "http://www.basketball-reference.com/players/"
        char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for i in range(0, 26):
            cur_url = base_url + char_list[i] + "/"

            try:
                request = urllib.request.urlopen(cur_url)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    continue
            else:
                html = request.read().decode('UTF-8')
                url_data = html[html.find('<tbody>') + 7:html.find('</tbody>')]
                each_url = url_data.split('</tr>')
                for j in range(0, len(each_url) - 1):
                    if "<strong>" in each_url[j]:
                        player_url = each_url[j][self.find_nth(each_url[j], "<", 4):self.find_nth(each_url[j], ">", 4)]
                    else:
                        player_url = each_url[j][self.find_nth(each_url[j], "<", 3):self.find_nth(each_url[j], ">", 3)]
                    player_url = player_url[9:-1]
                    player_url = "http://www.basketball-reference.com" + player_url
                    result.append(player_url)

        return result

    def get_all_player_page_url_with_specific_lname(self, lname_first_char):
        # Return urls of the statistics page for players with specified initial of last name
        result = []
        base_url = "http://www.basketball-reference.com/players/"
        cur_url = base_url + lname_first_char.lower() + "/"

        try:
            request = urllib.request.urlopen(cur_url)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # not find, return empty result list
                return result
        else:
            html = request.read().decode('UTF-8')
            url_data = html[html.find('<tbody>') + 7:html.find('</tbody>')]
            each_url = url_data.split('</tr>')
            for j in range(0, len(each_url) - 1):
                if "<strong>" in each_url[j]:
                    player_url = each_url[j][self.find_nth(each_url[j], "<", 4):self.find_nth(each_url[j], ">", 4)]
                else:
                    player_url = each_url[j][self.find_nth(each_url[j], "<", 3):self.find_nth(each_url[j], ">", 3)]
                player_url = player_url[9:-1]
                player_url = "http://www.basketball-reference.com" + player_url
                result.append(player_url)

        return result

    def find_nth(self, big_str, sub_str, n):
        # Helper function for finding the position of the nth sub_str in the big_str
        start = big_str.find(sub_str)
        while start >= 0 and n > 1:
            start = big_str.find(sub_str, start+len(sub_str))
            n -= 1
        return start

    def consine_sim(self, player_1, player_2):
        # Helper function for calculating the similarity value according to the cosine method
        # player data in the [points rebounds steals assists blocks] format
        player_1_data = [player_1.cPoints, player_1.cRebound, player_1.cSteal, player_1.cAssist, player_1.cBlock]
        player_2_data = [player_2.cPoints, player_2.cRebound, player_2.cSteal, player_2.cAssist, player_2.cBlock]
        result = 0.0
        numerator = 0.0
        denominator = 0.0
        for i in range(0, 5):
            numerator += player_1_data[i] * player_2_data[i]
        temp = 0.0
        for i in range(0, 5):
            temp += (player_1_data[i] * player_1_data[i])
        denominator += math.sqrt(temp)
        temp = 0.0
        for i in range(0, 5):
            temp += (player_2_data[i] * player_2_data[i])
        denominator *= math.sqrt(temp)
        result = numerator / denominator
        return result

