from django.db import models

# Create your models here.
class StudentWallet(models.Model):
    studentID = models.CharField(max_length = 15, default='')
    studentName = models.CharField(max_length = 50)
    studentMobile = models.CharField(max_length=10)
    parentMobile = models.CharField(max_length=10)
    balance = models.PositiveIntegerField()
    studentEmail = models.EmailField(max_length=50,default='abc@gmail.com')
    parentEmail = models.EmailField(max_length=50,default='abc@gmail.com')

