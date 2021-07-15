from django.db.models.signals import post_save
from django.dispatch import receiver
from survey.models import Question, Answer, Review


@receiver(post_save, sender=Answer)
def update_ranking(sender, instance, created, **kwargs):
    instance.question.update_ranking()


@receiver(post_save, sender=Review)
def update_ranking(sender, instance, created, **kwargs):
    instance.question.update_ranking()


@receiver(post_save, sender=Question)
def update_ranking(sender, instance, created, **kwargs):
    if instance.ranking != instance.calculate_ranking():
        instance.update_ranking()
