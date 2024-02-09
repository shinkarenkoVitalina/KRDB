import hashlib
from django.shortcuts import render
from . import connectiontobd as con
import smtplib
from email.mime.text import MIMEText
import random, string


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def main_page(request):
    return render(request, 'mainpage/MainPage.html')


def registration(request):
    mes_err = ''
    return render(request, 'mainpage/Registration.html', {'mes_err': mes_err})


def autorization(request):
    mes_err = ''
    return render(request, 'mainpage/Autorization.html', {'mes_err': mes_err})


def IsExist(mail):
    query = f"SELECT * FROM Пользователь WHERE Почта = '{mail}'"
    res = con.ExecuteReadQuery(query)
    if (res):
        return 1
    else:
        return 0


def IsValid(name, email):
    message = ''
    # Поля не должны быть пустыми
    if (name == '' or email == ''):
        message = 'Все поля должны быть заполнены'
        return message, False
    # пароли должны совпадать
    # имя не должно иметь длину более 100 символов
    if (len(name) >= 100):
        message = 'Имя слишком длинное, доппустимая длина имени < 100 символов'
        return message, False
    return message, True


def SendMail(email, token):
    print("sendmail")
    mail_from = "taskmanagerdone2@gmail.com"
    mail_to = "alexzoombie036@gmail.com"
    # mail_to = f'{email}'
    password = "nssq wqfm qoyt rqte"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    message = f""" 
        Для завершения регистрации перейдите по ссылке:
        http://127.0.0.1:8000/ver/{token}

        Если вы не пытались зарегестрироваться в нашем приложении проигнорируйте это письмо

        DONE task manager"""
    mes = f"Для завершения регистрации перейдите по ссылке {token}"
    server.starttls()
    try:
        server.login(mail_from, password)
        mes = MIMEText(mes)
        message = MIMEText(message)
        server.sendmail(mail_from, mail_to, message.as_string())
        server.quit()
        return "Success"
    except Exception as _ex:
        return f"{_ex}\nПроверьте правильность введенных данных"


def RegUser(request):
    # получаем данные из формы
    name = request.POST.get('name')
    email = request.POST.get('login')
    # Проверяем валидность формы:
    mes_err, is_valid = IsValid(name, email)
    print(f'is_valid отработала/n mes_err = {mes_err} /n is_valid = {is_valid}')
    if (is_valid):
        is_reg = IsExist(email)
        print(f'is_exist отработала/n is_reg = {is_reg}')
        if (is_reg):
            mes_err = 'Пользователь с данным адресом почты уже зарегестрирован'
            return render(request, 'mainpage/Registration.html', {'mes_err': mes_err})
        else:
            token = randomword(30)
            request.session.set_expiry(300)
            request.session['unveruser'] = {'uname': name, 'uemail': email, 'utoken': token}
            print('token = ', token)
            print(request.session['unveruser'])
            SendMail(email, token)
            mes_err = 'На вашу почту было выслано письмо со ссылкой активации, для завершения регистрации перейдите по сылке в письме'
            return render(request, 'mainpage/Registration.html', {'mes_err': mes_err})
    return render(request, 'mainpage/Registration.html')


def ConfirmReg(request, token):
    # нужно понять по какой ссылке перешли и получить ее
    temp_token = token
    print(token)
    # если данный токен есть в кеше сессий
    print(request.session['unveruser']['utoken'])
    if (temp_token == request.session['unveruser']['utoken']):
        mes_err = ""
        return render(request, 'mainpage/Confirm.html', {'mes_err': mes_err})
    # else:
    mes_err = "Действие токена подтверждения истекло, пожалуйста, пройдите регистрацию повторно"
    return render(request, 'mainpage/Registration.html', {'mes_err': mes_err})


def DoneReg(request):
    pass1 = request.POST.get('pass1')
    pass2 = request.POST.get('pass2')
    if (pass1 == '' or pass2 == ''):
        mes_err = "Нужно ввести и подтвердить пароль"
        return render(request, 'mainpage/Confirm.html', {'mes_err': mes_err})
    if (pass1 != pass2):
        mes_err = "Пароли не совпадают"
        return render(request, 'mainpage/Confirm.html', {'mes_err': mes_err})
    hpass = hashlib.md5(pass1.encode())
    pass1 = hpass.hexdigest()
    if (request.session.keys()):
        name = request.session['unveruser']['uname']
        email = request.session['unveruser']['uemail']
        print(name)
        print(email)
        query = f"INSERT INTO Пользователь VALUES ('{name}', '{email}', '{pass1}')"
        con.ExecuteQuery(query)
        print('reg suc')
        request.session['user'] = email
        return render(request, 'user_pages/rp_space.html', {'work_spaces': ''})
    else:
        mes_err = "Что-то пошло не так, пожалуйста, пройдите регистрацию повторно"
        return render(request, 'mainpage/Registration.html', {'mes_err': mes_err})


def GetWorkSpaces(email):
    query = f"SELECT * FROM Рабочее_пространство WHERE Почта_пользователя='{email}'"
    temps = con.ExecuteReadQuery(query)
    work_spaces = []
    for i in range(len(temps)):
        listatr = ['name_rp', 'description', 'date_create', 'user_mail', 'id']
        work_space = dict(zip(listatr, temps[i]))
        work_spaces.append(work_space)
    return work_spaces


def AuthUser(request):
    email = request.POST.get('login')
    password = request.POST.get('pass')
    hpass = hashlib.md5(password.encode())
    password = hpass.hexdigest()
    query = f"SELECT Пароль FROM Пользователь WHERE Почта='{email}'"
    data = con.ExecuteReadQuery(query)
    mes_err = ""
    if (data):
        true_pass = data[0][0]
        if (true_pass == password):
            request.session['user'] = email
            print(request.session)
            work_spaces = GetWorkSpaces(email)
            return render(request, 'user_pages/rp_space.html', {'work_spaces': work_spaces})
        else:
            mes_err = "Неверный пароль"
            return render(request, 'mainpage/Autorization.html', {'mes_err': mes_err})
    else:
        mes_err = "Пользователь с данным адресом почты не зарегестрирован"
        return render(request, 'mainpage/Autorization.html', {'mes_err': mes_err})



