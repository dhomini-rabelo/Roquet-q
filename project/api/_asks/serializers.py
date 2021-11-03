from rest_framework import serializers
from asks.models import Question
from room.models import Room, Theme




class QuestionSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Question
        fields = 'creator', 'text', 'theme'
        