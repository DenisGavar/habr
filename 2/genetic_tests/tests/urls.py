from django.urls import path
from .views import GeneticTestListView, StatisticsView

urlpatterns = [
    path('tests', GeneticTestListView.as_view()),
    path('statistics', StatisticsView.as_view()),
]
