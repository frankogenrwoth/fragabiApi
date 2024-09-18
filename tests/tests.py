import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import FragabiUser, Question, Assignment, AssignmentQuestion, Consultation, Answer
from api.v1.serializers import AssignmentSerializer, ConsultationSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def fragabi_user():
    return FragabiUser.objects.create(name="testuser", user_id="helloWas12KS", grade=5)


@pytest.fixture
def question():
    return Question.objects.create(text="Test question", grade=5, score=10)


@pytest.mark.django_db
class TestQuizViewSet:
    def test_generate_quiz(self, api_client, fragabi_user, question):
        url = reverse('quiz-generate')
        data = {
            'grade': 5,
            'num_questions': 1,
            'user_id': str(fragabi_user.id)
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'id' in response.data
        assert len(response.data['questions']) == 1

    def test_view_quiz(self, api_client, fragabi_user, question):
        assignment = Assignment.objects.create(user=fragabi_user)
        AssignmentQuestion.objects.create(assignment=assignment, question=question)

        url = reverse('quiz-view')
        response = api_client.get(url, {'quiz_id': assignment.id})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == assignment.id

    def test_quiz_history(self, api_client, fragabi_user):
        Assignment.objects.create(user=fragabi_user)
        url = reverse('quiz-history')
        response = api_client.get(url, {'user_id': fragabi_user.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_submit_quiz(self, api_client, fragabi_user, question):
        assignment = Assignment.objects.create(user=fragabi_user)
        assignment_question = AssignmentQuestion.objects.create(assignment=assignment, question=question)
        Answer.objects.create(question=question, text="Correct answer")

        url = reverse('quiz-submit')
        data = {
            'quiz': assignment.id,
            'data': [{'id': assignment_question.id, 'text': 'Test answer'}]
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'questions' in response.data
        assert len(response.data['questions']) == 1

    def test_quiz_report(self, api_client, fragabi_user):
        assignment = Assignment.objects.create(user=fragabi_user)
        url = reverse('quiz-report', args=[assignment.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == assignment.id


@pytest.mark.django_db
class TestConsultationViewSet:
    def test_ask_consultation(self, api_client, fragabi_user):
        url = reverse('consultation-ask')
        data = {
            'user_id': str(fragabi_user.id),
            'text': 'What is the capital of France?'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['text'] == data['text']

    def test_consultation_history(self, api_client, fragabi_user):
        Consultation.objects.create(user=fragabi_user, text="Test question", response="Test answer")
        url = reverse('consultation-history')
        response = api_client.get(url, {'user_id': fragabi_user.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_consultation(self, api_client, fragabi_user):
        consultation = Consultation.objects.create(user=fragabi_user, text="Test question", response="Test answer")
        url = reverse('consultation-detail', args=[consultation.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == consultation.id