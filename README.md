
<h1>Exploratory Analysis of Covid19 Tweets using Topic Modeling, UMAP, and DiGraphs</h1>

Jupyter Notebooks for the paper, <i>Ordun, Catherine, Sanjay Purushotham, and Edward Raff. "Exploratory analysis of covid-19 tweets using topic modeling, umap, and digraphs." arXiv preprint arXiv:2005.03082 (2020)</i>

https://arxiv.org/abs/2005.03082



<h2>Overview</h2>
Exploratory Analysis includes a variety of notebooks, some of which are unpolished and "scratch", meaning cells show raw work and unpolished code written for exploration. Recommend running each cell one at a time, for careful analysis.

Recommended directory structure:

    - covid-mv(home)  #my dir name for this repo: covid-mv
      - Notebooks     #all notebooks described below
      - plots         #figures for time series, umap, etc.
      - csv           #csv files of dataframes
      - models        #LDA topic models
      - split_jsons   #where to save .json files after splitting them per `json_parser`
      - data          #save .json files here after calling from `twitter_query` dir file `stream-query1.py`

To pull data from Twitter, you will need to first use: `twitter_query/stream-query1.py`. You need to go to Twitter and sign up for a personal (free) developer account and add your credentials to the script. For your own research purposes, you may want to customize the track terms, different from the terms used in our paper. Then simply run:

    $python stream-query1.py

In my experience, I would run this overnight for 12 or more hours.

<h2>Relevant Notebooks include:</h2>


- `/notebooks/EDA.ipynb` - EDA including preprocessing, keyword analysis, timeseries UTC conversion, and searching in dataframes
- `/notebooks/Parsing_Twitter.ipynb` - After splitting original .json file using `/notebooks/json_parser.ipynb`, this reads in a pandas dataframe and extracts metadata for the retweeting time analysis and network modeling.
- `/notebooks/Parsing_Twitter_March24_Prototype.ipynb` - Scratch notebook for March 24th .json to dataframe, exploring different metadata required for the retweeting time and network analysis.
- `/notebooks/Parsing_Twitter_March25.ipynb` - Cleaned up scratch notebook for March 25, 2020
- `/notebooks/Parsing_Twitter_March28.ipynb` - Cleaned up scratch notebook for March 28, 2020
- `/notebooks/Parsing_Twitter_March30.ipynb` - Cleaned up scratch notebook for March 30, 2020. You could use this same notebook to get another period of time from Twitter -> run it through .json parsing notebook and then run it through this notebook to explore. One thing I noticed was that Twitter .json will occasionally fail to parse the `user` column after pandas conversion because it reads it as a string dict instead of a dict. As a result, would recommend future versions to read straight in from .json.
- `/notebooks/Topic Model Whole Corpora.ipynb` - Topic modeling (LDA) for entire 5.5M corpora of no-retweets. "no_retweets" dataframe can be obtained by using `/notebooks/EDA.ipynb`. Out of 23.3 M tweets keyword analysis and topic modeling only uses 5.5M tweets that comprise no-retweets. Notebook includes assigining topics from 20-topic LDA model to all 5.5M tweets, in addition to all broken axes plots in addition to use of binary segmentation from `ruptures` package for changepoint detection. Note, for `ruptures` you'll see I also ran dynamic programming, windows-based, and PELT models for changepoint detection, that you can explore. Modeling packages used: `gensim`, `brokenaxes`, `ruptures`
- `/notebooks/Twitter Networks_Whole.ipynb` - Retweeting analysis notebook and network analysis. Combines data from the `Parsing_Twitter` notebooks for each of the dates. Modeling packages used: `networkx`
- `/notebooks/UMAP.ipynb`- Applies TF-IDF vectorization to no-retweets (5.5M) and randomly selects 1M for 2D-embedding for UMAP visualization. Modeling packages used: `umap-learn`, `scikit-learn`

<h3>Helper Notebooks:</h3>

- `/notebooks/json_parser.ipynb` - Check out my blog post at <a href="https://nudratic.ghost.io/2020/03/31/bash-versus-pandas-to-split-json/">splitting json</a> to understand the reasoning behind splitting up a very large 20GB+ .json file into smaller files in order to process it on a CPU. Alternatives include using the NVIDIA `cudf`, however I found it to fail upon loading in a .json. This is a pre-step before analyzing retweets and network modeling. You don't need all the metadata.
- `/notebooks/preprocess.ipynb` - Accompanying notebook that can be used alone instead of importing in  `preprocess.py`. In case you need to do some form of data preprocessing on Twitter ahead of time.
- `/notebooks/twitter_geo.ipynb` - No geolocation was done in this paper.
   But if interested, you can use this to parse some geocoords.
- `/notebooks/preprocess.py` - Notebooks for topic modeling and UMAP import this script I wrote to preprocess that includes removing terms less than 3 chars, keeping only Latin chars, removing punctuation, hashtags, "user", etc. You can continue to add to this for your purposes.

<h2>Example plots</h2>
<img src=./misc/umap.png></img>


<img src=./misc/topics.png></img>


<img src=./misc/network.png></img>

<img src=./misc/wh.png></img>

<img src=./misc/changepoint.png></img>

<h2>Contact</h2>

Catherine, cordun1@umbc.edu
Sanjay, psanjay@umbc.edu
Ed, edraff1@umbc.edu
