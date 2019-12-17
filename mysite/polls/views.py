from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .serializers import QuestionSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Choice, Question
from django.contrib.auth.models import User

def indexview(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'polls/index.html')
    else:
        form = UserCreationForm()
        return render(request, 'polls/register.html', {'form':form})

def logoutview(request):
    if request.user.is_authenticated:
        request.session.flush('userlogin')
        deauth(request)
        return render(request, 'polls/login.html')



class PollsIndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@api_view(['POST', 'GET'])
def apitest(request):
    if request.method == 'GET':
        q = Question.objects.all()
        c = Choice.objects.all()
        qserializer = QuestionSerializer(q, many=True)
        return Response(qserializer.data)

    if request.method == 'POST':
        postdata = QuestionSerializer(data=request.data)
        if postdata.is_valid():
            postdata.save()
            return Response(postdata.data)


@api_view(['DELETE'])
def deleteapi(request, question_id):
    if request.method == 'DELETE':
        data = Question.objects.get(id=question_id)
        data.delete()
        return HttpResponse('Deletion was successfull')

@api_view(['POST', 'GET'])
def userapi(request, x):
    q = User.objects.filter(username=x)
    qserializer = UserSerializer(q, many=True)
    return Response(qserializer.data)