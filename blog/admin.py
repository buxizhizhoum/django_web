from django.contrib import admin
from blog.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Reply)
admin.site.register(Notes)
admin.site.register(NotesType)
admin.site.register(ChatContent)
