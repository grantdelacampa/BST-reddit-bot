import praw
import sys, os
import configparser
import sqlite3


# Load config file

cfg_file = configparser.SafeConfigParser()
cfg_file.read('config.cfg')
c_id = cfg_file.get('reddit', 'id')
c_secret = cfg_file.get('reddit', 'secret')
u_agent = cfg_file.get('reddit', 'agent')
u_name = cfg_file.get('reddit', 'username')
p_word = cfg_file.get('reddit', 'password')
bot_name = cfg_file.get('users', 'bot')
sub_name = cfg_file.get('subreddit', 'name')
db_name = cfg_file.get('database', 'db_name')


post_tags = ['FOR TRADE', 'FOR SALE', 'SOLD ITEM']

def main():

    #hit the praw api with user credentials
    reddit = praw.Reddit(client_id = c_id, client_secret = c_secret, user_agent = u_agent, username= u_name, password= p_word)
    #-------------------------------------------------------------------
    #       Database Access
    #-------------------------------------------------------------------
        
    subreddit = reddit.subreddit('FashionRepsBST')

    for template in subreddit.flair.templates:
        print(template)

    
if __name__ == "__main__":
    main()
