import covid_tweets
import argparse

#enter path with quotes
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path",  required=True, help="path to Twitter json batch")
args = vars(ap.parse_args())

#====Instantiate twitter cnn_object==================
twitter_object = covid_tweets.Twitter_Batch(args["path"])

#====Process, remove retweets, make dataframe==========
no_retweets = twitter_object.process_json_to_frame()

#====Get the trending keywords===========
no_retweets_with_keywords = twitter_object.get_keywords(no_retweets, save_csv = "False", pickle="False")

#====Extract places using NER, this may take a while========
no_retweets_with_keywords_and_places = twitter_object.get_places(no_retweets_with_keywords, save_csv="False", pickle="False")

#====Make time series html plotly============
resampled_df = twitter_object.resample_time_keywords(no_retweets_with_keywords, resample_factor = '1T', save_csv="False", pickle="False")
twitter_object.plot_trends_to_html(resampled_df)

#====Make sunburst html plotly================
twitter_object.plot_sunburst(no_retweets_with_keywords, resample_factor = '5T')

print (30 * '-')
print ("   S E A R C H   Q U E R Y  D E M O")
print (30 * '-')
print ("1. Atlanta and ventilators, only")
print ("2. New Orleans and ventilators or masks")
print ("3. New York and hospitals or coughing")
print (30 * '-')

###########################
## Robust error handling ##
## only accept int       ##
###########################
## Wait for valid input in while...not ###
is_valid=0

while not is_valid :
        try :
                choice = int (input('Enter your choice [1-3] : ') )
                is_valid = 1 ## set it to 1 to validate input and to terminate the while..not loop
        except:
                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])

### Take action as per selected menu-option ###
if choice == 1:
        print ("Returning Atlanta-ventilator results...")
        twitter_object.search_covid_tweets(no_retweets_with_keywords_and_places, "Atlanta", "vent", "hospital", multi="False", save_csv="False", pickle="False")
elif choice == 2:
        print ("Returning New Orleans-ventilator or mask results...")
        twitter_object.search_covid_tweets(no_retweets_with_keywords_and_places, "New Orleans", "vent", "mask", multi="True", save_csv="False", pickle="False")
elif choice == 3:
        print ("Returning New York-hospitals or coughing results...")
        twitter_object.search_covid_tweets(no_retweets_with_keywords_and_places, "New York", "cough", "hospital", multi="False", save_csv="False", pickle="False")
else:
        print ("Invalid number. Try again...")
