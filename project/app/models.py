from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


def answer_helper(answer):
  answer.likes_count = len(LikeForAnswer.objects.filter(answer=answer))
  answer.photo = Profile.objects.get(user = answer.author).avatar
  return answer


def question_helper(question):
  question.answers_count = len(Answer.objects.filter(question=question))
  question.likes_count = len(LikeForQuestion.objects.filter(like=question))
  question.photo = Profile.objects.get(user = question.author).avatar
  return question


class Profile(models.Model):
  user = models.OneToOneField(
    User,
    on_delete = models.CASCADE,
    db_index  = True
  )

  avatar = models.CharField(
    max_length = 90,
    default="/img/me.jpg"
  )


class Tag(models.Model):
  name = models.CharField(
    max_length   = 50,
    verbose_name = u"Tag"
  )

  def __str__(self):
      return self.name


class QuestionManager(models.Manager):
  def get_by_tag(self, tag):
    return super().get_queryset().filter(tags=tag)

  def get_hot(self):
    hotest = map(question_helper, super().get_queryset())
    return sorted(hotest, 
      key = lambda question: question.answers_count, 
      reverse=True
    )


class Question(models.Model):
  title = models.CharField(
      max_length   = 100,
      verbose_name = u"Заголовок вопроса..."
    )

  text  = models.CharField(
      max_length   = 1000,
      verbose_name = u"Поле вопроса..."
    )

  create_date = models.DateTimeField(
      default      = datetime.now,
      verbose_name = u"Время создания вопроса"
    )

  likes_count = models.PositiveIntegerField(
      default = 0
    )

  answer_count = models.PositiveIntegerField(
      default = 0
    )

  author = models.ForeignKey(
      User,
      on_delete = models.CASCADE,
      db_index = True
    )

  tags = models.ManyToManyField(
    Tag,
    db_index = True
  )

  def __unicode__(self):
    return self.title

  class Meta:
    ordering = ['-create_date']


class AnswerManager(models.Manager):
    def get_by_question(self, question):
        return super().get_queryset().filter(question=question)


class Answer(models.Model):
  text = models.TextField(
    verbose_name=u"Поле ответа..."
  )

  question = models.ForeignKey(
    Question,
    on_delete=models.CASCADE,
    db_index=True
  )

  author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    db_index=True
  )

  objects = AnswerManager()


class LikeForAnswer(models.Model):
  user = models.ForeignKey(
    User,
    on_delete   = models.CASCADE,
    related_name= "User"
  )

  answer = models.ForeignKey(
    Answer,
    on_delete    = models.CASCADE,
    related_name ="Answer"
  )


class LikeForQuestion(models.Model):
  user = models.ForeignKey(
    User,
    on_delete = models.CASCADE,
    db_index  = True
  )

  like = models.ForeignKey(
    Question,
    on_delete = models.CASCADE,
    db_index  = True
  )
