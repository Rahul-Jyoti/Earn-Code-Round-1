from django.db import models


class Questions(models.Model):
    question = models.TextField(max_length=2000)
    option1 = models.CharField(max_length=300)
    option2 = models.CharField(max_length=300)
    option3 = models.CharField(max_length=300)
    option4 = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
    type = models.IntegerField(max_length=100)
    explanation = models.TextField(max_length=3000)

    def __str__(self):
        return str(self.pk)

    def get_options(self):
        return [self.option1, self.option2, self.option3, self.option4]


class User(models.Model):
    login_name = models.CharField(max_length=100)
    receipt_number = models.IntegerField()
    phone_number1 = models.IntegerField()
    phone_number2 = models.IntegerField()
    college_name1 = models.CharField(max_length=100)
    college_name2 = models.CharField(max_length=100)
    user_name1 = models.CharField(max_length=100)
    user_name2 = models.CharField(max_length=100)
    email1 = models.CharField(max_length=100)
    email2 = models.CharField(max_length=100)
    attempted_questions = models.CharField(max_length=1000)
    attempted_answers = models.CharField(max_length=1000)
    total_score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    count_easy = models.IntegerField(default=0)
    count_medium = models.IntegerField(default=0)
    count_hard = models.IntegerField(default=0)
    question_array_easy = models.TextField()
    question_array_medium = models.TextField()
    question_array_hard = models.TextField()
    correct_answered = models.IntegerField(default=5)
    user_bonus_clicked = models.BooleanField(default=False)
    user_bonus_activated = models.BooleanField(default=True)

    end_time = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk)+" "+str(self.login_name)
