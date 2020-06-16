from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from app.models import Question, Answer, Tag, Like, Profile
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


def login(request):
  return render(request, 'login.html', { })


def signup(request):
  return render(request, 'signup.html', { })


def ask(request):
  return render(request, 'ask.html', { })


def hot(request):
  questions_, paginates_range = paginate(
              Question.objects.get_hot(),
              request.GET.get('page')
            )
  return render(request, 'hot.html', {
            'questions': questions_,
            'paginates': paginates_range,
          })


def index(request):
  questions_, paginates_range = paginate(
      Question.objects.all(),
      request.GET.get('page')
    )
  return render(request, 'index.html', {
            'questions': questions_,
            'paginates': paginates_range,
         })


def question(request, qid):
  question = get_object_or_404(Question, id = qid)
  answers_, paginates_range = paginate(
            Answer.objects.get_by_question(question),
            request.GET.get('page')
          )

  # print(question.answers_count)
  return render(request, 'question.html', {
          'question': question,
          'answers': answers_,
          'paginates': paginates_range,
         })


def tag(request, tag):
  tag = get_object_or_404(Tag, name = tag)
  questions_, paginates_range = paginate(
                        Question.objects.get_by_tag(tag),
                        request.GET.get('page')
                      )

  return render(request, 'tag.html', {
              'questions': questions_,
              'tag': tag,
              'paginates': paginates_range,
         })
