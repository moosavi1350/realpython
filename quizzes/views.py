from django.shortcuts import render
import smtplib
from email.message import EmailMessage
from django.contrib.auth.models import User


def quizzes(request):
    return render(request, 'quizzes/index.html')


def process(req):
    # ps = 'cnaaivmbzrrueqxn'
    msg = EmailMessage()
    msg['Subject'] = ' موضوع '
    msg['From'] = 'hm5458584@gmail.com'
    msg['To'] = req.POST['email']
    msg.set_content('سلامی دوباره')

    # with open('t.gif', 'rb') as f:
    #     file_date = f.read()
    #     file_name = f.name
    # msg.add_attachment(file_date, maintype='image', subtype='gif', filename=file_name)
    msg.add_alternative('''
    <body dir=rtl style="background-color:gray; border-radius:12px; padding-right:12px" kk="hasan" >
        <h1> این اولین ایمیل ماست برای امتحان </h1>
        <img src='https://ali7.iran.liara.run/static/media/w1.jfif' />
        <h4> منتظر ایمیل های بعدی ما باشید </h4>
        
    </body>
    ''', subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('hm5458584@gmail.com', 'cnaaivmbzrrueqxn')
        # server.sendmail('sssss', 'z.moosavi@chmail.ir', 'khobiiiiii')
        server.send_message(msg)

    em = req.POST['email']
    try:
        u = User.objects.create_user(em, em, em)
    except Exception as ex:
        pass

    return render(req, 'quizzes/welcome.html', {'em': em})
