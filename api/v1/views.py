from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ai.ask_ai import generate_response
from api.models import FragabiUser, Question, Assignment, AssignmentQuestion, Consultation
from api.v1.serializers import FragabiUserSerializer, QuestionSerializer, AssignmentSerializer, ConsultationSerializer
from api.v1.utils import get_n_random_elements_from_list


class FragabiUserViewSet(viewsets.ModelViewSet):
    queryset = FragabiUser.objects.all()
    serializer_class = FragabiUserSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        grade = request.data.get('grade')
        num_questions = request.data.get('num_questions', 10)

        questions = Question.objects.filter(grade=grade)
        user = get_object_or_404(FragabiUser, id=request.data.get('user_id'))

        assignment = Assignment.objects.create(user=user)

        random_quiz_questions = get_n_random_elements_from_list(num_questions, len(questions) - 1)

        selected_questions = [questions[i] for i in random_quiz_questions]

        print(random_quiz_questions, selected_questions)


        for question in selected_questions:
            AssignmentQuestion.objects.create(assignment=assignment, question=question)

        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def view(self, request):
        quiz_id = request.query_params.get('quiz_id')
        print(quiz_id)

        assignment = Assignment.objects.get(id=quiz_id)
        serializer = AssignmentSerializer(assignment)

        print(assignment, serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        user = get_object_or_404(FragabiUser, id=request.query_params.get('user_id'))
        assignments = Assignment.objects.filter(user=user).order_by('-date_added')
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        assignment = get_object_or_404(Assignment, id=pk)
        print(assignment)
        submitted_answers = request.data.get('data', [])

        for submitted_answer in submitted_answers:
            assignment_question = get_object_or_404(AssignmentQuestion, assignment=assignment, question_id=submitted_answer['question_id'])
            correct_answer = assignment_question.question.answer_set.filter(text=submitted_answer['answer']).exists()
            assignment_question.score = assignment_question.question.score if correct_answer else 0
            assignment_question.save()

        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        assignment = get_object_or_404(Assignment, id=pk)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

    @action(detail=False, methods=['post'])
    def ask_question(self, request):
        user = get_object_or_404(FragabiUser, id=request.data.get('user_id'))
        text = request.data.get('text')

        if not text:
            return Response({'error': 'Question text is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate AI response
        ai_response = generate_response(text, grade=user.grade)

        # Create and save the consultation
        consultation = Consultation.objects.create(user=user, text=text, response=ai_response)

        serializer = self.get_serializer(consultation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def chat_history(self, request):
        user = get_object_or_404(FragabiUser, id=request.query_params.get('user_id'))
        consultations = Consultation.objects.filter(user=user).order_by('-id')

        page = self.paginate_queryset(consultations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(consultations, many=True)
        return Response(serializer.data)