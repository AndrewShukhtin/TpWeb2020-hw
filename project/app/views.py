from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import render

HARD_CODE_answers = [
  {
    id : i,
    'text': 'Never gonna give you up \
             Never gonna let you down \
             Never gonna run around and desert you \
             Never gonna make you cry \
             Never gonna say goodbye \
             Never gonna tell a lie and hurt you',
  }
  for i in range(10)
]

HARD_CODE_questions = {
  i : {
    'id': i,
    'title': 'How to build a moon park?',
    'text': 'Lorem ipsum dolor sit amet, consectetur \
             adipiscing elit, sed do eiusmod tempor incididunt \
             ut labore et dolore magna aliqua Ut enim ad minim \
             veniam, quis nostrud exercitation ullamco laboris \
             nisi ut aliquip ex ea commodo consequat. Duis aute \
             irure dolor in reprehenderit in voluptate velit esse \
             cillum dolore eu fugiat nulla pariatur. Excepteur \
             sint occaecat cupidatat non proident, sunt in culpa \
             qui officia deserunt mollit anim id est laborum.',
    'tags': ['black-jack', 'bender'],
    'answers': [],
    'answers_count': 13,
    'likes_count': 7,
  }
  for i in range(25)
}


def paginate(objects_list, request):
  default_items_count_on_page = 8
  default_start = 1
  default_stop = len(objects_list) // default_items_count_on_page + 2
  if default_stop > 4:
    default_stop = 4

  page_number = request.GET.get('page')
  try:
    page_number = int(page_number)
  except:
    return objects_list[:default_items_count_on_page], \
            range(default_start, default_stop)

  if page_number <= 1:
    return objects_list[:default_items_count_on_page], \
            range(default_start, default_stop)

  start = (page_number - 1) * default_items_count_on_page
  stop = page_number * default_items_count_on_page

  if stop > len(objects_list):
    return objects_list[start:stop], \
            range(page_number - 1, page_number + 1)

  return objects_list[start:stop], \
        range(page_number - 1, page_number + 2)


def index(request):
  questions, paginates_range = paginate(list(HARD_CODE_questions.values()), request)
  return render(request, 'index.html', {
                         'questions': questions
                         'paginates': paginates_range,
  })


def login(request):
  return render(request, 'login.html', { })


def signup(request):
  return render(request, 'signup.html', { })


def ask(request):
  return render(request, 'ask.html', { })


def hot(request):
  questions, paginates_range = paginate(list(HARD_CODE_questions.values()), request)
  return render(request, 'hot.html', {
                         'questions': questions,
                         'paginates': paginates_range,
  })


def question(request, qid):
  question = HARD_CODE_questions.get(qid)
  answers, paginates_range = paginate(HARD_CODE_answers, request)
  return render(request, 'question.html', {
                         'question' : question,
                         'answers'  : answers,
                         'paginates': paginates_range,
  })


def tag(request, tag):
  questions_with_tags = list()
  for question in HARD_CODE_questions.values():
    if tag in question['tags']:
        questions_with_tags.append(question)

  questions, paginates_range = paginate(questions_with_tags, request)
  return render(request, 'tag.html', {
                         'questions' : questions,
                         'tag'       : tag,
                         'paginates' : paginates_range,
  })
