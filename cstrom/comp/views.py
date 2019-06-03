import simplejson as simplejson
from django.shortcuts import render, HttpResponse, render_to_response
from .models import Questions, User
import random
from operator import attrgetter
import json
import time
from subprocess import Popen, PIPE



def run_code():


    print("Thread started")

def register(request):

    # data = json.load(open('main_comp_questions.json'))
    # for i in data:
    #     new_question = Questions.objects.create(question=i['question'], option1=i['option1'], option2=i['option2'],
    #                                             option3=i['option3'], option4=i['option4'], answer=i['answer'], explanation='.')
    #     new_question.save()
    # print("done==================")
    return render(request, 'comp/register_new.html')


def check_login(request):
    team_name = request.POST.get('team_name')
    participant1 = request.POST.get('participant1')
    mobile1 = request.POST.get('mobile1')
    college1 = request.POST.get('college1')
    email1 = request.POST.get('email1')
    reciept_number = request.POST.get('reciept_number')
    participant2 = request.POST.get('participant2')
    mobile2 = request.POST.get('mobile2')
    college2 = request.POST.get('college2')
    email2 = request.POST.get('email2')
    msg = ''
    new_user = User(login_name=team_name, receipt_number=reciept_number, phone_number1=mobile1, phone_number2=mobile2,
                    college_name1=college1,
                    college_name2=college2, user_name1=participant1, user_name2=participant2, email1=email1,
                    email2=email2)
    new_user.save()
    # return generate(request,new_user.pk)
    return instruction_view(request, new_user.pk)


# Generate once user registers
def generate(request, user_id):
    all_user = list(User.objects.all().order_by('total_score'))
    all_user.reverse()
    # try:
    #     f = open('requirement.txt', 'w')
    # 
    #     for user in all_user:
    #         code =str(user.user_name1 + " " + user.user_name2 + "  " + user.college_name1 + "  " + str(user.phone_number1) + "  "+ str(user.phone_number2)+ "  "+ str(user.total_score) +" \n\n ")#+ " " + user.user_name2 + " " + user.college_name1 + " " + user.phone_number1 + " " + user.phone_number2 + " " + user.total_score)
    # 
    #         f.write(code)
    #     f.close()
    # except:
    #     print("not")


    easy = []
    medium = []
    hard = []

    easy_from_db = Questions.objects.filter(type = 0)
    for i in easy_from_db:
        easy.append(i.pk)

    random.shuffle(easy)

    medium_from_db = Questions.objects.filter(type=1)
    for i in medium_from_db:
        medium.append(i.pk)

    random.shuffle(medium)

    hard_from_db = Questions.objects.filter(type=2)
    for i in hard_from_db:
        hard.append(i.pk)

    random.shuffle(hard)


    print(len(easy))
    print(len(medium))
    print(len(hard))
    # print(easy[0])
    current_user = User.objects.get(pk=user_id)

    current_user.question_array_easy = json.dumps(easy)
    current_user.question_array_medium = json.dumps(medium)
    current_user.question_array_hard = json.dumps(hard)
    current_user.count_easy = 0
    current_user.count_hard = 0
    current_user.count_medium = 0
    current_user.total_score = 0
    current_user.correct_answered = 3
    current_user.level = 1
    current_user.user_bonus_clicked = False
    current_user.user_bonus_activated = True
    current_user.end_time = time.time() + (30 * 60)
    # current_user.attempted_questions=easy[0]
    current_user.save()

    # return HttpResponse("<h3>hii</h3>")
    level = "Easy"
    all_user = list(User.objects.all().order_by('total_score'))
    all_user.reverse()

    return render(request, 'comp/question_new.html',
                  {'question': Questions.objects.get(pk=easy[0]), 'user_id': user_id, 'score': current_user.total_score,
                   'enabled_skip': True, 'enabled_bonus': current_user.user_bonus_activated, 'remaining_time': current_user.end_time - time.time(), 'level': level,
                   'all_user': all_user
                   }
                  )


# For next new Question or same Question if no option is selected
def next(request, user_id):
    if request.POST.get("finish_test"):
        all_user = list(User.objects.all().order_by('total_score'))
        all_user.reverse()
        # all_user = User.objects.all()
        # all_user.sort(key=lambda x: x.total_score(),reverse= True)
        # for user in all_user:
        # print(user.total_score)

        return render(request, 'comp/leaderboard_new.html', {'user_id': int(user_id), 'all_user': all_user})

    selected_option = request.POST.get("option")
    correct = False
    jsonDec = json.decoder.JSONDecoder()
    selected_id = request.POST.get("id") #id of attempted question
    attempted_question = Questions.objects.get(pk=selected_id) #actual question
    # print(str(selected_option))
    # print(str(selected_id))
    counter = 0
    bonus_activated = False
    current_user = User.objects.get(pk=user_id)

    # current_user.save() not necessary

    enabled_skip = False
    if current_user.correct_answered >= 3:
        enabled_skip = True

    if request.POST.get("bonus"):
        current_user.user_bonus_clicked = True
        current_user.save()
        level = ""
        if current_user.level == 1:
            level = "Easy"
        elif current_user.level == 2:
            level = "Medium"
        else:
            level = "Hard"

        all_user = User.objects.all().order_by('total_score').reverse()
        rank = 0
        for user in all_user:
            rank += 1
            if user == current_user:
                break
        return render(request, 'comp/question_new.html',
                      {'question': Questions.objects.get(pk=selected_id), 'user_id': user_id,
                       'enabled_skip': enabled_skip, 'enabled_bonus': False,
                       'score': current_user.total_score, 'current_rank': rank,
                       'remaining_time': current_user.end_time - time.time()})

    if request.POST.get("next"):
        # print(current_user.pk)
        # print(current_user.login_name)
        # print(current_user.attempted_questions)

        if selected_option in [None, '']:
            # print("inside none")
            # print(selected_id)
            # print(current_user.user_bonus)
            return render(request, 'comp/question_new.html',
                          {'question': Questions.objects.get(pk=selected_id), 'user_id': user_id,
                           'error_msg': 'Please select one option!', 'current_user': current_user,
                           'score': current_user.total_score, 'enabled_skip': enabled_skip,
                           'enabled_bonus': current_user.user_bonus_activated,
                           'remaining_time': current_user.end_time - time.time()})

        elif attempted_question.answer == selected_option:
            correct = True
            current_user.correct_answered += 1
            current_user.save()

        if attempted_question.option1 == selected_option:
            current_user.attempted_answers += ", 1"
        elif attempted_question.option2 == selected_option:
            current_user.attempted_answers += ", 2"
        elif attempted_question.option3 == selected_option:
            current_user.attempted_answers += ", 3"
        elif attempted_question.option4 == selected_option:
            current_user.attempted_answers += ", 4"
        current_user.attempted_questions += ("," + str(selected_id))
        current_user.save()

        # Make a customised code for index bound out of range for medium and hard level conditions

        if current_user.level == 1:
            current_user.count_easy += 1
            current_user.save()

            if correct is True:
                counter = current_user.count_medium
                question = jsonDec.decode(current_user.question_array_medium)
                current_user.level = 2
                current_user.total_score += 2
                level = "Medium"
                if current_user.user_bonus_clicked is True:
                    current_user.user_bonus_clicked = False
                    current_user.user_bonus_activated = False
                    bonus_activated = False
                    current_user.total_score += 2
                current_user.save()
            else:
                counter = current_user.count_easy
                current_user.total_score -= 1
                level = "Easy"
                if current_user.user_bonus_clicked is True:
                    current_user.user_bonus_clicked = False
                    current_user.user_bonus_activated = False
                    bonus_activated = False
                    current_user.total_score -= 1
                current_user.save()
                question = jsonDec.decode(current_user.question_array_easy)
        elif current_user.level == 2:
            # print("level 2")
            #
            # print(current_user.level)
            current_user.count_medium += 1
            current_user.save()
            if correct:
                level = "Hard"
                counter = current_user.count_hard
                question = jsonDec.decode(current_user.question_array_hard)
                current_user.level = 3
                current_user.total_score += 4
                if current_user.user_bonus_clicked is True:
                    current_user.user_bonus_clicked = False
                    current_user.user_bonus_activated = False
                    bonus_activated = False
                    current_user.total_score += 4
                current_user.save()
            else:
                level = "Easy"
                counter = current_user.count_easy
                question = jsonDec.decode(current_user.question_array_easy)
                current_user.level = 1
                current_user.total_score -= 2
                if current_user.user_bonus_clicked is True:
                    current_user.user_bonus_clicked = False
                    current_user.user_bonus_activated = False
                    bonus_activated = False
                    current_user.total_score -= 2
                current_user.save()
        else:
            # print("level 3")
            #
            # print(current_user.level)
            current_user.count_hard += 1
            current_user.save()

            if correct:
                level = "Hard"
                counter = current_user.count_hard
                question = jsonDec.decode(current_user.question_array_hard)
                current_user.total_score += 8
                if current_user.user_bonus_clicked == True:
                    current_user.user_bonus_clicked = False
                    current_user.user_bonus_activated = False
                    bonus_activated = False
                    current_user.total_score += 2
                current_user.save()
            else:
                level = "Medium"
                counter = current_user.count_medium
                question = jsonDec.decode(current_user.question_array_medium)
                current_user.level = 2
                current_user.total_score -= 4
                if current_user.user_bonus_clicked:
                    current_user.user_bonus_clicked = False
                    current_user.user_bonus_activated = False
                    bonus_activated = False
                    current_user.total_score -= 4
                current_user.save()

    elif request.POST.get('skip'):
        current_user.attempted_questions += ("," + str(selected_id))
        current_user.attempted_answers += ","
        current_user.correct_answered -= 3
        current_user.save()
        if current_user.level == 1:
            level = "Easy"
            current_user.count_easy += 1
            current_user.save()
            counter = current_user.count_easy
            question = jsonDec.decode(current_user.question_array_easy)
        elif current_user.level == 2:
            level = "Medium"
            current_user.count_medium += 1
            current_user.save()
            counter = current_user.count_medium
            question = jsonDec.decode(current_user.question_array_medium)
        else:
            level = "Hard"
            current_user.count_hard += 1
            current_user.save()
            counter = current_user.count_hard
            question = jsonDec.decode(current_user.question_array_hard)
        # print(counter)

        current_user.save()
    # print(counter)
    if current_user.correct_answered >= 3:
        enabled_skip = True
    else:
        enabled_skip = False

    all_user = User.objects.all().order_by('total_score').reverse()
    rank = 0
    for user in all_user:
        rank += 1
        if user == current_user:
            break
    if(len(question) <= counter):
        all_user = list(User.objects.all().order_by('total_score'))
        all_user.reverse()
        # all_user = User.objects.all()
        # all_user.sort(key=lambda x: x.total_score(),reverse= True)
        # for user in all_user:
        # print(user.total_score)

        return render(request, 'comp/leaderboard_new.html', {'user_id': int(user_id), 'all_user': all_user})

    return render(request, 'comp/question_new.html',
                  {'question': Questions.objects.get(pk=question[counter]), 'user_id': user_id,
                   'enabled_skip': enabled_skip, 'enabled_bonus': current_user.user_bonus_activated,
                   'score': current_user.total_score, 'remaining_time': current_user.end_time - time.time(),
                   'level': level, 'current_rank': rank, 'current_team': current_user.login_name})


# To print all Questions
def print_all_questions(request):
    all_questions = Questions.objects.all()
    return render(request, 'comp/print_all_questions.html', {'all_questions': ''})


# leaderboard
def leaderboard(request, user_id):

    all_user = list(User.objects.all().order_by('total_score'))
    all_user.reverse()
    # try:
    #     f = open('requirement.txt', 'w')
    # 
    #     for user in all_user:
    #         code = user.user_name1 + " " + user.user_name2 + " " + user.college_name1 + " " + user.phone_number1 + " " + user.phone_number2 + " " + user.total_score
    #         f.write(code)
    #     f.close()
    # except:
    #     print("not")
    return render(request, 'comp/leaderboard_new.html', {'user_id': int(user_id), 'all_user': all_user})


def instruction_view(request, user_id):
    return render(request, 'comp/instructions_new.html', {'user_id': user_id})


def update_leaderboard(request):
    leaderboard_dict = []
    all_user = User.objects.all().order_by('total_score').reverse()
    for user in all_user:
        leaderboard_dict.append({user.login_name: user.total_score})

    # sorted(leaderboard_dict.values())
    # print(leaderboard_dict, "----------------------")

    return HttpResponse(simplejson.dumps({'read': list(all_user.values_list('login_name', flat=True)),
                                          'newest': list(all_user.values_list('total_score', flat=True))}))
