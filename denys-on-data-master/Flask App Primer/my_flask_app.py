import os
import requests

from flask import Flask
from flask import render_template

my_nasa_api_link = 'https://api.nasa.gov/planetary/apod?api_key=' + os.getenv('MY_API_KEY') 

app = Flask(__name__)

@app.route('/')
def index_page():
    r = requests.get(my_nasa_api_link)
    response = r.json()
    
    copyright_text = 'Image Credits: '
    if 'copyright' in response:
        copyright_text += response['copyright']
    else:
        copyright_text += 'Public Domain'
    
    description_text = response.get('explanation', 'No description')
    title_text = response.get('title', 'No title')

    media_type = response['media_type']
    media_url = response['url']
    
    return render_template('index.html',
        copyright_text=copyright_text,
        description_text=description_text,
        title_text=title_text,
        media_type=media_type,
        media_url=media_url)
    
if __name__ == '__main__':
    app.run()