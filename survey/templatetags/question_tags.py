from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def user_value(context, question):
    answer = question.answers.filter(author=context.request.user).first()
    return answer.value if answer else 0


@register.simple_tag(takes_context=True)
def user_likes(context, question):
    review = question.reviews.filter(author=context.request.user, like=True).first()
    return True if review else False


@register.simple_tag(takes_context=True)
def user_dislikes(context, question):
    review = question.reviews.filter(author=context.request.user, like=False).first()
    return True if review else False
