from django.http import HttpResponse, JsonResponse
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
import random
import urllib

from app.models import Question, Answer, Tag, Like, Profile
from app.forms import LoginForm, QuestionForm, RegisterForm, AnswerForm, SettingsForm
from askme.settings import DEFAULT_ITEMS_COUNT_ON_PAGE, MEDIA_URL, MEDIA_ROOT, BASE_AVATAR


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

def upload_image(file, user_id):
  with open(MEDIA_ROOT+f"/img/{user_id}", "wb+") as f:
    for chunk in file.chunks():
      f.write(chunk)

  return f"img/{user_id}"


def change_photos(user):
  for question in Question.objects.filter(author = user):
    question.save()
  for answer in Answer.objects.filter(author = user):
    answer.save()


def signup(request):
  if request.method == "GET":
    form = RegisterForm()
  else:
    form = RegisterForm(data = request.POST, files = request.FILES)
    if form.is_valid():
      user = DjangoUser.objects.create_user(
          form.cleaned_data["username"],
          form.cleaned_data["email"],
          form.cleaned_data["password"])
      user.is_superuser = False
      user.is_staff     = False
      user.save()

      if form.cleaned_data["avatar"]:
        image_path = upload_image(form.cleaned_data["avatar"], user.id)
      else:
        image_path = BASE_AVATAR

      Profile.objects.create(
          user     = DjangoUser.objects.get(
          username = form.cleaned_data["username"]),
          avatar   = image_path
      )

      return redirect("/login")

  return render(request, "signup.html", {
          "form"      : form,
          "tags"      : get_top_tags(),
          "members"   : get_top_members(),
          "MEDIA_URL" : MEDIA_URL,
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

  return render(request, "login.html", {
            "form"     : form,
            "user"     : request.user,
            "tags"     : get_top_tags(),
            "members"  : get_top_members(),
            "previous" : request.META.get("HTTP_REFERER"),
            "MEDIA_URL": MEDIA_URL,
          })


@login_required
def ask(request):
  if request.method == "GET":
    form = QuestionForm()
  else:
    form = QuestionForm(data=request.POST)
    if form.is_valid():
      tags  = form.cleaned_data["tag"].split(" ")
      text  = form.cleaned_data["text"]
      title = form.cleaned_data["title"]
      question = Question.objects.create(
          author = request.user,
          text   = text,
          title  = title
      )

      tags_list = []
      for tag_name in tags:
        try:
          tag = Tag.objects.get(name = tag_name)
        except Tag.DoesNotExist:
          tag = Tag.objects.create(name = tag_name)
        tags_list.append(tag)
      question.tags.set(tags_list)
      question.save()

      return redirect(reverse("question", kwargs={"qid": question.pk}))

  return render(request, "ask.html", {
            "form"      : form,
            "user"      : request.user,
            "tags"      : get_top_tags(),
            "members"   : get_top_members(),
            "MEDIA_URL" : MEDIA_URL
          })


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


def base(request):
    return redirect("index/")


def index(request):
  questions, paginates_range = paginate(
        Question.objects.all(),
        request.GET.get("page")
      )

  return render(request, "index.html", {
    "questions" : questions,
    "paginates" : paginates_range,
    "user"      : request.user,
    "tags"      : get_top_tags(),
    "members"   : get_top_members(),
    "MEDIA_URL" : MEDIA_URL,
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
                      "form"      : form,
                      "question"  : question,
                      "answers"   : answers,
                      "is_owner"  : (question.author == request.user),
                      "user"      : request.user,
                      "tags"      : get_top_tags(),
                      "members"   : get_top_members(),
                      "MEDIA_URL" : MEDIA_URL,
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
                "MEDIA_URL": MEDIA_URL,
              })


@login_required
def settings(request):
  if request.method == "GET":
    form = SettingsForm(initial = {
        "username" : request.user.username,
        "email"    : request.user.email
    })
  else:
    form = SettingsForm(data = request.POST, files = request.FILES)
    if form.is_valid():
      user = request.user
      if form.cleaned_data["username"] != user.username:
          user.username = form.cleaned_data["username"]
      if form.cleaned_data["email"] != user.email:
          user.email = form.cleaned_data["email"]
      if form.cleaned_data["password"]:
          user.set_password(form.cleaned_data["password"])
      if form.cleaned_data["avatar"]:
        profile = Profile.objects.get(user=user)
        new_photo = upload_image(form.cleaned_data["avatar"], user.id)
        if profile.avatar == BASE_AVATAR:
          flag = True
        profile.avatar = new_photo
        profile.save()
        if flag:
          change_photos(user)
      user.save()

  return render(request, "settings.html", {
              "form"      : form,
              "user"      : request.user,
              "tags"      : get_top_tags(),
              "members"   : get_top_members(),
              "avatar"    : Profile.objects.get(user = request.user).avatar,
              "MEDIA_URL" : MEDIA_URL,
          })


@login_required
def ajax(request):
  qid = int(request.POST.get("id"))
  type_ = request.POST.get("type")

  if type_ == "question":
    object_class = Question
  elif type_ == "answer":
    object_class = Answer

  object_ = get_object_or_404(object_class, id=qid)
  if object_.likes.filter(user = request.user).count() == 0:
    like = Like(
        user           = request.user,
        content_object = object_class.objects.get(id=qid)
    )
    like.save()
    object_.likes_count += 1
    object_.save()
  return JsonResponse({
      "likes_count": object_.likes_count,
  })


@login_required
def corect_ajax(request):
  qid = int(request.POST.get("id"))
  answer = get_object_or_404(Answer, id=qid)
  if answer.author == request.user:
    answer.is_correct = True
    answer.save()

    return JsonResponse({
        "is_correct": True,
    })
  else:
    return JsonResponse({
        "is_correct": False,
    })
