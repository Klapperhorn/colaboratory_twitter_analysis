import pandas as pd

def current_time():
    
    from datetime import datetime
    print("Current Time =", datetime.now().strftime("%H:%M:%S"))
    return

#https://github.com/rehanraza24/Twitter-Text-Sentiment-Analysis-/blob/main/Text%20Preprocessing%20using%20SPACY.ipynb


# Contaction to Expansion > can't TO can not ,you'll TO you will
contractions = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"i'd": "I had / I would",
"i'd've": "I would have",
"i'll": "I shall / I will",
"i'll've": "I shall have / I will have",
"i'm": "I am",
"i've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}


def cont_to_exp(x):
    if type(x) is str:
        for key in contractions:
            value = contractions[key]
            x = x.replace(key, value)
        return x
    else:
        return x


def TweetCleaner(text):
    import preprocessor as p
    import re
    text=" ".join([word for word in text.split() if word[0]!="@" if word[:4]!="http"])
    text=text.replace("&amp","&")
    text=text.lstrip("RT ")
    text=re.sub(r'https?://[^\s<>"]+|www\.[^\s<>"]+','', text) # remove websites
    
    # https://github.com/s/preprocessor
    text=p.clean(text)

    return text

def pureText(text):
    import re
    text=text.lower()
    text=cont_to_exp(text)
    text=re.sub('[^A-Z a-z 0-9äöüÄÖÜß]+','', text) # Remove all Punctiations or Special Charactors 
    return text


def Tokenize(text,nlp):
    
    import pandas as pd
    if type(text)!=str:
        return pd.Series([None,None, None])  
    
    NLP= nlp(text)
    
    tokens=[token.lemma_ for token in NLP if token.is_alpha==True]
    NoStopwords=[token.lemma_ for token in NLP if token.is_stop==False and token.is_alpha==True]
    modal_verb=[token.lemma_ for token in NLP if token.tag_=="MD"]
    
    return pd.Series([tokens,NoStopwords,modal_verb])   


def Sentiment(text,nlp):
    nlp.add_pipe('spacytextblob')
    doc = nlp(text)
    polarity=doc._.blob.polarity
    subjectivity=doc._.blob.subjectivity
    return pd.Series([polarity, subjectivity])

def langDetect(text):
    try:
        from langdetect import detect
        lang=detect(text)
    except:
        lang="no_language_features"
    return lang


def load_nlp(target_language="en"):
    import spacy
    
    if target_language=="en":
        #import spacy_transformers
        import en_core_web_sm
       # nlp = spacy.load("en_core_web_trf")
        nlp = spacy.load('en_core_web_sm')
        
    if target_language=="de":
        import de_core_news_sm
        spacy.cli.download("de_core_news_sm")
        nlp = spacy.load("de_core_news_sm")   
    return nlp
    
def roberta_sentiment(row, column="sentences",pipe=None):
    
    if pipe==None:
        pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", max_length=512, truncation=True)
    
    text = row[column]
    result = pipe(text)
    sentiment=[i["label"] for i in result][0]
    return sentiment

def NLP_Pipeline(df, language="en"):
    
    from tqdm import tqdm
    
    tqdm.pandas()
    nlp=load_nlp(language)    
    df["clean_text"]=df.text.apply(TweetCleaner)
    
    text_column="clean_text"
    df["pure_text"]=df[text_column].apply(pureText)
    
    print("cleaning done.")
    
    print("Token & Lemmatizing & stopword removal & modal_word.") 
    
    df[["Lemmata","NoStopwords","modal"]]=df[text_column].progress_apply(Tokenize, nlp=nlp)
    df["word_count"]=df[text_column].dropna().apply(lambda x: len(x.split()))
    return df





def WordlistFilter(Lemmata, by):
    x=False
    
    if type(Lemmata)!=list:
        Lemmata=Lemmata.split()
        
    # As soon as the function finds a Word from the word list, x turns to True
    if len(Lemmata)>0:
        for i in Lemmata:
            if type(i)==str:
                if i.lower() in by:
                    x= True
    return x
    
