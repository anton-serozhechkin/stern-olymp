from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from .forms import UserForm, SignUpStudentForm, UserAnswerForm
from .models import *
import json
import datetime
from django.contrib.auth import logout
from .optional_methods import getting_student, user_started_olymp, getting_user_in_event, strftime, finish_time_olymp, create_new_user_answer
from .controllers import PaymentController
from django.template.loader import render_to_string


def auth_user(request):
    """
        signin/signup view
        using django authenticate mechanism
    """
    if request.method == 'GET':
        req = request.GET
        if 'pwd' in req:
            if req.get('pwd', None):
                username = req.get('username')
                password = req.get('pwd')
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    return JsonResponse({'status': 'ok'})
                else:
                    return JsonResponse({'status': 'error', 'msg' : 'Неправильный логин или пароль'})
        if 'telephone_number' in req:
            if req.get('telephone_number', None):
                email = req.get('email', None)
                username = req.get('username', None)
                telephone_number = req.get('telephone_number', None)
                password = req.get('password', None)
                first_name = req.get('first_name', None)
                last_name = req.get('last_name', None)
                class_number = req.get('class_number', None)
                name_school = req.get('name_school', None)
                if not email or len(email) < 5:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле электронная почта'})
                elif not username or len(username) < 3:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле логин'})
                elif not telephone_number:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле телефонный номер'})
                elif not password:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле пароль'})
                elif not first_name:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле имя'})
                elif not last_name:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле фамилия'})
                elif not class_number or int(class_number) not in range(1, 12):
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле номер класса. Вводить нужно только сам номер(цифрой)'})
                elif not name_school:
                    return JsonResponse({'status': 'error', 'msg' : 'Заполните поле название школы'})
                elif User.objects.filter(username=username).exists():
                    return JsonResponse({'status': 'error', 'msg' : 'Логин уже занят'})
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'status': 'error', 'msg' : 'Электронная почта уже занята'})
                else:
                    new_user = User.objects.create_user(username=username, email=email,
                                                        first_name=first_name, last_name=last_name,
                                                        password=password)
                    user = User.objects.get(username=username)
                    class_number_get = ClassNumber.objects.get(name=class_number)
                    student = Student.objects.create(user=new_user, telephone_number=telephone_number,
                                                     class_number=class_number_get, name_school=name_school)
                    registration_text = settings.REGISTRATION_TEXT
                    hello_text = registration_text.format(username, password)
                    event_for_user = Event.objects.get(classes__name=class_number_get)
                    create_user_in_event = UserInEvent.objects.create(user=student, event=event_for_user,
                                               paid=False, date_registration=datetime.datetime.now())
                    auth.login(request, user)
                    if settings.START_SETTING == "PRODUCTION":
                        send_mail(
                        'Регистрация на онлайн олимпиаду',
                        hello_text,
                        settings.EMAIL_HOST_USER,
                        [email, ],
                        fail_silently=False)
                    return JsonResponse({'status': 'ok'})
    return render(request, 'core/index.html')


def redirect_index(request):
    return redirect('auth_user')


@login_required(login_url='/user/auth/')
def payment(request):
    """

    :param request: standard django param

    **Code**
        account - request username of current user

        desc - description of payment

        sum - dum of payment

        sign_string - collecting the necessary information for signature

        sign - readymade encrypted signature

    :return sign to unitpay server
    """
    student = UserInEvent.objects.get(user__user=request.user)
    if student.paid is False:
        if request.method == 'POST':
            controller = PaymentController(request)
            redirect_url = controller._prepare_post_responce()
            return redirect(redirect_url)
    else:
        return redirect(reverse('time_to_start', kwargs={'category_slug': student.event.category.slug, 'slug': student.event.slug}))
    return render(request, 'payment/payment.html', locals())


@login_required(login_url='/user/auth/')
def time_to_start(request, category_slug, slug):
    user_in_event = getting_user_in_event(request.user)
    if user_in_event.paid is False:
        return redirect('payment')
    else:
        if user_in_event.finish_olymp is True:
            return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
        else:
            time_start = Event.objects.get(slug=slug).data_event
            if datetime.datetime.now().timestamp() < time_start.timestamp():
                return render(request, 'core/timer.html', {'category_slug': category_slug, 'slug': slug, 'time_to_start': json.dumps(strftime(time_start))})
            else:
                return redirect(reverse('start_olympiad', kwargs={'category_slug': category_slug, 'slug': slug}))


@login_required(login_url='/user/auth/')
def final(request, category_slug, slug):
    finish_olymp = UserInEvent.objects.get(user__user=request.user)
    if finish_olymp.finish_olymp is False:
        finish_olymp.finish_olymp = True
        finish_olymp.save()
    return render(request, 'core/final.html', locals())


@login_required(login_url='/user/auth/')
def start_olympiad(request, category_slug, slug):
    student_in_event = getting_user_in_event(request.user)
    user_started = user_started_olymp(request.user)
    if student_in_event.paid is False:
        return redirect('payment')
    elif user_started:
        return redirect(reverse('question', kwargs={'category_slug': category_slug, 'slug': slug}))
    else:
        data = Event.objects.get(slug=slug)
        if 'start-modal-start' in request.POST:
            return redirect(reverse('question', kwargs={'category_slug': category_slug, 'slug': slug}))
    return render(request, 'core/start-olymp.html', locals())


@login_required(login_url='/user/auth/')
def question(request, category_slug, slug):    
    user_in_event = getting_user_in_event(request.user)
    if user_in_event.paid is False:
        return redirect('payment')
    else:
        if user_in_event.finish_olymp is False:
            student = getting_student(request.user)
            answered_questions = UserAnswer.objects.filter(student=request.user.student)
            questions = Question.objects.filter(event__slug=slug)
            event = Event.objects.get(slug=slug)
            finish_time = finish_time_olymp(user=request.user, event=event)
            if finish_time.timestamp() < datetime.datetime.now().timestamp():
                return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
            end_olymp_user = json.dumps(strftime(finish_time))
            if questions.count() == answered_questions.count():
               return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
            list_answered_questions = []
            if answered_questions:
                for answered_question in answered_questions:
                    list_answered_questions.append(answered_question.question.question)
                questions = Question.objects.filter(event__slug=slug).exclude(question__in=list_answered_questions)
            if request.method == "POST":
                if 'аштшыр-modal-start' in request.POST:
                    return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
                if request.POST.get('answer'):
                    answer = request.POST.get('answer')
                    question = Question.objects.get(pk=request.POST.get('id'))
                    create_new_user_answer(event, question, answer, student)
                else:
                    nothing_answer = 'Вы ничего не ответили'
                return redirect(reverse('question', kwargs={'category_slug': category_slug, 'slug': slug}))
        else:
            return redirect(reverse('final', kwargs={'category_slug': category_slug, 'slug': slug}))
    return render(request, 'core/olymp.html', locals())


def signout(request):
    logout(request)
    return redirect('auth_user')


def payment_check(request):
    """
    handler Unitay payment

    :param request: standard django param

    **Code**
        data - data from request UnitPay server

        method - status of payment

        payment - user from db
    :return json with message to user
    check this links:
    :https://github.com/unitpay/python-sdk
    :https://github.com/Underlor/unitpay_python_sdk

    """
    controller = PaymentController(request.GET)
    responce = controller._prepare_responce()
    return HttpResponse(responce, content_type='json')


@login_required(login_url='/user/auth/')
def bad_payment(request):
    """
    :param request: standard django param

        will be called if the UnitPay server
        response on the board is negative
    """
    return render(request, 'payment/bad-payment.html')


def documents(request):
    if request.user.is_authenticated:
        user_in_event = getting_user_in_event(request.user)
        return render(request, 'info/documents.html', {'user_in_event': user_in_event})
    else:
        return render(request, 'info/documents.html')


@login_required(login_url='/user/auth/')
def profile(request):
    user = User.objects.get(username=request.user.username)
    student = Student.objects.get(user=request.user)
    user_in_event = getting_user_in_event(request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = SignUpStudentForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            if user_form.has_changed():
                instance = user_form.save(commit=False)
                instance.username = user_form.cleaned_data['username']
                instance.last_name = user_form.cleaned_data['last_name']
                instance.first_name = user_form.cleaned_data['first_name']
                instance.email = user_form.cleaned_data['email']
                instance.save()
            if student_form.has_changed():
                instance = student_form.save(commit=False)
                instance.telephone_number = student_form.cleaned_data['telephone_number']
                if student.class_number.name != student_form.cleaned_data['class_number']:
                    if user_in_event.paid:
                        UserInEvent.objects.filter(user=student).delete()
                        event_for_user = Event.objects.get(classes__name=student_form.cleaned_data['class_number'])
                        create_user_in_event = UserInEvent.objects.create(user=student, event=event_for_user,
                                               paid=True, date_registration=datetime.datetime.now())
                    else:
                        UserInEvent.objects.filter(user=student).delete()
                        event_for_user = Event.objects.get(classes__name=student_form.cleaned_data['class_number'])
                        create_user_in_event = UserInEvent.objects.create(user=student, event=event_for_user,
                                               paid=False, date_registration=datetime.datetime.now())
                
                instance.class_number = student_form.cleaned_data['class_number']
                instance.name_school = student_form.cleaned_data['name_school']
                instance.save()
        else:
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        student_form = SignUpStudentForm(instance=student)
    return render(request, 'profile/profile.html', locals())


@login_required(login_url='/user/auth/')
def succes_payment(request):
    user_in_event = getting_user_in_event(request.user)
    user_in_event.paid = True
    user_in_event.save()
    return render(request, 'payment/success-payment.html', {'user_in_event': user_in_event})
    

def not_found_view(request, exception):
    exc = {'exception': exception}
    return render(request, 'errors/404.html', exc)


def error_view(request):
    return render(request, 'errors/500.html')


def permission_denied_view(request, exception):
    exc = {'exception': exception}
    return render(request, 'errors/403.html', exc)


def bad_request_view(request, exception):
    exc = {'exception': exception}
    return render(request, 'errors/400.html', exc)
