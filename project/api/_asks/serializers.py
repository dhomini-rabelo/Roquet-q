from rest_framework import serializers
from asks.models import Question



class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = 'creator', 'text',