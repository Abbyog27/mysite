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


question_one = {
    'question_text': 'What is your favorite color?',
    'pub_date': datetime.now(),
}

question_two = {
    'question_text': 'What ORM do we use from MongoDB?',
    'pub_date': datetime.now(),
}
db.polls_question.insert_one(question_one)

db.polls_question.insert_one(question_two)


print(db.polls_question.find_one())
# print('new polls question', db.polls_question.find_one({'_id'}))

#TODO Search by question_text
def search_question_by_text(question_text):
    for question in db.polls_question.find_all():
        if question['question_text'] == question[question_text]:
            print(question_text)
            return question
            print("question not found")
            return None
            

#TODO Search a question by a certain text
def search_question_by_text(question_text):
    for question in db.polls_question.find_all():
        if question_text in question['question_text']:
            print('Found question')
            return question
            print("question not found")
            return None
            


#TODO Search all questions by one date
def search_question_by_date(pub_date):
    for question in db.polls_question.find():
        if question['pub_date'] == pub_date: 
            return question

#TODO Update a question (pub_date -> needs to be set to current date)
def update_question_date(question_id, new_pub_date):
    db.polls_question.update_one({"_id": ObjectId(question_id)}, {"$set": {"pub_date": new_pub_date}})
    print('Question has been updated')
    
#TODO Delete a question
def delete_question(question_id):
    db.polls_question.delete_one({"_id": ObjectId(question_id)})
    print('Question deleted')
    
def index(request):
    return HttpResponse("Hello, world. You're at the polls index")
