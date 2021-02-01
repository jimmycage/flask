import os
import requests
import boto3

from flask import Flask
from flask import render_template

# Astronomy Picture of the Day  &date=2017-07-04  would return a video
my_nasa_apod_url = 'https://api.nasa.gov/planetary/apod?api_key={my_api_key}'

app = Flask(__name__)

@app.route('/')
def home():
    r = requests.get(my_nasa_apod_url)
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
                           media_type=media_type,
                           media_url=media_url,
                           title_text=title_text,
                           copyright_text=copyright_text,
                           description_text=description_text)


if __name__ == '__main__':
    ssm = boto3.client('ssm', region_name='us-east-1')
    response = ssm.get_parameters(Names=['MY_NASA_API_KEY'],
                                  WithDecryption=True)
    nasa_api_key = response['Parameters'][0]['Value']
    my_nasa_apod_url = my_nasa_apod_url.format(my_api_key=nasa_api_key)
    app.run(host='0.0.0.0', debug=True)
