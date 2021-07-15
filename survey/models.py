from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now

from survey.managers import QuestionQuerySet


class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    # TODO: Quisieramos tener un ranking de la pregunta, con likes y dislikes dados por los usuarios.
    ranking = models.BigIntegerField('Ranking', default=0)

    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])

    @property
    def likes(self):
        return self.reviews.filter(like=True)

    @property
    def dislikes(self):
        return self.reviews.filter(like=False)

    def update_ranking(self):
        self.ranking = self.calculate_ranking()
        self.save()

    def calculate_ranking(self):
        today_bonus = 10 if self.created == now().date() else 0
        return self.answers.count() * 10 + self.likes.count() * 5 - self.dislikes.count() * 3 + today_bonus

    class Meta:
        ordering = ('-ranking', )

    objects = QuestionQuerySet().as_manager()


class Answer(models.Model):
    ANSWERS_VALUES = ((0, 'Sin Responder'),
                      (1, 'Muy Bajo'),
                      (2, 'Bajo'),
                      (3, 'Regular'),
                      (4, 'Alto'),
                      (5, 'Muy Alto'),)

    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0, choices=ANSWERS_VALUES)
    comment = models.TextField("Comentario", default="", blank=True)


class Review(models.Model):
    question = models.ForeignKey(Question, related_name="reviews", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="reviews", verbose_name='Autor', on_delete=models.CASCADE)
    like = models.BooleanField('Like', null=True, blank=True)
