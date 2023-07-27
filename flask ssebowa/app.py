subscription_key = "6c8086f863064921a6fd641e8ae1d3e7"
assert subscription_key
import os

#from PIL import Image, ImageTk
#import cv2,numpy
import os
 
#import requests

#print(googletrans.LANGUAGES)
#from googletrans import Translator
#translator = Translator()

#import requests


global text,simage,svideo

headers = {"Ocp-Apim-Subscription-Key": subscription_key}

from flask import Flask, render_template, request

import os




# Create flask instance
app = Flask(__name__)



def get_newses(search_term):
      search_url = "https://api.bing.microsoft.com/v7.0/news/search"
      news=[]
      params = {"q": search_term,"count":50, "textDecorations": True, "textFormat": "HTML"}
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()
      
      for result in search_results["value"]:
            
            news.append((result["name"],result['url'],result['description']))
      return news






def get_search(search_term,lang):
      search_url = "https://api.bing.microsoft.com/v7.0/search"
      global text,simage,svideo
      text=[]
      simage=[]
      svideo=[]
      params = {"q": search_term,"count":100, "textDecorations": True, "textFormat": "HTML"}
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()

      
      for result in search_results['webPages']['value']:
            if lang != 'en':
               t = translator.translate(result["name"],dest=lang).text

            else:
                t = result["name"]  
            try:
               
               text.append((t,result['url'],result['snippet'],result["thumbnailUrl"]))
            except:
               text.append((t,result['url'],result['snippet'],"https://store.ssebowa.org/static/img/logo.png"))
            
            
      try:
             for result in search_results['images']['value']:
                   
                   simage.append((result['thumbnailUrl'],result['hostPageUrl']))
      except:
            simage=[]

      try:
             for result in search_results['videos']['value']:
                   
                   svideo.append((result['thumbnailUrl'],result['hostPageUrl']))
      except:
            svideo=[]
      return text,simage,svideo

def get_images(search_term):
      search_url = "https://api.bing.microsoft.com/v7.0/images/search"
      image=[]
      params = {"q": search_term,"count":50, "textDecorations": True, "textFormat": "HTML"}
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()
      
      for result in search_results["value"]:
            
            image.append((result["name"],result['thumbnailUrl'],result["contentUrl"],
                          result["hostPageUrl"]))
      return image


def get_videos(search_term):
      search_url = "https://api.bing.microsoft.com/v7.0/videos/search"
      video=[]
      params = {"q": search_term,"count":50, "textDecorations": True, "textFormat": "HTML"}
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()
      
      for result in search_results["value"]:
            
            video.append((result["name"],result['thumbnailUrl'],
                          result["hostPageUrl"]))
      return video





























global key

 
#this method for login page
@app.route("/", methods = ['GET','POST'])
def home():
     return render_template('index.html')

# this method for registration page
@app.route("/get_text", methods = ['GET','POST'])
def get_text():
            text = request.form.get('t')
            lang = 'en'#request.POST["l"]
            global key
            key = text
            text,simage,svideo = get_search(text,lang)
            return render_template("base_results.html",results=text[0:10],resultsimg=simage[0:4],
                                   resultvideo=svideo,keyword=key,active1="active")    
@app.route("/get_text_2", methods = ['GET','POST'])
def get_text_2():
            return render_template("base_results.html",results=text[10:20],resultsimg=simage[5:9],
                                   resultvideo=svideo,keyword=key,active2="active")
@app.route("/get_text_3", methods = ['GET','POST'])
def get_text_3():
            return render_template("base_results.html",results=text[20:30],resultsimg=simage[10:14],
                                   resultvideo=svideo,keyword=key,active3="active") 

@app.route("/get_text_4", methods = ['GET','POST'])
def get_text_4():
            return render_template("base_results.html",results=text[30:40],resultsimg=simage[15:19],
                                   resultvideo=svideo,keyword=key,active4="active")
@app.route("/get_text_5", methods = ['GET','POST'])
def get_text_5():
            return render_template("base_results.html",results=text[40:50],resultsimg=simage[19:23],
                                   resultvideo=svideo,keyword=key,active5="active")

@app.route("/get_video", methods = ['GET','POST'])          
def get_video():
            #text = request.POST["t"]

            video = get_videos(key)

            return render_template("showvideo.html",results=video,keyword=key)

@app.route("/get_img", methods = ['GET','POST'])          
def get_img():
            #text = request.POST["t"]

            image = get_images(key)

            return render_template("showimg.html",results=image,keyword=key)
@app.route("/get_news", methods = ['GET','POST'])
def get_news():
            #text = request.POST["t"]

            news = get_newses(key)

            return render_template("shownews.html",results=news,keyword=key)



BASE_URI = 'https://api.bing.microsoft.com/v7.0/images/visualsearch'
SUBSCRIPTION_KEY = "6c8086f863064921a6fd641e8ae1d3e7"
HEADERS = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY}
def get(file):

      try:
          response = requests.post(BASE_URI, headers=HEADERS, files=file)
          response.raise_for_status()
          obj=response.json()
          list=[]
          #print(obj["tags"][0]["actions"][2]['data']['value'])
          for data in (obj["tags"][0]["actions"][2]['data']['value']):
                
                list.append((data['name'],data['webSearchUrl'],data['thumbnailUrl']))
    
          return list 
          
      except:
  
          return render_template('index.html')          
          
@app.route("/visual", methods = ['GET','POST'])
def visual():
      file = request.files["f"]
      filename = file.filename
      file = Image.open(file)
      file = file.resize((512,512),Image.ANTIALIAS)
      file.save(filename)

      
      file1 = {'image' : ('myfile',open(filename, 'rb'))}
      response = get(file1)
      
      #print(response)
      return render_template('visual.html',results=response)

# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,port=7000) 
    
    
