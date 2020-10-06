from .models import Student, UserInEvent, StartOlymp, Answer, UserAnswer
import datetime


def getting_student(user):
    student = Student.objects.get(user=user)
    return student


def getting_user_in_event(student):
    user_in_event = UserInEvent.objects.get(user__user=student)
    return user_in_event


def strftime(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


def finish_time_olymp(user, event):
    student = getting_student(user)
    if student.class_number.name in range(1, 3):
        end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    elif student.class_number.name in range(3, 9):
        end_time = datetime.datetime.now() + datetime.timedelta(hours=1, minutes=30)
    else:
        end_time = datetime.datetime.now() + datetime.timedelta(hours=2)
    if not StartOlymp.objects.filter(user__username=user.username).exists():
        finish_time = StartOlymp.objects.create(user=user, event=event,
                                  start_time=datetime.datetime.now(),
                                  end_time=end_time)
    else:
        finish_time = StartOlymp.objects.get(event=event, user=user)
    return finish_time.end_time


def create_new_user_answer(event, question, answer, student):
    exist_answer = Answer.objects.filter(event=event, question=question,
                                         text=answer.lower()).exists()
    if exist_answer:
        UserAnswer.objects.create(question=question, student=student,
                                  answer=answer, correct=True)
        student.count += question.count_balls
        student.save()
    else:
        UserAnswer.objects.create(question=question, student=student,
                                  answer=answer, correct=False)
