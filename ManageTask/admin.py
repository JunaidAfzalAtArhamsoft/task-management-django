from django.contrib import admin
from .models import Person, TaskList, Task


class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'date_joined', 'gender']
    fieldsets = (
        ('Information', {'fields': ('first_name', 'last_name', 'username',
                                    'password', 'email', 'date_joined', 'gender')
                         }
         ),
    )


admin.site.register(Person, PersonAdmin)
admin.site.register(TaskList)
admin.site.register(Task)
