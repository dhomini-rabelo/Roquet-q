from rest_framework.fields import empty
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


############################################################################################

class ThemeSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Theme
        fields = 'name', 'creator', 'questions',

        
class DataRoomSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)
    all_questions = serializers.IntegerField(default=0)
    
    class Meta:
        model = Room
        fields = 'creator', 'visits', 'all_questions', 'themes', 
        
        