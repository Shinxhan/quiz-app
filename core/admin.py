from django.contrib import admin
from .models import Category, Quiz, Question, Option
class OptionInline(admin.TabularInline):
    model = Option
    extra = 2 # minimum 2 options
    max_num = 4
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)