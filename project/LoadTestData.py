import os
import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "askme.settings")
django.setup()

from app.models import Question, Like, Answer, Tag, Profile
from django.contrib.auth.models import User
from datetime import datetime

user              = User.objects.create_user(
                      'vendroid',
                      password = 'vaxkax1488'
                    )
user.is_superuser = False
user.is_staff     = False
user.save()

user              = User.objects.create_user(
                      'snegovik',
                      password = 'nintendoswitch'
                    )
user.is_superuser = False
user.is_staff     = False
user.save()

Profile.objects.create(
    user   = User.objects.get(username = "vendroid"),
    avatar = "/img/me.jpg"
  )

Profile.objects.create(
    user   = User.objects.get(username = "snegovik"),
    avatar = "/img/snegovik.jpeg"
  )

for i in range(10):
  Tag.objects.create(name=('tag' + str(i)))

for i in range(20):
  Question.objects.create(
    id    = i,
    title = 'Где купить Nintendo Switch?',
    text  = 'Был я значит на аниме фестивале, и мне представилась \
             возможность опробовать епонский чудодевайс -- Nintendo Switch. \
             Где можно его приобрести подешевле? \
             Как же хочется поиграть в Зельду...',

    author    = User.objects.get(username = "snegovik"),
    is_active = True
    ).tags.set(
        Tag.objects.filter(name=('tag' + str(i % 10 + 1)))
      )


for i in range(20):
  Answer.objects.create(
    text     = 'Зачем тебе свич, если ты все равно постоянно играешь в Европку...',
    question = Question.objects.get(id = i),
    author   = User.objects.get(username = "vendroid"),
  )

for i in range(20):
  Like.objects.create(
    user = User.objects.get(username = "snegovik"),
    content_object = Question.objects.get(id = i)
  )

for i in range(1, 21):
  Like.objects.create(
    user = User.objects.get(username = "vendroid"),
    content_object = Answer.objects.get(id = i)
  )

