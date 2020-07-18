import pandas as pd
import time
import spacy
import timeit
import plotly.express as px
import plotly.graph_objects as go
import plotly
from plotly import version
print (version)
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import re

class Twitter_Batch(object):
    def __init__(self, twitter_batch_json):
        """
        Args:
            - twitter_batch_json is the path to a Twitter .json file
            - example: "query_03252020.json"
        """
        self.twitter_batch_json = twitter_batch_json



    def process_json_to_frame(self, save_csv = "False", pickle="True"):
        """
        Transforms Twitter json to pandas dataframe for text analysis.
        Currently not including 'geo', 'coord', and 'place' tags b/c upon analysis less than 0.03% of tweets include this data.
        Args:
            - save_csv set to False by default
            - pickle set to True by default; faster I/O than csv

        Returns dataframe called 'no_retweets' that has datetime field and does not contain any retweets.
        """
        #=====STEP 1 - Read in json and convert to pandas dataframe====#
        df = pd.read_json(self.twitter_batch_json, lines=True)
        df = df[['created_at', 'text']] #you could add additional fields here like 'geo', 'coord', 'place' from Twitter API

        #=====STEP 2 - Fill nans and drop tweets where there is no datetime====#
        #drop nans
        df.fillna(value=0, inplace=True)
        #Drop tweets where there is no datetime specified b/c we need to index against datetime
        df2 = df.loc[df['created_at'] !=0]

        #=====STEP 3 - Convert to datetime=============================#
        #need to convert to string first
        df2['created_at'] = df2['created_at'].astype(str)
        #map to create a datetime feature
        df2['datetime'] = df2['created_at'].map(lambda x: time.strftime('%Y-%m-%d %H:%M:%S+00:00', time.strptime(x,'%Y-%m-%d %H:%M:%S+00:00')))
        #pandas conversion to datetime variable
        df2['datetime'] = pd.to_datetime(df2['datetime'])

        #=====STEP 4 - Remove retweets through RegEx================#
        df2['rt'] = df2['text'].str.contains('RT', case=True, regex=True)
        #use no_retweets
        no_retweets = df2.loc[df2['rt'] == False]

        #save to csv - first save dateformat
        if save_csv == "True":
            no_retweets.to_csv('./saved/no_retweets.csv', date_format='%Y-%m-%d %H:%M:%S+00:00', index=False)
            print("Saved to csv file.")

        if pickle=="True":
            no_retweets.to_pickle('./saved/no_retweets.pickle')
            print("Saved to pickle file.")

        #NOTE TO USER: use below to read back in
        #no_retweets = pd.read_csv('no_retweets.csv', parse_dates=['datetime'])
        #no_retweets = pd.read_pickle('my_df.pickle')
        print("Finished processing to dataframe.")
        return no_retweets

    def get_keywords(self, df, save_csv = "False", pickle="True"):
        """
        Args:
            df - pandas df, no_retweets

        Use RegEx to extract keywords of interest from the covid dataframe.
        For information on how RegEx patterns are used, check out regex101.com
        Note: This is where you would add new key words. For phrases use spacy and see the def i_am()
        Returns dataframe with booleans for multiple columns of respective flags:
            example: no_retweets['bed'] = False for a single record

        If save_csv = "True", will save to csv file, default is 'True'
        """
        df['bed'] = df['text'].str.contains(r"(?i)bed+\w+", regex=True)
        df['hospital'] = df['text'].str.contains(r"(?i)hosp+\w+", regex=True)
        df['mask'] = df['text'].str.contains(r"(?i)mas+\w+", regex=True)
        df['icu'] = df['text'].str.contains("ICU", regex=False)
        df['help'] = df['text'].str.contains(r"(?i)help+\w+", regex=True)
        df['nurse'] = df['text'].str.contains(r"(?i)nurs+\w+", regex=True)
        df['doctors'] = df['text'].str.contains(r"(?i)doc+\w+", regex=True)
        df['vent'] = df['text'].str.contains(r"(?i)vent+\w+", regex=True)
        df['test_pos'] = df['text'].str.contains('tested pos', regex=False)
        df['serious_cond'] = df['text'].str.contains('serious cond', regex=False)
        df['exposure'] = df['text'].str.contains('exposure', regex=False)
        df['cough'] = df['text'].str.contains(r"(?i)cough+\w+", regex=True)
        df['fever'] = df['text'].str.contains(r"(?i)fever+\w+", regex=True)

        #save to csv
        if save_csv == "True":
            df.to_csv('./saved/no_retweets_with_keywords.csv', date_format='%Y-%m-%d %H:%M:%S+00:00', index=False)
            print("Saved to csv file.")

        if pickle == "True":
            df.to_pickle('./saved/no_retweets_with_keywords.pickle')
            print("Saved to pickle file.")

        #NOTE TO USER: use below to read back in
        #no_retweets_with_keywords = pd.read_csv('no_retweets_with_keywords.csv', parse_dates=['datetime'])
        #no_retweets_with_keywords = pd.read_pickle('no_retweets_with_keywords'.pickle')
        print("Extracted keywords successfully.")
        return df


    def get_places(self, df, save_csv="False", pickle="True"):
        """
        Args:
            df - pandas df, no_retweets_with_keywords

        Gets places from the text using spacy's NER library. This may take several minutes to run
        depending on the size of the json batch.

        Returns dataframe with a 'places' column that is itself a list.
        """

        nlp = spacy.load("en_core_web_sm")
        print("Please wait as the dataframe extracts places. This may take several minutes depending on the size of the json file.")

        def return_places(text):
            gpe = []
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == 'GPE':
                    gpe.append(ent.text)
            return gpe


        df['places'] = df['text'].map(lambda x: return_places(x))

        #save if needed for another analysis
        if save_csv=="True":
            df.to_csv('./saved/no_retweets_keywords_and_places.csv', date_format='%Y-%m-%d %H:%M:%S+00:00', index=False)
            print("Saved to csv file.")

        if pickle=="True":
            df.to_pickle('./saved/no_retweets_with_keywords_and_places.pickle')
            print("Saved to pickle file.")

        #NOTE TO USER: use below to read back in
        #no_retweets_with_keywords_and_places = pd.read_csv('no_retweets_with_keywords_and_places.csv', parse_dates=['datetime'])
        #no_retweets_with_keywords_and_places = pd.read_pickle('no_retweets_with_keywords_and_places.pickle')

        print("Extracted places succesfully.")
        return df

    def search_covid_tweets(self, df, place_input, flag_input1, flag_input2="none", multi="False", save_csv ="False", pickle="True"):
        """
        Args:
            place_input - type str, in quotes
            flag_input - type str, in quotes
            df - pandas df, no_retweets_with_keywords_and_places

            available flags:
            'bed'
            'hospital'
            'mask'
            'icu'
            'help'
            'nurse'
            'doctors'
            'vent'
            'test_pos'
            'serious_cond'
            'exposure'
            'places'
            'cough'
            'fever'

        A search query script that returns all texts associated with an identified place
        inferred from the tweet, with the datetime. Currently only allows a single or a double or condition,
        by a single location.

        example usage:
            new_orleans_vent = search_covid_tweets(main_df, "New Orleans", "vent", "mask", multi="True")

        return dataframe of the search query

        """
        locale = df.loc[df['places'].str.contains(place_input, regex=False)]
        if multi:
            by_flag = locale.loc[(df[flag_input1] ==True) | (df[flag_input2] ==True)]
            print(*by_flag['text'], sep = "\n")
        else:
            by_flag = locale.loc[df[flag_input1]== True]
            print(*by_flag['text'], sep = "\n")

        #save if needed for another analysis
        if save_csv=="True":
            by_flag.to_csv('./saved/search_results.csv', date_format='%Y-%m-%d %H:%M:%S+00:00', index=False)
            print("Saved to csv file.")

        if pickle=="True":
            by_flag.to_pickle('./saved/search_results.pickle')
            print("Saved to pickle file.")

        return by_flag


    def resample_time_keywords(self, df, resample_factor = '1T', save_csv="False", pickle="True"):
        """
        Args:
            df - pandas dataframe - no_retweets_with_keywords
            resample_factor - type str, options:
                '1T' - Every minute (default)
                '5T' - Every 5 minutes
                '10T' - Every 10 minutes
                'H' - Every hour
        """
        #convert false/true to 0, 1
        df[['bed','hospital', 'mask', 'icu', 'help', 'nurse', 'doctors', 'vent', 'test_pos', 'serious_cond', 'exposure', 'cough', 'fever']] *=1

        #resamples and calculates sum every 1 minutes
        datetime_index = pd.DatetimeIndex(df['datetime'].values)
        df2=df.set_index(datetime_index)
        df2.drop(['datetime'], axis=1)
        resampled_df= df2.resample(resample_factor, label='right').sum()

        #save if needed for another analysis
        if save_csv=="True":
            resampled_df.to_csv('./saved/resampled_tweets.csv', date_format='%Y-%m-%d %H:%M:%S+00:00', index=False)
            print("Saved to csv file.")

        if pickle=="True":
            resampled_df.to_pickle('./saved/resampled_tweets.pickle')
            print("Saved to pickle file.")

        return resampled_df

    def plot_trends_to_html(self, df):
        """
        Args:
            df - pandas Dataframe, resampled_df

        Returns time series plot with time slider for all twitter Mentions
        of keyword over batch of Twitter increments of time by the resampled factor.
        """

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['bed'], name="bed",
                                 line_color='deepskyblue'))

        fig.add_trace(go.Scatter(x=df.index, y=df['hospital'], name="hospital",
                                 line_color='dimgray'))

        fig.add_trace(go.Scatter(x=df.index, y=df['mask'], name="mask",
                                 line_color='forestgreen'))

        fig.add_trace(go.Scatter(x=df.index, y=df['icu'], name="ICU",
                                 line_color='fuchsia'))

        fig.add_trace(go.Scatter(x=df.index, y=df['help'], name="help",
                                 line_color='gainsboro'))

        fig.add_trace(go.Scatter(x=df.index, y=df['nurse'], name="nurse",
                                 line_color='gold'))

        fig.add_trace(go.Scatter(x=df.index, y=df['doctors'], name="doctors",
                                 line_color='green'))

        fig.add_trace(go.Scatter(x=df.index, y=df['vent'], name="ventilator",
                                 line_color='greenyellow'))

        fig.add_trace(go.Scatter(x=df.index, y=df['test_pos'], name="tested positive",
                                 line_color='honeydew'))

        fig.add_trace(go.Scatter(x=df.index, y=df['serious_cond'], name="serious condition",
                                 line_color='dodgerblue'))

        fig.add_trace(go.Scatter(x=df.index, y=df['exposure'], name="exposure",
                                 line_color='firebrick'))

        fig.add_trace(go.Scatter(x=df.index, y=df['cough'], name="cough",
                                 line_color='mediumblue'))

        fig.add_trace(go.Scatter(x=df.index, y=df['fever'], name="fever",
                                 line_color='plum'))

        fig.update_layout(title_text='Time Series with Rangeslider Sampled every Minute',
                          xaxis_rangeslider_visible=True)

        #outputs to html file
        fig.write_html("./plots/flags.html")
        print("Your time series plot is ready in html.")

    def plot_sunburst(self, df, resample_factor = '5T'):
        """
        Args:
            df - pandas dataframe - no_retweets_with_keywords
            resample_factor - type str, options:
                '1T' - Every minute (default)
                '5T' - Every 5 minutes
                '10T' - Every 10 minutes
                'H' - Every hour

        User note - sunburst is more intuitive and visualizes better when resample_factor is longer time.
        This function resamples the dataframe.

        Returns sunburst plot to visualize frequency of key word mentions, as a sum.

        """
        #datetime formatting indexing again
        #resamples and calculates sum every 1 minutes
        datetime_index = pd.DatetimeIndex(df['datetime'].values)
        df2=df.set_index(datetime_index)
        df2.drop(['datetime'], axis=1)
        #resamples
        df3 = df2.resample(resample_factor, label='right').sum()

        #melts into long form
        df_long = pd.melt(df3,
                  value_vars=['bed','hospital', 'mask', 'icu', 'help', 'nurse', 'doctors', 'vent', 'test_pos', 'serious_cond', 'exposure', 'cough', 'fever'])

        #plotly viz
        fig = px.bar_polar(df_long, r="value", theta="variable", color="value",
                       color_discrete_sequence= px.colors.sequential.Plasma_r,
                       title="Total Frequency of Covid Twitter Mentions")

        #outputs to html file
        fig.write_html("./plots/sunburst.html")
        print("Your sunburst plot is ready in html.")
