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
    # lists_id = []
    for i in range(len(temps)):
        # lists_id.append(temps[i][3])
        listatr = ['name','date','num','id','desk_id']
        list_space = dict(zip(listatr,temps[i]))
        lists.append(list_space)
    # list_spaces = sorted(lists, key=('num'))
    # lists_id = tuple(lists_id)
    return lists

def GetCardList(list_id):
    # if(lists_id):
    #     if(type(lists_id)!=int):
    #         query = f"SELECT * FROM Карточка WHERE id_Списка in {lists_id}"
    #     else:
    #         query = f"SELECT * FROM Карточка WHERE id_Списка = {lists_id}"
    #     temps = con.ExecuteReadQuery(query)
    #     tasks = []
    #     tasks_id = []
    #     if (temps):
    #         for i in range(len(temps)):
    #             tasks_id.append(temps[i][6])
    #             listatr = ['name', 'desc', 'date', 'dedline', 'num', 'check', 'id', 'list_id']
    #             task = dict(zip(listatr, temps[i]))
    #             tasks.append(task)
    #         # task_spaces = sorted(tasks, key=('num'))
    #         tasks_id = tuple(tasks_id)
    # else:
    #     tasks = []
    #     tasks_id = []
    # return tasks, tasks_id

    query = f"SELECT * FROM Карточка WHERE id_Списка={list_id}"
    temps = con.ExecuteReadQuery(query)
    tasks = []
    for i in range(len(temps)):
        listatr = ['name', 'desc', 'date', 'dedline', 'num', 'check', 'id', 'list_id']
        task = dict(zip(listatr, temps[i]))
        tasks.append(task)
    # task_spaces = sorted(tasks, key=('num'))
    return tasks

def GetCheckLists(task_id):
    # if(tasks_id):
    #     if(type(tasks_id)!=int):
    #         query = f"""SELECT * FROM "Чек-лист" WHERE id_Карточки in {tasks_id}"""
    #     else:
    #         query = f"""SELECT * FROM "Чек-лист" WHERE id_Карточки = {tasks_id}"""
    #     temps = con.ExecuteReadQuery(query)
    #     checklists = []
    #     checklists_id = []
    #     if (temps):
    #         for i in range(len(temps)):
    #             checklists_id.append(temps[i][3])
    #             listatr = ['name', 'check', 'date', 'id', 'task_id']
    #             checklist = dict(zip(listatr, temps[i]))
    #             checklists.append(checklist)
    #         checklists_id = tuple(checklists_id)
    # else:
    #     checklists = []
    #     checklists_id = []
    # return checklists, checklists_id

    query = f"""SELECT * FROM "Чек-лист" WHERE id_Карточки={task_id}"""
    temps = con.ExecuteReadQuery(query)
    checklists = []
    for i in range(len(temps)):
        listatr = ['name', 'check', 'date', 'id', 'task_id']
        checklist = dict(zip(listatr, temps[i]))
        checklists.append(checklist)
    return checklists

def GetActionLists(checklist_id):
    # if(checklists_id):
    #     if(type(checklists_id)!=int):
    #         query = f"""SELECT * FROM Действие WHERE "id_Чек-листа" in {checklists_id}"""
    #     else:
    #         query = f"""SELECT * FROM Действие WHERE "id_Чек-листа" = {checklists_id}"""
    #     temps = con.ExecuteReadQuery(query)
    #     Actions = []
    #     actions_id = []
    #     if(temps):
    #         for i in range(len(temps)):
    #             actions_id.append(temps[i][4])
    #             listatr = ['name', 'check', 'date', 'dedline', 'id', 'cl_id']
    #             action = dict(zip(listatr, temps[i]))
    #             Actions.append(action)
    # else:
    #     Actions = []
    # return Actions

    query = f"""SELECT * FROM Действие WHERE "id_Чек-листа"={checklist_id}"""
    temps = con.ExecuteReadQuery(query)
    actions = []
    for i in range(len(temps)):
        listatr = ['name', 'check', 'date', 'dedline', 'id', 'cl_id']
        action = dict(zip(listatr, temps[i]))
        actions.append(action)
    return actions
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
    query = f"SELECT background_color FROM Фон_доски"
    data = con.ExecuteReadQuery(query)
    colors = []
    for i in range(len(data)):
        tempdt = data[i]
        temp = {'name': tempdt[0]}
        colors.append(temp)
    return render(request, 'user_pages/desk_space.html', {'desk_spaces': desk_spaces, 'id_ws':id_ws, 'rp_name': rp_name,'rp_desc':rp_desc, 'colors': colors})


def NormalizeDeskView(lists):
    newlist = sorted(lists, key=lambda d: d['num'])
    num = 0
    for item in newlist:
        num += 1
        item_id = item['id']
        query = f"UPDATE Список SET Номер_на_доске = {num} WHERE id = {item_id}"
        con.ExecuteQuery(query)

def NormalizeListView(tasks):
    newlist = sorted(tasks, key=lambda d: d['num'])
    num = 0
    for item in newlist:
        num += 1
        item_id = item['id']
        query = f"UPDATE Карточка SET Номер_в_списке = {num} WHERE id = {item_id}"
        con.ExecuteQuery(query)


def user_desk(request, id_ws, desk_id):
    # Desks, id_ws = GetDeskSpaces(id_ws)
    # Lists, lists_id = GetDeskLists(desk_id)
    # if(Lists):
    #     NormalizeDeskView(Lists)
    #     for list in Lists:
    #         list_id = list['id']
    #         ttasks, task_id = GetCardList(list_id)
    #         if(ttasks):
    #             NormalizeListView(ttasks)
    # Tasks, tasks_id = GetCardList(lists_id)
    # Clists, clists_id = GetCheckLists(tasks_id)
    # Actions = GetActionLists(clists_id)
    # query = f"SELECT Название, Описание FROM Доска WHERE id = {desk_id}"
    # desk_data = con.ExecuteReadQuery(query)
    # desk_name = desk_data[0][0]
    # desk_desc = desk_data[0][1]


    Desks, id_ws = GetDeskSpaces(id_ws)
    Lists = GetDeskLists(desk_id)
    # NormalizeDeskView(Lists)
    Tasksinlists = []
    CheckLists = []
    ActionList = []
    for list in Lists:
        list_id = list['id']
        Taskinlist = GetCardList(list_id)
        # NormalizeListView(Taskinlist)
        Tasksinlists.append(Taskinlist)
        for task in Taskinlist:
            task_id = task['id']
            Checklist = GetCheckLists(task_id)
            CheckLists.append(Checklist)
            for checklist in Checklist:
               cl_id = checklist['id']
               action = GetActionLists(cl_id)
               ActionList.append(action)

    #     Tasksinlists.append(Taskinlist)
    # CheckLists = []
    # for task in Tasksinlists:
    #     print(task[0])
    #     task_id = task['id']
    #     Checklist = GetCheckLists(task_id)
    # #     temp = {f'{task_id}':Checklist}
    #     CheckLists.append(Checklist)
    # ActionList = []
    # for checklist in CheckLists:
    #     cl_id = checklist['id']
    #     action = GetActionLists(cl_id)
    # #     temp = {f'{cl_id}': action}
    #     ActionList.append(action)
    query = f"SELECT Название FROM Доска WHERE id = {desk_id}"
    desk_data = con.ExecuteReadQuery(query)
    data = desk_data[0]
    if(len(data)>1):
        desk_name = data[0]
        desk_desc = data[1]
    else:
        desk_name = data[0]
        desk_desc = ''
    # return Lists, Tasksinlists, CheckLists, ActionList
    return render(request, 'user_pages/user_desk.html', {'Lists':Lists,'desk_id':desk_id, 'id_ws':id_ws, 'desk_name':desk_name, 'desk_desc':desk_desc,
        'Desks':Desks, 'Tasksinlists':Tasksinlists, 'CheckLists':CheckLists, 'ActionList':ActionList})
    # return render(request, 'user_pages/user_desk.html',
    #               {'Lists': Lists, 'desk_id': desk_id, 'id_ws': id_ws, 'Tasksinlists': Tasksinlists})

    # return render(request, 'user_pages/user_desk.html',
    #               {'Lists': Lists, 'desk_id': desk_id, 'id_ws': id_ws, 'Tasks':Tasks, 'Clists':Clists, 'Actions':Actions, 'desk_name':desk_name, 'desk_desc':desk_desc})

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

# ///
def create_checklist(request, id_ws, desk_id, card_id):
    name = request.POST.get('label-name')
    data = datetime.datetime.now()
    check = False
    query = f"""INSERT INTO "Чек-лист"(Название, Статус_выполнения, Дата_создания, id_Карточки) VALUES ('{name}', {check}, '{data}', {card_id})"""
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')
# ///
def create_action(request, id_ws, desk_id, checklist_id):
    name = request.POST.get('label-name')
    data = datetime.datetime.now()
    check = False
    query = f"""INSERT INTO Действие(Название, Статус_выполнения, Дата_создания, "id_Чек-листа") VALUES ('{name}', {check}, '{data}', {checklist_id})"""
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')
# ///
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

def update_space(request, id_ws):
    name = request.POST.get('name')
    desc = request.POST.get('desc')
    print(name)
    print(desc)
    if(not name):
        return redirect('rp_space')
    query = f"UPDATE Рабочее_пространство SET Название = '{name}', Описание = '{desc}' WHERE id = {id_ws}"
    print('2')
    con.ExecuteQuery(query)
    print('3')
    return redirect('rp_space')

def update_desk(request, id_ws, desk_id):
    name = request.POST.get('name')
    desc = request.POST.get('desc')
    if(not name):
        return redirect('desk', id_ws)
    query = f"UPDATE Доска SET Название = '{name}', Описание = '{desc}' WHERE id = {desk_id}"
    con.ExecuteQuery(query)
    return redirect('desk', id_ws)

def update_desk_type(request, id_ws, desk_id):
    typed = request.POST.get('select')
    if(typed=='privat'):
        typed = 'приватная'
    else:
        typed = 'публичная'
    query = f"UPDATE Доска SET Тип = '{typed}' WHERE id = {desk_id}"
    con.ExecuteQuery(query)
    return redirect('desk', id_ws)

def update_list(request, id_ws, desk_id, list_id):
    name = request.POST.get('name')
    if (not name):
        return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    query = f"""UPDATE Список SET Название = '{name}' WHERE id = {list_id}"""
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def update_card(request, space_id, desk_id, card_id):
    pass

def update_checklist(request, id_ws, desk_id, checklist_id):
    name = request.POST.get('label-name')
    if (not name):
        return redirect('desk_space', f'{id_ws}', f'{desk_id}')
    query = f"""UPDATE "Чек-лист" SET Название = '{name}' WHERE id = {checklist_id}"""
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

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

def DeleteTask(request, id_ws, desk_id, task_id):
    query = f"DELETE FROM Карточка WHERE id = {task_id};"
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')

def DeleteChecklist(request, id_ws, desk_id, task_id):
    query = f"""DELETE FROM "Чек-лист" WHERE id_Карточки = {task_id};"""
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

def SortListInDesk(Lists):

    pass

def SortTaskInList(TaskList):
    pass

def GetDeadlineTask(request, id_ws, desk_id, task_id):
    date = request.POST.get('date')
    time = request.POST.get('time')
    print(date)
    print(time)
    deadline = date+' '+time
    query = f"UPDATE Карточка SET Дедлайн = '{deadline}' WHERE id = {task_id}"
    con.ExecuteQuery(query)
    return redirect('desk_space', f'{id_ws}', f'{desk_id}')