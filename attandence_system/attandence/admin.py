from django.contrib import admin
from .models import Employee, Attendance


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'fine')  

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'time', 'day', 'status')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
