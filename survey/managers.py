from django.db.models import Q, QuerySet


class QuestionQuerySet(QuerySet):
    def likes(self):
        return self.filter(like=True)

    def dislikes(self):
        return self.filter(like=False)
