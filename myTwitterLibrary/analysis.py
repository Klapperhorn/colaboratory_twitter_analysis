from xml.etree.ElementTree import PI
import pandas as pd

from datetime import datetime
Today=datetime.now().strftime('%Y-%m-%d')

directory="/content/drive/MyDrive/"

def convert_xlsx(x):
    ### To load XLSX files when lists are borken
    from json import loads
    if type(x)==str:
        if x[0]=="[":
            x=x.strip("[]").replace("'","").split(",")
            return x
    return x


def WordlistFilter(Lemmata, by):
    # Lemmata = Source List of words to filter
    # by = Rule List of words to filter for
    
    x=False
    
    if type(Lemmata)==str:
        Lemmata=Lemmata.split()
    
    if type(Lemmata)==list:
        
        if type(by[0])==str:
            by=[i.lower() for i in by]
        
        # As soon as the function finds a Word from the word list, x turns to True
        if len(Lemmata)>0:
            for i in Lemmata:
                if type(i)==str:
                    if i.lower() in by:
                        x= True
    return x



def save_df_excel(df,filename="filtered_dataset.xlsx",directory=directory):
    filename=directory+filename
    df.to_json(filename.replace("xlsx","json"))      
    print("data stored to: ", filename)
    df["created_at"] = df["created_at"].dt.tz_localize(None)
    df.to_excel(filename)
    return



def filter_df(df,save=False, n_tweets=10,start="2022-11-01",end="2023-01-20",like_count=30,
             replay_count=0,retweet_count=0,word_count=5, polarity=0,language="no filter",Wordfilter="",Userfilter="",PolarityFilter=False,directory=directory):
    df_f=df
    df_f=df_f[df_f['created_at'].dt.strftime('%Y-%m-%d') > start]
    df_f=df_f[df_f['created_at'].dt.strftime('%Y-%m-%d') < end]
    df_f=df_f[df_f.like_count>=like_count]
    
    if language!="no filter":
        df_f=df_f[df_f.language==language]
        
    #df_f=df_f.dropna()
        
    if Wordfilter!="":
        Wordfilter=Wordfilter.split(", ")
        print("Displey only results that contain: ", Wordfilter)
        
        df_f=df_f[(df_f.Lemmata.apply(WordlistFilter,by=Wordfilter)) | (df_f.hashtags.apply(WordlistFilter,by=Wordfilter))]
        
        #df_f=df_f[df_f.Lemmata.apply(WordlistFilter,by=Wordfilter)]
        
#        df_f=df_f.append(df_f[df_f.hashtags.apply(WordlistFilter,by=Wordfilter)])

    if Userfilter!="":
        Userfilter=Userfilter.split(", ") # Makes list of key words to filter for
        print("Displey only results from: ", Userfilter)
        df_f=df_f[df_f.username.apply(lambda x: x in Userfilter)]
        
    df_f=df_f[df_f.reply_count>=replay_count]
    df_f=df_f[df_f.retweet_count>=retweet_count]
    df_f=df_f[df_f.word_count>word_count]
    
    if PolarityFilter==True:
        df_f=df_f[(df_f.polarity>=polarity-0.2) & (df_f.polarity<=polarity+0.2)]

    
    print("Number of Tweets: ", len(df_f))
    
    
   
    if save==True:
        save_df_excel(df_f,filename="filtered_dataset.xlsx",directory=directory)
    
    
    print(f"{n_tweets} example Tweets: \n")
    pd.set_option('display.max_colwidth', None)
    df_f=df_f[["created_at",'username',"text","like_count",'hashtags']]#.head(n_tweets)
    display(df_f)
    
    return df_f



def make_wordcloud(flat_list,filename,Mostcommon=100):
    from collections import Counter
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    
    a_counter = Counter(flat_list)
    most_common = a_counter.most_common(Mostcommon)
    wordcloud=WordCloud(background_color="white", width=1200, height=1200).generate_from_frequencies(dict(most_common))
    
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(filename,dpi=300)
    plt.show()
    
    
def FindTweetByMediaKey(x, mediaKey="3_1250417374660100096"):

    if type(x)==list:
        for i in x:
            if mediaKey in i:
                return True
        
    return False


def Keyword_context(text,search_word="sustainable",context=(4,4)):
    next_word=""
    pos=0
    PreWords,AfterWords=context
    if type(text)!=list:
        list_of_words = text.split(" ")
    else:
        list_of_words=text
        
    list_of_words=[word.lower() for word in list_of_words]
    WordbeginLetters=6 # for better word sensitivity
    

    similars=list(set([word for word in list_of_words if word[:WordbeginLetters].lower()==search_word[:WordbeginLetters]]))
    if len(similars)==0:
        return

    else:
        similars=similars[0].lower() # strings

        pos=list_of_words.index(similars) #position in the text
      #   print(similars + ":   ")

        if pos+AfterWords+1<len(list_of_words):
            # next_word =" ".join(list_of_words[pos-PreWord : pos+AfterWords])
            next_word =" ".join(list_of_words[pos-PreWords : pos+AfterWords+1])
            print(next_word)

        else:
            next_word =" ".join(list_of_words[0: pos+AfterWords+1])
            print(next_word)

    return


def ImgDownload(c):
    import requests
    key=c["media_key"]
    url=c["url"]
    try:
        filename=key+"."+url.split(".")[-1]
    #print(filename)
        r = requests.get(url, allow_redirects=True)
    
        with open ("IMG_Download/"+filename, "wb") as f:
            f.write(r.content)
    except:
        print("error: ", url)
    
    return key,url

def mostCommon(df,column="hashtags",n=10):
    
    from collections import Counter

    hashtags=df[column].dropna().to_list()
    
    if type(hashtags[0])==list:
        h=[y.lower() for x in hashtags for y in x]
    else:
        h=hashtags
    
    a_counter = Counter(h)

    c = a_counter.most_common(n)
    

    hs=pd.DataFrame(c,columns=[column,"count"])
    ax=hs.set_index(column).plot.barh(figsize=(5,5*n*0.1))
    
    
    for p in ax.patches:
        ax.annotate(str(p.get_width()), (p.get_width() * 1.005, p.get_y() * 1.005))
    
    
    if column=="urls":
        [print(i[0]) for i in c]
    
    # For newer matplotlib versions:
    #ax.bar_label(ax.containers[0])
    
    return hs



def TweetsHist(df,name="polarity", resample="1D",start='2022-11-04',end='2023-01-20', normalize=False,label=False):

    TimeRow=df.set_index("created_at")
    if start!=False:
        TimeRow=TimeRow[TimeRow.index.strftime('%Y-%m-%d') > start]
    if end!=False:
        TimeRow=TimeRow[TimeRow.index.strftime('%Y-%m-%d') < end]
        
    if name!="count":
        TimeRow=TimeRow.resample(resample)[name].mean()  
        if normalize==True:
            TimeRow=TimeRow/TimeRow.max()   
    
        TimeRow.plot(figsize=(16,5), title=f"The mean {name} in {resample} over time.")
    

    if name=="count":
        if normalize==True:
            TimeRow=TimeRow/TimeRow.max()   
        TimeRow=TimeRow.resample(resample)["id"].count()
        TimeRow.plot(figsize=(16,5), title=f"Tweets per {resample}")
    
    if label!=False:
        import matplotlib.pyplot as plt
        plt.legend([label]);

    
    return TimeRow    

## User_Analyse Functions:

def most_popular_users(df, by_value='like_count',n=20,plot=True,DataName=False,aggFunk="sum",column="name"):
    
    if aggFunk=="sum":
        aggFunk=sum
    if aggFunk=="mean":
        from statistics import mean
        aggFunk=mean
            
    
    if by_value!="polarity" and by_value!="subjectivity" :
        Piv_table = pd.pivot_table(df, values=by_value, index=["username","name"],aggfunc=aggFunk)
    else:

        Piv_table = pd.pivot_table(df, values=by_value, index=["username","name"],aggfunc=aggFunk)


    if plot==True:
        import matplotlib.pyplot as plt
        MostLikedAuthors=Piv_table.sort_values(by_value, ascending=False)[:n]
        MostLikedAuthors.reset_index(level=[column]).plot.barh(title=f'Most popular {n} users on Twitter by {by_value}',figsize=(5,5*n*0.1))
        if DataName!=False:
            plt.savefig(Today+DataName+"MostLiked_"+str(n)+"_Authors-Barh.pdf",dpi=300,bbox_inches="tight")
        plt.show()
    
    return MostLikedAuthors
    
    

    
def userTimeseries(df,name="username",n=10,resample="Q",DataName=False,start="2023-01-01",end="2023-01-20",stacked=True):
    df=df[df['created_at'].dt.strftime('%Y-%m-%d') > start]
    df=df[df['created_at'].dt.strftime('%Y-%m-%d') < end]
    
    if name=="hashtags" or name=="NoStopwords":
        df[name]=df[name].dropna().apply(lambda x: [word.lower() for word in x])
        df=df.explode(name).reset_index(drop=True)

    MostCommonAuthors=df[name].value_counts()[:n+1].index.tolist()
    SelektionsAutoren=df[df[name].isin(MostCommonAuthors)]
    TimeRow=SelektionsAutoren.set_index("created_at").groupby(name).resample(resample).size()

    TimeRow2=TimeRow.reset_index().set_index("created_at").pivot(columns=[name])[0]

    TimeRow2.plot.area(figsize=(16,5), stacked=stacked, title=f"{n} most active Twitter autors (per {resample})")
    
    if DataName!=False:
        import matplotlib.pyplot as plt
        plt.savefig(Today+"_"+DataName+"_"+'hist.pdf', dpi=300,bbox_inches="tight")


def NetworkGen(df):
    import networkx as nx
    import re
    G=nx.DiGraph()

    for i in df.index:
        source=df.username[i]
        mentions=df.mentions[i]
        #attributes
        tweetID=df["id"][i]
        
        if len(mentions)>0:
            
            for target in mentions:
                #print(source,target)
                
                source=re.sub(r'\W+', '', source) ## To avoid pyview errors.
                target=re.sub(r'\W+', '', target) ## To avoid pyview errors.
                G.add_edge(source,target,TweetID=str(tweetID))
                
        ## Attributes:
                
    return G 



def Word_NetworkGen(df,n=5,column="NoStopwords"):

    TweetWords=df[column].dropna().to_list()
    from itertools import combinations
    Tupples=[combinations(words, 2) for words in TweetWords if len(TweetWords)>1] 
    flatTuppleList=[y for x in Tupples for y in x]
    
    from collections import Counter
    a_counter = Counter(flatTuppleList)
    c = a_counter.most_common(n)
    
    print(c[:5])
    
    #c=[i[0] for i in c]
    
    import networkx as nx
    import re
    G=nx.Graph()
    
    for i in c:
        source=i[0][0]
        target=i[0][1]
        G.add_edge(source,target,count=str(i[1]))
    
    return G

    
def CleanGraph(G,removeIsolates=True,minDegree=20,only_largest_component=True):
    print(f"Cleaning Graph to minimum Degree {minDegree}.")
    import networkx as nx
    remove = [node for node,degree in dict(G.degree()).items() if degree <minDegree]
    
    G.remove_nodes_from(remove)
    
    if removeIsolates==True:
        G.remove_nodes_from(list(nx.isolates(G)))
        
    if only_largest_component==True:
        G=G.to_undirected()
        components = nx.connected_components(G)
        if G.size()>0:
            largest_component = max(components, key=len)
            G = G.subgraph(largest_component)
        
    print("Nodes count: ", len(G.nodes))
    print("Edges count: ", len(G.edges))
    return G



def PyVisGraph(G):
    
    from pyvis.network import Network
    net=Network(notebook=True,directed =True)
    net.from_nx(G)
    
    
    
    return net.show("network.html")



def writeNetworkHTML(G,filename="test.html",view=True):
    import networkx as nx
    if len(G.nodes)>60:
        print("sorry, but this graph is to big for an online analysis. Please export a gefx and try with gephi")
        return
    
    
    ## This function was necessary as the pyvis thing did not work in Colab
    
    folder=directory.split("content/")[1]
    filename=folder+"The_network.html"
    
    EdgesText=", ".join(["{ from: '"+str(i[0]) + "', to: '" + str(i[1]) +"' }" for i in G.edges])
    NodesText=", ".join(["{ id: '"+str(i)+ "', label: '"+str(i)+ "'}" for i in G.nodes])


    HTMLframe="""<!DOCTYPE html>
    <html lang="en">
      <head>
        <title>Network</title>
        <style type="text/css">
          #mynetwork_1 {
            width: 600px;
            height: 400px;
            border: 1px solid lightgray;
          }
        </style>
      </head>
      <body>
        <div id="mynetwork_1"></div>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <script type="text/javascript">

          // create an array with nodes
          var nodes = new vis.DataSet([""" + NodesText +  """
          ]);

          // create an array with edges
          var edges = new vis.DataSet(["""  + EdgesText + """
          ]);
          // create a network
          var container = document.getElementById("mynetwork_1");
          var data = {
            nodes: nodes,
            edges: edges,
          };
          var options = {};
          var network = new vis.Network(container, data, options);

        </script>
      </body>
    </html>"""
    
    
    with open(filename,"w") as f:
        f.write(HTMLframe)
        
    if view==True:    
        from IPython.display import HTML, display
        display(HTML(filename=filename))