from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout

from .models import Question, Answer
from .forms import AskForm, AnswerForm, LoginForm, SignupForm


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginate_questions(request, qs):
    limit = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def new_questions(request):
    question_list = Question.objects.new()
    questions = paginate_questions(request, question_list)
    return render(request, 'new.html', {
        'questions': questions,
        'user': request.user,
        'session': request.session,
    })


def popular_questions(request):
    question_list = Question.objects.popular()
    questions = paginate_questions(request, question_list)
    return render(request, 'popular.html', {
        'questions': questions,
        'user': request.user,
        'session': request.session,
    })


def question_details(request, id = None):
    question = get_object_or_404(Question, id = id)
    answers = question.answer_set.all()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            answer = form.save()
            return HttpResponseRedirect(question.get_url())
    else:
        form = AnswerForm(initial = {'question': id})
    return render(request, 'question.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'user': request.user,
        'session': request.session,
    })


def ask_question(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {
        'form': form,
        'user': request.user,
        'session': request.session,
    })


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST['username']
            password = form.empty_password
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form,
        'user': request.user,
        'session': request.session,
    })


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'user': request.user,
        'session': request.session,
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
