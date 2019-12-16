from rest_framework import serializers
from .models import Question, Choice
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model =  Question
		fields = ('id', 'question_text', 'pub_date')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')