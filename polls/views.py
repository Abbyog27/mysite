from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from pymongo import MongoClient
import os 
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


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
    


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index")


# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]
    
class DetailView(generic.DetailView):
    ...

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))

