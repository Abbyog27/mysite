from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os 
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId

client = MongoClient(os.getenv('MONGO_URI'))
db = client['mysite']
print(db.list_collection_names())

db.polls_question.insert_one({
    'question_text': 'What is your favorite color?',
    'pub_date': datetime.now(),
})

db.polls_question.insert_one({
    'question_text': 'What ORM do we use from MongoDB?',
    'pub_date': datetime.now(),
})


print(db.polls_question.find_one())
# print('new polls question', db.polls_question.find_one({'_id'}))

def index(request):
    return HttpResponse("Hello, world. You're at the polls index")
