# COVID19-TWITTER NLP

<h1>Version 1.0</h1>

Paper analyzing tweets from March 24 to April 8th: 
- Exploratory Data Analysis including extracting keywords using regular expressions
- Topic Modeling using LDA with coherence values
- UMAP visualization of topics using the Hellinger metric and a 2-dim embedding 

<img src=./plots/UMAP_1M_Apr162020.png></img>

<h1>Version 1.5</h1>

- Network analysis using the Tweets, User, and Entities object 

Target journal: TBD


<h1>Version 2.0</h1>
- Network analysis of medical rumors
- Definition or rumors
- Concept

Target journal: SBD-BRIMS Challenge Competition, May 117, 2020

Overleaf draft: https://www.overleaf.com/project/5e860dc79f5d7b0001bcfee0


<h1>Simple Data Pull and Plots</h1>
To pull data into a simple set of HTMLs for time-series and a radial/sunburst plot, go to `demo` dir and run:

    $ python covid_tweets.py

This will generate dataframes having cleaned, processed, removed retweets, and using regular expressions from the `covid_bed_search.json` file. The preprocessing script is also routinely used across the notebooks.
