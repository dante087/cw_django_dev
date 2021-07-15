from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from survey.models import Question, Answer, Review


class QuestionListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Question

    def get_queryset(self):
        return super().get_queryset()[:20]


class QuestionCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Question
    fields = ['title', 'description']
    success_url = reverse_lazy('survey:question-list')

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


@login_required(login_url=reverse_lazy('login'))
def answer_question(request):
    question_pk = request.POST.get('question_pk')
    print(request.POST)
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer, created = Answer.objects.get_or_create(question=question, author=request.user)
    answer.value = request.POST.get('value')
    answer.save()
    return JsonResponse({'ok': True})


@login_required(login_url=reverse_lazy('login'))
def like_dislike_question(request):
    question_pk = request.POST.get('question_pk')
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    # TODO: Dar Like
    value = request.POST.get('value')
    if value:
        like = True if value == 'like' else False
        review, created = Review.objects.get_or_create(question=question, author=request.user)
        review.like = like if like != review.like else None
        review.save()

    return JsonResponse({'ok': True})

