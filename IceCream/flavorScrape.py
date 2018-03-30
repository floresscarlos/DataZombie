#Libraries
from bs4 import BeautifulSoup
import requests
import re
import numpy as np 
import time
import tweepy as tp

#credentials to login to twitter api
consumer_key = 'VQfmS5hrAqSXSLppv2NWaSYZu'
consumer_secret = 'W0rENwcoRVnqCSJsg2dhp1EobL7CMhzvxZCXiIVWNrZOlDAU8z'
access_token = '954192403753086976-VO6goAyw6FIYg1WkQVReBwDUnCW37lK'
access_secret = '7MIBgZDRIJisTMbFpsRvJJACT4TBYBI5v5VmoJHWgTZtl'

#Existing Flavors
existing_flavors = ['coconut','icecream']

def flavor_script():   
    while True:
        print ('............ Looking for flavors ............... \n ............................................... \n')
        #Pull Flavors
        menu_url  = requests.get("http://linkedin.cafebonappetit.com/cafe/urban-terrace/")
        menu_data = menu_url.text
        menu_soup = BeautifulSoup(menu_data, 'html.parser') 
        menu_soup_daypart = menu_soup.select_one('body > div > #page > #main > #primary > #content > #panel-daypart-menu-1')
        menu_soup_script = menu_soup_daypart.select_one('script')
        menu_items = menu_soup_script.text.split('"monotony":{}}')
        menu_items_icecream = list(filter(lambda x: re.findall('"station_id":"10167"',x), menu_items))
        flavors = list(map(lambda x: re.findall('"label":"(.*?)".*"station_id":"10167"',x), menu_items_icecream))

        #Remove hard coded flavors
        remove_list = [('butter pecan ice cream', 'butter pecan ice cream'), ('chocolate ice cream', 'chocolate ice cream'), ('vanilla ice cream', 'vanilla ice cream'), ('caramel sauce', 'caramel sauce'), ('vegan chocolate syrup', 'vegan chocolate syrup'), ('whipped cream', 'whipped cream')]
        main_list = np.setdiff1d(flavors,remove_list)

        #Create new Flavors
        new_flavors = []
        for i in main_list:
            new_flavors.append((str(i),str(i)))

        #Check if its the same existing flavor   
        global existing_flavors
        same_flavor = sorted(new_flavors) == sorted(existing_flavors)    

        if len(main_list) > 0:
            existing_flavors = new_flavors
#             print(existing_flavors)
            #Login to twitter account api
            auth = tp.OAuthHandler( consumer_key, consumer_secret )
            auth.set_access_token( access_token, access_secret )
            api = tp.API(auth)
            #Tweet
            yummy = 'New flavors are out! \n* ' + ' \n* '.join(main_list)
            api.update_status(yummy)
            print(yummy + '\n')
            print('............................................... \n We Just Tweeted! Lets check back tomorrow ... \n ............................................... \n')
            time.sleep(1200 * 60) #20 hours
        else:
            print('...............No new Flavors .................. \n \n')
            print('Current flavors:\n')
            print(existing_flavors)
            print ('\n')
            time.sleep(20 * 60) #20minutes

            
if __name__ == '__main__':
    flavor_script()
    