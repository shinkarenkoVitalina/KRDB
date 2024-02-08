from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import connectiontobd as con
import datetime

# Create your views here.
def GetWorkSpaces(email):
    query = f"SELECT * FROM Рабочее_пространство WHERE Почта_пользователя='{email}'"
    temps = con.ExecuteReadQuery(query)
    work_spaces = []
    for i in range(len(temps)):
        listatr = ['name_rp','description','date_create','user_mail','id']
        work_space = dict(zip(listatr, temps[i]))
        work_spaces.append(work_space)
    return work_spaces
def GetDeskSpaces(id_ws):
    query = f"SELECT * FROM Доска WHERE id_РП={id_ws}"
    temps = con.ExecuteReadQuery(query)
    desk_spaces = []
    for i in range(len(temps)):
        listatr = ['desk_name','desk_desc','date_desk','type','id','id_ws','back_color']
        desk_space = dict(zip(listatr, temps[i]))
        desk_spaces.append(desk_space)
    return desk_spaces, id_ws

def GetDeskLists(desk_id):
    query = f"SELECT * FROM Список WHERE id_Доски={desk_id}"
    temps = con.ExecuteReadQuery(query)
    lists = []
    for i in range(len(temps)):
        listatr = ['name','date','num','id','desk_id']
        list_space = dict(zip(listatr,temps[i]))
        lists.append(list_space)
    # list_spaces = sorted(lists, key=('num'))
    return lists, desk_id

def GerCardList(list_id):
    query = f"SELECT * FROM Карточка WHERE id_Списка={list_id}"
    temps = con.ExecuteReadQuery(query)
    tasks = []
    for i in range(len(temps)):
        listatr = ['name','desc','date','dedline','num','check','id','list_id']
        task = dict(zip(listatr,temps[i]))
        tasks.append(task)
    # task_spaces = sorted(tasks, key=('num'))
    return tasks, list_id

def GetCheckList(task_id):
    query = f"""SELECT * FROM "Чек-лист" WHERE id_Карточки={task_id}"""
    temps = con.ExecuteReadQuery(query)
    checklists = []
    for i in range(len(temps)):
        listatr = ['name', 'check', 'date', 'id', 'task_id']
        checklist = dict(zip(listatr, temps[i]))
        checklists.append(checklist)
    return checklists, task_id

def GetTaskList(cl_id):
    query = f"""SELECT * FROM Действие WHERE "id_Чек-листа"={cl_id}"""
    temps = con.ExecuteReadQuery(query)
    issues = []
    for i in range(len(temps)):
        listatr = ['name', 'check', 'date', 'dedline', 'id', 'cl_id']
        issue = dict(zip(listatr, temps[i]))
        issues.append(issue)
    return issues, cl_id
def index(request):
    if(request.session.keys()):
        user_mail = request.session['user']
        work_spaces = GetWorkSpaces(user_mail)
    else:
        work_spaces = []
    return render(request, 'user_pages/rp_space.html', {'work_spaces': work_spaces})

def desk(request, id_rp):
    desk_spaces, id_ws = GetDeskSpaces(id_rp)
    query = f"SELECT Название, Описание FROM Рабочее_пространство WHERE id={id_rp}"
    data = con.ExecuteReadQuery(query)
    rp_name = data[0][0]
    rp_desc = data[0][1]
    return render(request, 'user_pages/desk_space.html', {'desk_spaces': desk_spaces, 'id_ws':id_ws, 'rp_name': rp_name,'rp_desc':rp_desc})

def user_desk(request, id_ws, desk_id):
    Desks, id_ws = GetDeskSpaces(id_ws)
    Lists, desk_id = GetDeskLists(desk_id)
    Tasksinlists = []
    # for list in Lists:
    #     list_id = list['id']
    #     Taskinlist = GerCardList(list_id)
    #     temp = {f'{list_id}': Taskinlist}
    #     Tasksinlists.append(temp)
    for list in Lists:
         list_id = list['id']
         Taskinlist, list_id = GerCardList(list_id)
         Tasksinlists.append(Taskinlist)
    CheckLists = []
    # for task in Tasksinlists:
    #     task_id = task['id']
    #     Checklist = GetCheckList(task_id)
    #     temp = {f'{task_id}':Checklist}
    #     CheckLists.append(temp)
    # ActionList = []
    # for checklist in CheckLists:
    #     cl_id = checklist['id']
    #     action = GetTaskList(cl_id)
    #     temp = {f'{cl_id}': action}
    #     ActionList.append(temp)
    # query = f"SELECT Название FROM Доска WHERE id = {desk_id}"
    # desk_name = con.ExecuteReadQuery(query)
    # desk_name = desk_name[0][0]
    # # return Lists, Tasksinlists, CheckLists, ActionList
    # return render(request, 'user_pages/user_desk.html', {'Lists':Lists,'desk_id':desk_id, 'id_ws':id_ws, 'desk_name':desk_name,
    #     'Desks':Desks, 'Tasksinlists':Tasksinlists, 'CheckLists':CheckLists, 'ActionList':ActionList})
    return render(request, 'user_pages/user_desk.html',
                  {'Lists': Lists, 'desk_id': desk_id, 'id_ws': id_ws, 'Tasksinlists':Tasksinlists})

def card_header_view(request):
    header_color = '#FF0000'  # Цвет шапки карточки
    context = {
        'header_color': header_color
    }
    return render(request, 'user_desk.html', context)

def LogoutUser(request):
    if(request.session.keys()):
        del request.session['user']
    return render(request, 'mainpage/MainPage.html')

def create_workspace(request):
    name = request.POST.get('name')
    description = ''
    data = datetime.datetime.now()
    if(request.session.keys()):
        user_mail = request.session['user']
        query = f"INSERT INTO Рабочее_пространство VALUES ('{name}','{description}', '{data}', '{user_mail}')"
        con.ExecuteQuery(query)
        work_spaces = GetWorkSpaces(user_mail)
    else:
        work_spaces = []
    return render(request, 'user_pages/rp_space.html', {'work_spaces': work_spaces})


#
def create_desk(request, id_ws):
    name = request.POST.get('name')
    description = ''
    data = datetime.datetime.now()
    type = 'публичная'
    back_color = 'FFFF00'
    query = f"INSERT INTO Доска(Название, Описание, Дата_создания, Тип, id_РП, background_color) VALUES ('{name}','{description}', '{data}', '{type}', '{id_ws}', '{back_color}')"
    con.ExecuteQuery(query)
    desk_spaces, id_ws = GetDeskSpaces(id_ws)
    return render(request, 'user_pages/desk_space.html', {'desk_spaces': desk_spaces, 'id_ws':id_ws})
    # desk_spaces = ''
    # return render(request, 'user_pages/desk_space.html', {'desk_spaces': desk_spaces, 'id_ws': id_ws})

def create_list(request, id_ws, desk_id):
    name = request.POST.get('name')
    data = datetime.datetime.now()
    query = f"SELECT MAX(Номер_на_доске) FROM Список WHERE id_Доски={desk_id}"
    num = con.ExecuteReadQuery(query)
    if(num[0][0] == None):
        num=1
    else:
        num = num[0][0]+1

    query = f"INSERT INTO Список(Название, Дата_создания, Номер_на_доске, id_Доски) VALUES ('{name}', '{data}', '{num}', '{desk_id}')"
    con.ExecuteQuery(query)
    desk_spaces, id_ws = GetDeskSpaces(id_ws)
    # return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    return redirect('desk_space', id_ws, desk_id)
    # return render(request, 'user_pages/user_desk.html', {'desk_spaces': desk_spaces, 'id_ws': id_ws})



def create_card(request, id_ws, desk_id, list_id):
    name = request.POST.get('name')
    if (name==''):
        mes_err = "В названии карточки должен содержаться хотя бы один символ"
        return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    desc = ''
    data = datetime.datetime.now()
    deadline = ''
    check = False
    query = f"SELECT MAX(Номер_в_списке) FROM Карточка WHERE id_Списка={list_id}"
    temp = con.ExecuteReadQuery(query)
    if (temp[0][0]):
        num = temp[0][0] + 1
    else:
        num = 1
    query = (f"INSERT INTO Карточка(Название, Описание, Дата_создания, Номер_в_списке, Статус_выполнения, id_Списка) VALUES ('{name}', '{desc}', '{data}', {num}, {check},{list_id})")
    con.ExecuteQuery(query)

    return redirect('desk_space', f'{id_ws}', f'{desk_id}')


def create_checklist(request, id_ws, desk_id, card_id):
    # name = request.POST.get('name')
    # data = datetime.datetime.now()
    # check = False
    # query = f"""INSERT INTO (Название, Статус_выполнения, Дата_создания, id_Карточки) VALUES ('{name}', {check}, '{data}', {card_id})"""
    # con.ExecuteQuery(query)
    # return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    pass

def create_task(request, id_ws, desk_id, checklist_id):
    # name = request.POST.get('name')
    # data = datetime.datetime.now()
    # deadline = ''
    # check = False
    # query = f"INSERT INTO Действие(Название, Статус_выполнения, Дата_создания, Дедлайн, 'id_Чек-листа') VALUES ('{name}', {check}, '{data}', '{deadline}', {checklist_id})"
    # con.ExecuteQuery(query)
    # return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    pass

def create_mark(request, id_ws, desk_id):
    # name = request.POST.get('name')
    # # color = ???
    # color = ''
    # if (name == ''):
    #     query = f"INSERT INTO Метка(Цвет, id_РП) VALUES ('{color}', {id_ws})"
    # else:
    #     query = f"INSERT INTO Метка(Название, Цвет, id_РП) VALUES ('{name}', '{color}', {id_ws})"
    # con.ExecuteQuery(query)
    # return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    pass

def update_space(request, space_id):
    # name = request.POST.get('name')
    # desc = request.POST.get('desc')
    # if(name):
    #     if(desc):
    #         query = f"UPDATE Рабочее_пространство SET Название = '{name}', Описание = '{desc}' WHERE id = {space_id}"
    #     else:
    #         query = f"UPDATE Рабочее_пространство SET Название = '{name}' WHERE id = {space_id}"
    # if(desc):
    #     query = f"UPDATE Рабочее_пространство SET Описание = '{desc}' WHERE id = {space_id}"
    # con.ExecuteQuery(query)
    # return redirect('rp_space')
    pass

def update_desk(request, space_id, desk_id):
    pass

def update_list(request, space_id, desk_id, list_id):
    pass

def update_card(request, space_id, desk_id, card_id):
    pass

def update_checklist(request, space_id, desk_id, checlist_id):
    pass

def update_task(request, space_id, desk_id, task_id):
    pass

def MoveCard(request, id_ws, desk_id, card_id):
    pass

def MoveList(request, id_ws, desk_id, list_id):
    pass
def DeleteSpace(request, id_ws):
    query = f"DELETE FROM Рабочее_пространство WHERE id = {id_ws};"
    con.ExecuteQuery(query)
    return redirect('rp_space')
def DeleteDesk(request, id_ws, id_desk):
    query = f"DELETE FROM Доска WHERE id = {id_desk};"
    con.ExecuteQuery(query)
    return redirect('desk', f'{id_ws}')

def DeleteList(request, id_ws, desk_id, list_id):
    query = f"DELETE FROM Список WHERE id = {list_id};"
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def DeleteCard(request, id_ws, desk_id, card_id):
    query = f"DELETE FROM Карточка WHERE id = {card_id};"
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def DeleteChecklist(request, id_ws, desk_id, cl_id):
    query = f"""DELETE FROM "Чек-лист" WHERE id = {cl_id};"""
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def DeleteAction(request, id_ws, desk_id, act_id):
    query = f"DELETE FROM Действие WHERE id = {act_id};"
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def DeleteMark(request, id_ws, desk_id, mark_id):
    query = f"DELETE FROM Метка WHERE id = {mark_id};"
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def MoveList(request, id_ws, desk_id, list_id):
    pass

def MoveCard(request, id_ws, desk_id, card_id):
    # выбираем список и место в нем
    # если список тот же, просто updatим номер в списке текущей карточки пересчитываем все следующие на +1
    #  если список другой нужно обновить всем карточкам с n места номера на +1 затем в том списке создать карточку с желаемым в списке номером затем в текущем списке удалить карточку и пересчитать номера
    pass

def SortForDeadline(request, id_ws, desk_id, list_id):
    # Получить список карточек сделать сортировку по дедлайну
    # заапдейтить бд
    pass

