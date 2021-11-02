from django.db.models.aggregates import Sum
from django.contrib import admin
from .models import Room, Theme



#* ACTIONS

@admin.action(description='Ativar temas selecionados')
def active_selected_themes(admin_model, request, query_set):
    query_set.update(active=True)


@admin.action(description='Desativar temas selecionados')
def disable_selected_themes(admin_model, request, query_set):
    query_set.update(active=False)


#* ADMIN SETTINGS 

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = 'get_room_code', 'name', 'creator', 'questions', 'active'
    list_display_links = 'name',
    list_filter = 'active', 'creator',
    list_per_page = 20
    empty_value_display = '[ NONE ]'    
    actions = disable_selected_themes, active_selected_themes, 
    
    @admin.display(description='Sala')
    def get_room_code(self, theme):
        return str(theme.room.code)
    
    @admin.display(description='Número de perguntas')
    def questions(self, theme):
        question_quantity = theme.questions.count()
        return str(question_quantity)
    



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = 'code', 'creator', 'get_themes', 'questions', 'visits'
    list_display_links = 'code',
    list_per_page = 20
    readonly_fields = 'password_admin',
    empty_value_display = '[ NONE ]'

    
    @admin.display(description='Temas')
    def get_themes(self, room):
        themes_name = ''
        themes = room.themes.all()
        
        for index, theme in enumerate(themes):
            themes_name += f', {theme.name}'
            if index == 3:
                break
        
        if len(themes) == 0:
            return '[ NONE ]'
        elif len(themes) <= 3:
            return themes_name[2:]
        else:
            return themes_name[2:] + f', ...({len(themes)-3})'
            
    @admin.display(description='Número de perguntas')
    def questions(self, room):
        question_quantity = 0
        themes = room.themes.all()
        for theme in themes:
            question_quantity += theme.questions.count()
        return str(question_quantity)
    
    