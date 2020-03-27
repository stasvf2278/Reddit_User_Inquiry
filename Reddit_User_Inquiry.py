
import requests, json, os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from PIL import Image

def main():

    print('Enter the directory to where you want the files saved.')
    directory = input()

    os.chdir(directory)                                                         ## Change directory here

    print('Enter name of Reddit user')
    name = input()                                                              ## Input user name

    r = requests.get("http://www.reddit.com/user/"+ name +"/comments/.json?limit=100", headers = {'User-agent': 'your bot 0.1'}) ##Get request from reddit

    if r.status_code == 200:                                                    ## Checks status code (200 means success)
        print("Code status: " + str(r.status_code))
        print('Plot Made')

        data = json.loads(r.text)

        ## Create lists to fill with Reddit data
        sub = []
        text = []

        for child in data['data']['children']:                                  ## Loop to fill sub and text lists with Reddit data
        ##    time = datetime.fromtimestamp(child['data']['created_utc'])
            sub.append(child['data']['subreddit'])
            text.append(child['data']['body'])

        dict = Counter(sorted(sub))                                             ##Counter() tallies the sub list occurences before converting sub into a dictionary

        ## Plotting the sub bar graph
        pos = np.arange(len(dict.keys()))
        width = 1.0
        ax = plt.axes()
        ax.set_xticklabels(dict.keys())
        plt.title('User: ' + name)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.bar(list(dict.keys()), dict.values(), color='B')
        plt.savefig(name+'_bargraph.png')

        ## WordCloud Script


        cloudSource = ''                                                        ## Creates empty string to fill with comment data

        for words in text:                                                      ## Loops through text list indices to fill cloudsource with index data (ie comment text)
            cloudSource = cloudSource + ' ' + words

        ## Creates WordCloud plot
        wordcloud = WordCloud().generate(cloudSource)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(name +'_wordcloud.png')

        ## Saves images as .png files
        bar = Image.open(name+'_bargraph.png')
        wc = Image.open(name +'_wordcloud.png')

        ## Loads .png files to .pdf file
        im1=bar.convert('RGB')
        im2=wc.convert('RGB')
        imagelist = [im2]
        im1.save(directory +'\\'+ name +'.pdf', save_all=True, append_images=imagelist) ## Change directory here

    else:                                                                       ## For when r.status_code != 200
        print("User not found")

name = 'main'

if name == 'main':
    main()