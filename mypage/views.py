from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mypage/index.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mypage/adminclick.html')


def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mypage/teacherclick.html')



def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mypage/studentclick.html')




def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'mypage/adminsignup.html',{'form':form})




def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher=teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'mypage/teachersignup.html',context=mydict)


def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.assignedTeacherId=request.POST.get('assignedTeacherId')
            student=student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'mypage/studentsignup.html',context=mydict)






def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'mypage/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'mypage/student_wait_for_approval.html')








#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    teachers=models.Teacher.objects.all().order_by('-id')
    students=models.Student.objects.all().order_by('-id')
    #for three cards
    teachercount=models.Teacher.objects.all().filter(status=True).count()
    pendingteachercount=models.Teacher.objects.all().filter(status=False).count()

    studentcount=models.Student.objects.all().filter(status=True).count()
    

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'teachers':teachers,
    'students':students,
    'teachercount':teachercount,
    'pendingteachercount':pendingteachercount,
    'studentcount':studentcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'mypage/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'mypage/admin_teacher.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.Teacher.objects.all().filter(status=True)
    return render(request,'mypage/admin_view_teacher.html',{'teachers':teachers})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    userForm=forms.TeacherUserForm(instance=user)
    teacherForm=forms.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST,instance=user)
        teacherForm=forms.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.status=True
            teacher.save()
            return redirect('admin-view-teacher')
    return render(request,'mypage/admin_update_teacher.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.status=True
            teacher.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-teacher')
    return render(request,'mypage/admin_add_teacher.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    #those whose approval are needed
    teachers=models.Teacher.objects.all().filter(status=False)
    return render(request,'mypage/admin_approve_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_teacher_view(request,pk):
    teacher=models.Teacher.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'mypage/admin_student.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.Student.objects.all().filter(status=True)
    return render(request,'mypage/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)

    userForm=forms.StudentUserForm(instance=user)
    studentForm=forms.StudentForm(instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST,instance=user)
        studentForm=forms.StudentForm(request.POST,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.status=True
            student.assignedTeacherId=request.POST.get('assignedTeacherrId')
            student.save()
            return redirect('admin-view-student')
    return render(request,'mypage/admin_update_student.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            student=studentForm.save(commit=False)
            student.user=user
            student.status=True
            student.assignedTeacherId=request.POST.get('assignedTeacherId')
            student.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-student')
    return render(request,'mypage/admin_add_student.html',context=mydict)






#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'mypage/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'mypage/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.teacherId=request.POST.get('teacherId')
            appointment.studentId=request.POST.get('studentId')
            appointment.teacherName=models.User.objects.get(id=request.POST.get('teacherId')).first_name
            appointment.studentName=models.User.objects.get(id=request.POST.get('studentId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'mypage/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'mypage/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------







#---------------------------------------------------------------------------------
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    #for three cards
    studentcount=models.Student.objects.all().filter(status=True,assignedTeacherId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,teacherId=request.user.id).count()
    
    appointments=models.Appointment.objects.all().filter(status=True,teacherId=request.user.id).order_by('-id')
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid).order_by('-id')
    appointments=zip(appointments,students)
    mydict={
    'studentcount':studentcount,
    'appointmentcount':appointmentcount,
    'appointments':appointments,
    'teacher':models.Teacher.objects.get(user_id=request.user.id), 
    }
    return render(request,'mypage/teacher_dashboard.html',context=mydict)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_student_view(request):
    mydict={
    'teacher':models.Teacher.objects.get(user_id=request.user.id), 
    }
    return render(request,'mypage/teacher_student.html',context=mydict)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_student_view(request):
    students=models.Student.objects.all().filter(status=True,assignedTeacherId=request.user.id)
    teacher=models.Teacher.objects.get(user_id=request.user.id) 
    return render(request,'mypage/teacher_view_student.html',{'students':students,'teacher':teacher})






@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_appointment_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id) 
    return render(request,'mypage/teacher_appointment.html',{'teacher':teacher})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_appointment_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id) 
    appointments=models.Appointment.objects.all().filter(status=True,teacherId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'mypage/teacher_view_appointment.html',{'appointments':appointments,'teacher':teacher})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_delete_appointment_view(request):
    teacher=models.Teacher.objects.get(user_id=request.user.id) 
    appointments=models.Appointment.objects.all().filter(status=True,teacherId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'mypage/teacher_delete_appointment.html',{'appointments':appointments,'teacher':teacher})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    teacher=models.Teacher.objects.get(user_id=request.user.id) 
    appointments=models.Appointment.objects.all().filter(status=True,teacherId=request.user.id)
    studentid=[]
    for a in appointments:
        studentid.append(a.studentId)
    students=models.Student.objects.all().filter(status=True,user_id__in=studentid)
    appointments=zip(appointments,students)
    return render(request,'mypage/teacher_delete_appointment.html',{'appointments':appointments,'teacher':teacher})



#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    student=models.Student.objects.get(user_id=request.user.id)
    teacher=models.Teacher.objects.get(user_id=student.assignedTeacherId)
    mydict={
    'student':student,
    'teacherName':teacher.get_name,
    'teacherPosition':teacher.position,
    'violation':student.violation,
    'scheduleday':student.scheduleday,
    'hoursperday':student.hoursperday,
    'teacherDepartment':teacher.department,
    'admitDate':student.admitDate,
    }
    return render(request,'mypage/student_dashboard.html',context=mydict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_appointment_view(request):
    student=models.Student.objects.get(user_id=request.user.id) 
    return render(request,'mypage/student_appointment.html',{'student':student})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_book_appointment_view(request):
    appointmentForm=forms.StudentAppointmentForm()
    student=models.Student.objects.get(user_id=request.user.id) 
    message=None
    mydict={'appointmentForm':appointmentForm,'student':student,'message':message}
    if request.method=='POST':
        appointmentForm=forms.StudentAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('teacherId'))
            desc=request.POST.get('description')

            teacher=models.Teacher.objects.get(user_id=request.POST.get('teacherId'))
            
            if teacher.department == 'ICT':
                if 'Ict' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Teacher"
                    return render(request,'mypage/student_book_appointment.html',{'appointmentForm':appointmentForm,'student':student,'message':message})




            appointment=appointmentForm.save(commit=False)
            appointment.teacherId=request.POST.get('teacherId')
            appointment.studentId=request.user.id 
            appointment.teacherName=models.User.objects.get(id=request.POST.get('teacherId')).first_name
            appointment.studentName=request.user.first_name 
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('student-view-appointment')
    return render(request,'mypage/student_book_appointment.html',context=mydict)





@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_view_appointment_view(request):
    student=models.Student.objects.get(user_id=request.user.id) 
    appointments=models.Appointment.objects.all().filter(studentId=request.user.id)
    return render(request,'mypage/student_view_appointment.html',{'appointments':appointments,'student':student})










#
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'mypage/aboutus.html')

