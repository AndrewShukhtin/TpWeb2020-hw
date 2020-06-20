from django.db import models as DjangoDBModels
from django.contrib.auth import models as DjangoAuthModels
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from datetime import datetime


class Profile(DjangoDBModels.Model):
  user = DjangoDBModels.OneToOneField(
    DjangoAuthModels.User,
    on_delete = DjangoDBModels.CASCADE,
    db_index  = True
  )

  avatar = DjangoDBModels.CharField(
    max_length = 90,
  )


class Tag(DjangoDBModels.Model):
  name = DjangoDBModels.CharField(
    max_length   = 50,
    verbose_name = u"Tag",
    unique       = True,
  )

  def __str__(self):
    return self.name


class Like(DjangoDBModels.Model):
  content_type = DjangoDBModels.ForeignKey(
      ContentType,
      on_delete=DjangoDBModels.CASCADE
  )

  object_id = DjangoDBModels.PositiveIntegerField()

  content_object = GenericForeignKey('content_type', 'object_id')

  def save(self, *args, **kwargs):
    self.content_object.like(self)
    super(Like, self).save(*args, **kwargs)

  user = DjangoDBModels.ForeignKey(
      DjangoAuthModels.User,
      on_delete=DjangoDBModels.CASCADE,
      db_index=True
  )


class QuestionManager(DjangoDBModels.Manager):
  def get_by_tag(self, tag):
    return super().get_queryset().filter(tags = tag)

  def get_hot(self):
    return super().get_queryset().order_by('-likes_count')


class Question(DjangoDBModels.Model):
  title = DjangoDBModels.CharField(
    max_length   = 100,
    verbose_name = u"Заголовок вопроса"
  )

  text = DjangoDBModels.CharField(
    max_length   = 1000,
    verbose_name = u"Поле вопроса..."
  )

  likes = GenericRelation(Like, related_query_name = 'question')

  create_date = DjangoDBModels.DateTimeField(
    default      = datetime.now,
    verbose_name = u"Время создания вопроса"
  )

  is_active = DjangoDBModels.BooleanField(
    default      = True,
    verbose_name = u"Доступность вопроса"
  )

  likes_count = DjangoDBModels.PositiveIntegerField(
    default = 0
  )

  answers_count = DjangoDBModels.PositiveIntegerField(
    default = 0
  )

  author = DjangoDBModels.ForeignKey(
    DjangoAuthModels.User,
    on_delete = DjangoDBModels.CASCADE,
    db_index  = True
  )

  tags = DjangoDBModels.ManyToManyField(
    Tag,
    db_index = True
  )

  photo = DjangoDBModels.CharField(
    default     = u"/img/snegovik.jpeg",
    max_length  = 120
  )

  objects = QuestionManager()

  def like(self, like_object):
    if like_object not in Like.objects.all():
      self.likes_count += 1
    self.save()

  def add_answer(self, answer_object):
    if answer_object not in Question.objects.all():
      self.answers_count += 1
      self.save()

  def __unicode__(self):
    return self.title

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    self.photo = Profile.objects.get(user = self.author).avatar
    super(Question, self).save(*args, **kwargs)


  class Meta:
    ordering = ['-create_date']


class AnswerManager(DjangoDBModels.Manager):
  def get_by_question(self, question):
    return super().get_queryset().filter(question = question)


class Answer(DjangoDBModels.Model):
  text = DjangoDBModels.TextField(verbose_name = u"Поле ответа....")

  likes_count = DjangoDBModels.PositiveIntegerField(default = 0)

  photo = DjangoDBModels.CharField(default = u"/img/me.jpg",
                           max_length = 120)

  is_correct = DjangoDBModels.BooleanField(default = False)

  likes = GenericRelation(Like, related_query_name = 'answer')

  question = DjangoDBModels.ForeignKey(
    Question,
    on_delete = DjangoDBModels.CASCADE,
    db_index  = True
  )

  author = DjangoDBModels.ForeignKey(
    DjangoAuthModels.User,
    on_delete = DjangoDBModels.CASCADE,
    db_index  = True
  )

  objects = AnswerManager()

  def save(self, *args, **kwargs):
    self.question.add_answer(self)
    self.photo = Profile.objects.get(user = self.author).avatar
    super(Answer, self).save(*args, **kwargs)

  def like(self, like_object):
    if like_object not in Like.objects.all():
      self.likes_count += 1
      super(Answer, self).save()
