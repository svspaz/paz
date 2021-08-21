from django.contrib import admin
from .models import Teacher,Student,Appointment
# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teacher, TeacherAdmin)

class StudentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Student, StudentAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

