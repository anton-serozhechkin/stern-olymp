from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone_number',
                    'class_number', 'name_school',
                    'count', )
    list_filter = ('class_number__name', )
    search_fields = ('user__username', 'user__last_name', 'user__first_name', 'name_school')

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'answer', 'question', )
    search_fields = ('student', 'answer', 'question')
    
class AnswerAdmin(admin.ModelAdmin):
    #list_display = ('question', 'text')
    search_fields = ('text', )
    #list_editable = ('text', 'correct')
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'event', )
    search_fields = ('question', )

class CategoryEventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'slug', )
    prepopulated_fields = {'slug': ('title', )}

class EventAdmin(admin.ModelAdmin):
    list_filter = ('category', )
    search_fields = ('title', 'content', 'short_description', 'category__title', 'price')
    prepopulated_fields = {'slug': ('title', )}
    fieldsets = (
        ('Основные параметры', {
            'fields':(
                'title',
                'category',
                'content',
                'short_description',
                'main_image',
                'data_event',
                'price',
                'classes'
            )
        }),
        ('Дополнительные опции',
            {
            'classes': ('collapse', ),
            'fields': ('slug', 'data_created')
            }
            )
    )

class UserInEventAdmin(admin.ModelAdmin):
    list_filter = ('paid', 'event')
    search_fields = ('user__user__last_name', 'user__user__first_name', 'event__title')

class StartOlympAdmin(admin.ModelAdmin):
    list_filter = ('event__title', )
    search_fields = ('user__last_name', 'user__username', 'user__first_name', 'event__title')
        
admin.site.unregister(Group)
admin.site.register(CategoryEvent, CategoryEventAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(ClassNumber)
admin.site.register(Event, EventAdmin)
admin.site.register(UserInEvent, UserInEventAdmin)
admin.site.register(StartOlymp, StartOlympAdmin)
admin.site.register(Student, StudentAdmin)