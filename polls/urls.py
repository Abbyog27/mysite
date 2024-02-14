from django.urls import include, path
from . import views  #right not, it has the index method



app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name= "index"), 
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('email/', views.send_email, name="email")
]

