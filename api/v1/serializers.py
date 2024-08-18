from api.models import FragabiUser, Answer, Question, AssignmentQuestion, Assignment, Consultation
from rest_framework import serializers


class FragabiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FragabiUser
        fields = ['id', 'name', 'user_id', 'grade', 'date_added', 'date_modified']
        read_only_fields = ['date_added', 'date_modified']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'grade', 'text', 'score', 'answers']


class AssignmentQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = AssignmentQuestion
        fields = ['id', 'question', 'text', 'score']


class AssignmentSerializer(serializers.ModelSerializer):
    questions = AssignmentQuestionSerializer(many=True, read_only=True, source='assignmentquestion_set')
    total_marks = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    score = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    performance = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'user', 'date_added', 'date_modified', 'questions', 'total_marks', 'score', 'performance']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_marks'] = instance.get_total_marks()
        representation['score'] = instance.get_score()
        representation['performance'] = instance.get_performance()
        return representation


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'user', 'text', 'response']
        read_only_fields = ['response']