from django.http import HttpResponse
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
import random

from app.models import Question, Answer, Tag, Like, Profile
from app.forms import LoginForm, QuestionForm, RegisterForm, AnswerForm
from askme.settings import DEFAULT_ITEMS_COUNT_ON_PAGE


def paginate(objects_list, page_number):
  pag = Paginator(objects_list, DEFAULT_ITEMS_COUNT_ON_PAGE)
  try:
    page_number = int(page_number)
  except TypeError:
    return pag.page(1).object_list, pag.page_range

  if page_number < 1:
    return pag.page(1).object_list, pag.page_range

  return pag.page(page_number).object_list, pag.page_range


def get_random_color():
  return "#%02X%02X%02X" % (
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255),
  )


def get_top_tags():
  tags = \
  [
    {
      "name"  : i,
      "color" : get_random_color(),
      "size"  : random.randint(17, 23)
    } for i in Tag.objects.all()
  ]
  return tags


def get_top_members():
  members = [i.username for i in DjangoUser.objects.all()[:5]]
  return members


def signup(request):
  if request.method == "GET":
    form = RegisterForm()
  else:
    form = RegisterForm(data = request.POST)
    if form.is_valid():
      user = DjangoUser.objects.create_user(
              form.cleaned_data["username"],
              form.cleaned_data["email"],
              form.cleaned_data["password"]
            )
      user.is_superuser = False
      user.is_staff     = False
      user.save()
      Profile.objects.create(
          user = DjangoUser.objects.get(
              username = form.cleaned_data["username"]
            )
        )
      return redirect("/login")

    render(request, "signup.html", {
                    "form"    : form,
                    "tags"    : get_top_tags(),
                    "members" : get_top_members()
                  })

  return render(request, "signup.html", {
                    "form"    : form,
                    "tags"    : get_top_tags(),
                    "members" : get_top_members()
                  })


def login(request):
  if request.method == "GET":
    form = LoginForm()
  else:
    form = LoginForm(data=request.POST)
    if form.is_valid():
      user = auth.authenticate(request, **form.cleaned_data)
      if user is not None:
        auth.login(request, user)
        next_ = request.GET.get("next")
        return redirect(f"{next_}")

  ctx = {
      "form"    : form,
      "user"    : request.user,
      "tags"    : get_top_tags(),
      "members" : get_top_members(),
      "previous": request.META.get("HTTP_REFERER")
  }

  return render(request, "login.html", ctx)


@login_required
def ask(request):
  if request.method == "GET":
    form = QuestionForm()
    ctx = {
        "form"   : form,
        "user"   : request.user,
        "tags"   : get_top_tags(),
        "members": get_top_members()
    }
    return render(request, "ask.html", ctx)

  form = QuestionForm(data=request.POST)
  if form.is_valid():
    tags  = form.cleaned_data["tag"].split(" ")
    text  = form.cleaned_data["text"]
    title = form.cleaned_data["title"]
    question = Question.objects.create(
        author = request.user, text = text, title = title
    )
    tags_list = []
    for tag_name in tags:
      try:
        tag = Tag.objects.get(name = tag_name)
      except Tag.DoesNotExist:
        tag = Tag.objects.create(name = tag_name)
      tags_list.append(tag)
    # print(tags)
    question.tags.set(tags_list)
    question.save()
    return redirect(reverse("question", kwargs={"qid": question.pk}))

  ctx = {
      "form"   : form,
      "user"   : request.user,
      "tags"   : get_top_tags(),
      "members": get_top_members(),
  }

  return render(request, "ask.html", ctx)


@login_required
def logout_view(request):
  previous = request.META.get("HTTP_REFERER")
  logout(request)
  return redirect(previous)


def hot(request):
  questions, paginates_range = paginate(
            Question.objects.get_hot(),
            request.GET.get("page")
          )

  return render(request, "hot.html", {
      "questions": questions,
      "paginates": paginates_range,
      "user"     : request.user,
      "tags"     : get_top_tags(),
      "members"  : get_top_members(),
  })


def index(request):
  questions, paginates_range = paginate(
        Question.objects.all(),
        request.GET.get("page")
      )

  return render(request, "index.html", {
    "questions": questions,
    "paginates": paginates_range,
    "user"     : request.user,
    "tags"     : get_top_tags(),
    "members"  : get_top_members(),
  })


def question(request, qid):
  question = get_object_or_404(Question, id=qid)
  if request.method == "GET":
    form = AnswerForm()
  else:
    form = AnswerForm(data = request.POST)
    if form.is_valid() and request.user.is_authenticated:
      Answer.objects.create(
          text     = form.cleaned_data["field"],
          author   = request.user,
          question = question
      )

  answers = Answer.objects.get_by_question(question)
  return render(request, "question.html", {
                "form"     : form,
                "question" : question,
                "answers"  : answers,
                "user"     : request.user,
                "tags"     : get_top_tags(),
                "members"  : get_top_members(),
              })


def tag(request, tag):
  tag = get_object_or_404(Tag, name=tag)
  questions, paginates_range = paginate(
      Question.objects.get_by_tag(tag), request.GET.get("page"))

  return render(request, "tag.html", {
                "questions"   : questions,
                "tag"         : tag,
                "paginates"   : paginates_range,
                "user"        : request.user,
                "tags"        : get_top_tags(),
                "members"     : get_top_members(),
  })
