import praw
import logging
import sys, os
import configparser
import sqlite3

#-------------------------------------------------------------------
#       Load Config File
#-------------------------------------------------------------------

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

comment_format = "Poster: {} \n \n" + "Verified Sale Count: {} \n \n" + "Moderator: <put mods to tag here>"
target_flair = ['FOR TRADE', 'FOR SALE']
#-------------------------------------------------------------------
#       Main
#-------------------------------------------------------------------

def main():

    #hit the praw api with user credentials
    reddit = praw.Reddit(client_id = c_id, client_secret = c_secret, user_agent = u_agent, username= u_name, password= p_word)

    subreddit = reddit.subreddit(sub_name)

    for submission in subreddit.stream.submissions(skip_existing=True):
        process_submission(submission)

#-------------------------------------------------------------------
#       Process submission through database
#-------------------------------------------------------------------
def process_submission(submission):
    if(submission.link_flair_text in target_flair):                                         #Find posts with REVIEW as their flair

        print("     - Post Found: ", submission.title)


        #-------------------------------------------------------------------
        #       Database Access
        #-------------------------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, db_name)

        conn = sqlite3.connect(db_path)                                                 #Establish database connection

        c = conn.cursor()                                                               # Create Cursor object


        #-------------------------------------------------------------------
        #       Database Querries
        #-------------------------------------------------------------------
        print("     - Esatblishing Connection to DB")

        c.execute('SELECT Approved_Karma FROM Karma WHERE user_name = ?', (submission.author.name,))

        found_karma = c.fetchone()

        if found_karma == None:                                                          # This User does not exist in the database so add them 
            c.execute('INSERT INTO Karma VALUES (?, ?)', (submission.author.name, 0))
            conn.commit()
            found_karma = 0                                                             # New user karma is 0

        conn.close()
        
        if type(found_karma) is int:
            submission.reply(comment_format.format(submission.author.name, found_karma))
        else:
            submission.reply(comment_format.format(submission.author.name, found_karma[0]))   # post reply message
    else:
        return



if __name__ == "__main__":
    main()
