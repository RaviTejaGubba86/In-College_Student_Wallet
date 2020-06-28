from django.shortcuts import render
from . models import StudentWallet
from django.core.mail import send_mail
import random
import datetime


s_stdid = None
s_amount = None

def paymentPortal(request):
    return render(request, 'app/paymentsDesk.html')


def paymentDesk(request):
    if request.method == "POST":
        if request.POST['stu_id'] and request.POST['amount']:
            stuID = request.POST['stu_id']
            amount = request.POST['amount']
            student = StudentWallet.objects.get(studentID=request.POST['stu_id'])
            request.session['sid'] = stuID
            request.session['amount'] = amount
            balance = student.balance
            if int(request.POST['amount']) > balance:
               return  render(request,'app/failedTransaction.html')
            else:
                subject = 'One time password'
                otp = random.randrange(1000,10000,1)
                request.session['otpg'] = otp
                content = 'Use this ' + str(otp) + '  as your otp for payment' 
                from_address = 'grt9640973619@gmail.com'
                email_address = [str(student.studentEmail)]
                send_mail(subject,content,from_address,email_address, fail_silently=False)
                return render(request,'app/otpDesk.html',{'sid' : stuID})

    return render(request,'app/paymentsDesk.html')

def otpDesk(request): 
    if request.method == "POST":
        if request.POST['otp']:
            otpform = int(request.POST['otp'])
            if otpform == request.session.get('otpg'):
                ID = str(request.session['sid'])
                student = StudentWallet.objects.get(studentID=ID)
                balance = student.balance
                deduct = int(request.session['amount'])
                #deduct = s_amount
                student.balance = balance-deduct
                student.save()
                if deduct >=500:
                    subject = "Your ward's payment"
                    content = 'Dear parent, your ward'+str(student.studentName)+'spent an amount of Rs. '+str(deduct)+'on'+str(datetime.datetime.now())
                    from_address = 'grt9640973619@gmail.com'
                    email_address = [str(student.parentEmail)]
                    send_mail(subject,content,from_address,email_address,fail_silently=False)
            
                if student.balance < 100:
                    subject = "Your ward's requirement"
                    content = 'Dear parent, your ward'+str(student.studentName)+'may be in need of money for his/her expences. Please do contact your ward'
                    from_address = 'grt9640973619@gmail.com'
                    email_address = [str(student.parentEmail)]
                    send_mail(subject,content,from_address,email_address,fail_silently=False)
                subject = 'payment receipt reg.'
                content = 'Dear customer you have spent Rs. '+str(request.session['amount'])+' on '+str(datetime.datetime.now())+'. Your balance is Rs. '+str(student.balance)
                from_address = 'grt9640973619@gmail.com'
                email_address = [str(student.studentEmail)]
                send_mail(subject,content,from_address,email_address, fail_silently=False)
                return render(request, 'app/successfulTransaction.html')
            else:
                return render(request,'app/otpDesk.html')
    return render(request,'app/paymentsDesk.html')