from flask import Flask, render_template, request, url_for, flash, redirect
import tweepy
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import base64
import io

from twitter import *

app = Flask(__name__)
import monitor

@app.route('/')
def index():
    return redirect('/monitor/groups/')

