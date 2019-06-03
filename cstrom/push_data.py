import json
from pprint import pprint
import django
django.setup()
from comp.models import Questions

data = json.load(open('main_comp_questions.json'))
for i in data:
    new_question = Questions.objects.create(question = i['question'],option1 = i['option1'],option2 = i['option2'],option3 = i['option3'],option4 = i['option4'],explanation='.')
    new_question.save()
print(data)