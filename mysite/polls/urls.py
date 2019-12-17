from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.PollsIndexView.as_view(), name='pollsview'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('testapi/', views.apitest),
    path('deleteapi/<int:question_id>/', views.deleteapi),
    path('userapi/<x>/', views.userapi)
]