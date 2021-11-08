from django.contrib import admin
from .models import Question, UsedKeys, UserKey, AdminKey


#* ACTIONS

@admin.action(description='Marcar perguntas selecionadas como respondidas')
def mark_selected_questions_as_answered(admin_model, request, query_set):
    query_set.update(answered=True)


#* ADMIN SETTINGS

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = 'room', 'theme', 'creator', 'get_text', 'score', 'answered',
    list_display_links = 'creator',
    list_per_page = 40
    empty_value_display = '[ NONE ]'
    actions = mark_selected_questions_as_answered,
    
    @admin.display(description='Sala')
    def room(self, question):
        return str(question.theme.room.code)
    
    @admin.display(description='question')
    def get_text(self, question):
        text_of_question = question.text
        if len(text_of_question) >= 61: 
            return text_of_question[:62] + '...'
        else:
            return text_of_question
        
    @admin.display
    def score(self, question):
        return str(question.up_votes - question.down_votes)
    
    

@admin.register(UserKey)
class UserKeyAdmin(admin.ModelAdmin):   
    list_display = 'key', 'room',
    list_display_links = 'key',
    list_per_page = 80  
    
    
         
@admin.register(AdminKey)
class AdminKeyAdmin(admin.ModelAdmin):   
    list_display = 'key', 'room',
    list_display_links = 'key',
    list_per_page = 80      
    
    
     
@admin.register(UsedKeys)
class UsedKeysAdmin(admin.ModelAdmin):   
    list_display = 'room', 'question',
    list_display_links = 'question',
    list_per_page = 80  
       
    @admin.display(description='Sala')
    def room(self, obj):
        return str(obj.question.theme.room.code)       

