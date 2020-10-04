from .models import Student, UserInEvent

def getting_student(user):
    student = Student.objects.get(user=user)
    return student

def getting_user_in_event(student):
    user_in_event = UserInEvent.objects.get(user__user=student)
    return user_in_event