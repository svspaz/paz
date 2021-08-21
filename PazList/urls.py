
from django.contrib import admin
from django.urls import path
from mypage import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
   


    path('adminclick', views.adminclick_view),
    path('teacherclick', views.teacherclick_view),
    path('studentclick', views.studentclick_view),

    path('adminsignup', views.admin_signup_view),
    path('teachersignup', views.teacher_signup_view,name='teachersignup'),
    path('studentsignup', views.student_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='mypage/adminlogin.html')),
    path('teacherlogin', LoginView.as_view(template_name='mypage/teacherlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='mypage/studentlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='mypage/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('delete-teacher-from-school/<int:pk>', views.delete_teacher_from_school_view,name='delete-teacher-from-school'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,name='admin-add-teacher'),
    path('admin-approve-teacher', views.admin_approve_teacher_view,name='admin-approve-teacher'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),
    
    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('delete-student-from-school/<int:pk>', views.delete_student_from_school_view,name='delete-student-from-school'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('admin-add-student', views.admin_add_student_view,name='admin-add-student'),

    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]



urlpatterns +=[
    path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),

    path('teacher-student', views.teacher_student_view,name='teacher-student'),
    path('teacher-view-student', views.teacher_view_student_view,name='teacher-view-student'),
    path('teacher-appointment', views.teacher_appointment_view,name='teacher-appointment'),
    path('teacher-view-appointment', views.teacher_view_appointment_view,name='teacher-view-appointment'),
    path('teacher-delete-appointment',views.teacher_delete_appointment_view,name='teacher-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]




urlpatterns +=[

    path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
    path('student-appointment', views.student_appointment_view,name='student-appointment'),
    path('student-book-appointment', views.student_book_appointment_view,name='student-book-appointment'),
    path('student-view-appointment', views.student_view_appointment_view,name='student-view-appointment'),
   

]

