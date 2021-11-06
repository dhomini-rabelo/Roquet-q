from rest_framework import serializers
from asks.models import Question
from room.models import Room, Theme




class QuestionSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Question
        fields = 'creator', 'text', 'theme'
        
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = 'id', 'creator', 'text', 'theme', 'up_votes', 'down_votes', 'creation', 'answered',