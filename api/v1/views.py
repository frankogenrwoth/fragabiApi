import ast

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ai.ask_ai import generate_response
from api.models import FragabiUser, Question, Assignment, AssignmentQuestion, Consultation, Answer
from api.v1.assistants.tutor import evaluate_responses
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

    @action(detail=False, methods=['post'])
    def submit(self, request):
        data = request.data.get('data', [])
        assignment_id = request.data.get("quiz", 1)

        print(type(data), type(assignment_id))


        assignment = get_object_or_404(Assignment, id=assignment_id)

        obj = []

        for item in data:
            try:
                question = AssignmentQuestion.objects.get(pk=item["id"]).question

                answer = Answer.objects.get(question_id=question.id)

                obj.append({
                    "id": item["id"],
                    "question": question,
                    "answer": item["text"],
                    "correct": answer.text,
                    "score": question.score,
                })

            except:
                pass

        marked = evaluate_responses(obj)

        for marked_item in marked:
            ob = AssignmentQuestion.objects.get(id=marked_item["id"])
            ob.text = marked_item["answer"]
            ob.score = marked_item["score"]
            ob.save()

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
    def ask(self, request):
        user = get_object_or_404(FragabiUser, id=request.data.get('user_id'))
        text = request.data.get('text')

        if Consultation.objects.filter(text=text).exists():
            pre_consultation = Consultation.objects.get(text=text)

            consultation = Consultation.objects.create(user=user, text=text, response=pre_consultation.response)
            serializer = self.get_serializer(consultation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        if not text:
            return Response({'error': 'Question text is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate AI response
        ai_response = generate_response(text, grade=user.grade)

        # Create and save the consultation
        consultation = Consultation.objects.create(user=user, text=text, response=ai_response)

        serializer = self.get_serializer(consultation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def history(self, request):
        user = get_object_or_404(FragabiUser, id=request.query_params.get('user_id'))
        consultations = Consultation.objects.filter(user=user).order_by('-id')

        page = self.paginate_queryset(consultations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(consultations, many=True)
        return Response(serializer.data)

    def get(self, request):

        user = get_object_or_404(FragabiUser, id=request.query_params.get('user_id'))
        consultation = get_object_or_404(Consultation, user=user.d, id=request.query_params.get('consultation_id'))

        serializer = self.get_serializer(consultation, many=False)
        return Response(serializer.data)