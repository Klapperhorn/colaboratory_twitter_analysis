# Aim of the project

Aim of this project is to allow analyzing a Twitter dataset with no or only little coding skills. For this reason the Google Colabs use Jupyter's iWidgets, such as sliders & drop down menus, to set parameters for the analysis. To guide the data analysis and motivate transparent note-keeping, this project follows the idea of "[computational narratives](http://archive.ipython.org/JupyterGrantNarrative-2015.pdf "computational narratives")" providing fields for user comments after each steps. As most of the project prepares and stores text data in a DataFrame for the analysis, it is possible with little adjustments, to also import other social media or text sources.

# Structure of the project

The project consists of two Google Colabs:

1.  **Twitter\_API\_dataset\_generation.ipynb** retrieves tweets to json files, using Twitter 2.0 API. To access the API a bearer token from twitter must be provided. In a next step, the nlp module tokenizes the text, removes stopwords, and analyzes the Tweet's sentiment using a roberta-based model from Huggingface. The data is then stored as pandas DataFrame in a second json file.
2.  **Twitter\_Analysis.ipynb** opens the json file and the analyst goes through different steps for the analysis. A filter, using likes, retweets, sentiment, or key-words allows to filter the tweets and continue working on a reduced subset. The notebook includes the analysis of text, counts, time-rows, user & hashtag networks, and images.

# How to use it?

The user saves the repository on Google drive and opens  the **.ipynb** files with Google Colabs (which eventually must be enabled first for google drive). To allow loading and storing data, the first cells of both notebooks define where on Google Drive the notebook is stored. This means, the user changes the text in red letters. If filled out correctly, the user can run the first cell of the notebook and then allow Google Colab access to Google Drive.

## Dataset generation:

1.  The second cell defines the search term, time range, and filename for the data. 
2.  In this cell, the user devindes the Bearer Token to access twitter by either copying it into the cell or giving the path to an external file. The code then checks if the API is available. Unfortunately, unpaid access for researchers is not possible anymore. This leads to **response code 403** (access not authorized).
3.  The user runs the next cells run the search, combine the retrieved data, and prepare the text data for the analysis. The last cell saves the file to json.

## Data Analysis:

1.  Again the user first fills out the correct directory to provide access to Google Drive (see above). And defines what file is to be loaded.
2.  The exploration begins with analyzing word clouds of hashtags or common words to provide an overview of the dataset.
3.  Next, the user adjusts the sliders to filter and store a subset of tweets if needed.
4.  The next few cells allow for descriptive statistics of tweet counts or likes.
5.  To better understand the use of hashtags or words, the context can be explored by showing a network of words and example sentences of these words.
6.  The image analysis first downloads all images of the loaded subset into a download folder. The next cell scrolls through this folder (using the slider), showing images with text, user and date.
7.  The next cells allow for timerow analysis of (first) counts and sentiment over time and next the most popular users, hashtags or words.
8.  The social network graph analysis by default only shows the largest graph. If more detailed analysis is needed, the user can export a gephi file.

# Development of this project

I prepared these notebooks for a workshop and later added the image function. If there is interest in this project, I might add further modules for analysis or fork this file to change the dataset generation to another social media platform or data source. Feel free to contact me if you are interested or need help in using this project.

You can refer to this project by:

Roßmann, M. (2023). Colaboratory Twitter Analysis. https://github.com/Klapperhorn/colaboratory_twitter_analysis