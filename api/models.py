from django.db import models

"""
    FragabiUser: correclates and stores data on the user that exists in the firebase database

    Question: corresponds to a scrapped question from the pdf

    Answer: corresponds to an individual answer as scrapped from the pdf

    QuestionAnswer: intermediate model that relates the question and answer models (Question -> QuestionAnswer -> Answer)

    Assignment: stores records for an attempted assignment by the user

    AssignmentQuestion: correlates specific assignments and the questions which are part of it
"""


class FragabiUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user_id = models.CharField(max_length=16)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    grade = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name.__str__()

    def fragabi_rating(self):
        return


class EmailStat(models.Model):
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Email Stats"

    def __str__(self):
        return self.id.__str__() + " monthly stats email"


class Question(models.Model):
    grade = models.TextField(default="quiz question")
    text = models.TextField()
    score = models.DecimalField(default=5.0, decimal_places=2, max_digits=4)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class AssignmentQuestion(models.Model):
    assignment = models.ForeignKey("Assignment", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)

    def get_correct_answer(self):
        return Answer.objects.get(question=self.question).text


class Assignment(models.Model):
    user = models.ForeignKey(FragabiUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__() + " assignment"

    def get_total_marks(self):
        assignment_questions = AssignmentQuestion.objects.filter(assignment=self)
        return sum([assignment_question.question.score for assignment_question in assignment_questions])

    def get_score(self):
        assignment_questions = AssignmentQuestion.objects.filter(assignment=self)
        return sum([assignment_question.score for assignment_question in assignment_questions])

    def get_performance(self):
        try:
            return self.get_score() / self.get_total_marks()
        except ZeroDivisionError as e:
            return 0


class Consultation(models.Model):
    user = models.ForeignKey(FragabiUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=510)
    response = models.TextField()

    def __str__(self):
        return self.user.__str__() + " ai consultation"
