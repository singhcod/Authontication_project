from django.contrib import admin
from .models import BookModel

# Register your models here.
@admin.register( BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','name','pages','price']
