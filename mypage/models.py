from django.db import models
from django.contrib.auth.models import User



departments=[('Department','Department'),
('Industrial Education','Industrial Education'),
('ITDept','ITDept'),
('Math and Science','Math and Science'),
]
position=[('Position','Position'),
('Teacher1','Teacher1'),
('Teacher2','Teacher2'),
('Teacher3','Teacher3'),
('Teacher4','Teacher4'),

]
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/TeacherProfilePic/',null=True,blank=True)
    position = models.CharField(max_length=50,choices=position,default='Position')
    department= models.CharField(max_length=50,choices=departments,default='Department')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)


course=[('Select Course','Select Course'),
('BSIE-ICT','BSIE-ICT'),
('BSIE-IA','BSIE-IA'),
('CIVIL ENGENEERING','CIVIL ENGENEERING'),
('COET','COET'),
('BET ESET','BET ESET'),
('ELECTRICAL ENGENEERING','ELECTRICAL ENGENEERING'),
('MECHANICAL ENGENEERING','MECHANICAL ENGENEERING'),

]
year=[('Select Year','Select Year'),
('1st year','1st year'),
('2nd year','2nd year'),
('3rd year','3rd year'),
('4th year','4th year'),
]


class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/StudentProfilePic/',null=True,blank=True)
    course = models.CharField(max_length=50,choices=course,default='Select Course')
    year = models.CharField(max_length=50,choices=year,default='Select Year')
    violation = models.CharField(max_length=100,null=False)
    service = models.CharField(max_length=100,null=True)
    scheduleday = models.CharField(max_length=100,null=True)
    hoursperday = models.CharField(max_length=100,null=True)
    assignedTeacherId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    def __str__(self):
        return self.user.first_name+" ("+self.violation+")"


class Appointment(models.Model):
    studentId=models.PositiveIntegerField(null=True)
    teacherId=models.PositiveIntegerField(null=True)
    studentName=models.CharField(max_length=40,null=True)
    teacherName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)






