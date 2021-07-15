from django.test import TestCase
from survey.models import Question
from django.contrib.auth import get_user_model


class QuestionTestCase(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create(first_name='User1', username='user1', email='user1@example.com')
        self.user2 = get_user_model().objects.create(first_name='User2', username='user2', email='user2@example.com')

        Question.objects.create(title="Pregunta 1", description="Descripción pregunta 1", author=self.author)
        Question.objects.create(title="Pregunta 2", description="Descripción pregunta 2", author=self.author)

    def test_ranking_by_answer(self):
        """
        Questions updates ranking by taking answers
        """
        question1 = Question.objects.get(title="Pregunta 1")
        question1.answers.create(value=1, author=self.user2)

        self.assertEqual(question1.ranking, 20)

    def test_ranking_by_likes(self):
        """
        Questions updates ranking by taking likes
        """
        question1 = Question.objects.get(title="Pregunta 1")
        ranking = question1.ranking
        question1.reviews.create(like=True, author=self.user2)

        self.assertEqual(ranking + 5, question1.ranking)

    def test_ranking_by_dislikes(self):
        """
        Questions updates ranking by taking dislikes
        """
        question1 = Question.objects.get(title="Pregunta 1")
        ranking = question1.ranking
        question1.reviews.create(like=False, author=self.user2)

        self.assertEqual(ranking - 3, question1.ranking)

