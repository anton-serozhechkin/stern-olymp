from django.conf import settings
import re
import json
from .models import UserInEvent
from hashlib import sha256
from urllib.parse import urlencode
from django.contrib.auth.models import User
class PaymentController():
    
    def __init__(self, request):
        self._request = request
        self._supportedPartnerMethods = ['check', 'pay', 'error']
    
    
    def _prepare_responce(self):
        qs = self._request
        params = self.__parseParams(qs)
        method = self._request['method']
        if not 'method' in self._request:
        	responce = self.__getErrorHandlerResponse('Метод не определен')
        elif not params:
        	responce = self.__getErrorHandlerResponse('Пустые параметры')
        elif not method in self._supportedPartnerMethods:
        	responce = self.__getErrorHandlerResponse('Метод не поддерживается')
        elif params['signature'] != self.__getSignature(account=params['account'])[0]:
        	responce = self.__getErrorHandlerResponse('Неверная подпись')
        elif not 'signature' in params:
            responce = self.__getErrorHandlerResponse('Не найдено подписи')
        elif not User.objects.filter(username=params['account']):
            responce = self.__getErrorHandlerResponse('Такого пользователя не существует')
        elif float(params['orderSum']) != float(settings.PRICE):
            responce = self.__getErrorHandlerResponse('Сумма оплаты и сумма услуги не совпадают')
        else:
            responce = self._handler_request(method, params)
        return responce
        
    

    def _handler_request(self, method, params):
        if method == 'check':
            responce =self.__getSuccessHandlerResponse('Check Success. Ready to pay.')
        elif method == 'pay':
            user_in_event = UserInEvent.objects.get(user__user__username=params['account'])
            user_in_event.paid = True
            user_in_event.save()
            responce = self.__getSuccessHandlerResponse('Оплата успешна')
        elif method == 'error':
            responce = self.__getSuccessHandlerResponse('Произошла ошибка, попробуйте еще раз')
        return responce


    def __getErrorHandlerResponse(self, message):
        return json.dumps({'error': {'message': message}})


    def __getSuccessHandlerResponse(self, message):
        return json.dumps({'result': {'message': message}})


    def __parseParams(self, parametrs):
        params = {}
        for values in parametrs:
            if re.search('params', values):
                p = values[len('params['):-1]    
                params[p] = parametrs[values]
        return params
    
    
    def __getSignature(self, account=None):
        if not account:
            account = self._request.user.username
        separator = '{up}'
        params = {
            'account': account,
            'desc': settings.DESC,
            'sum': str(settings.PRICE),
        }
        sign_string = separator.join(['{}'.format(value) for (key, value) in params.items()])
        sign_string += separator + settings.SECRET_KEY_PAYMENT
        sign = sha256(sign_string.encode('utf-8')).hexdigest()
        return sign, params


    def _prepare_post_responce(self):
        sign, params = self.__getSignature()
        params.update({'signature': sign})
        params_string = urlencode(params)
        url = 'https://unitpay.ru/pay/{}?{}'
        redirect_url = url.format(settings.MERCHANT_ID, params_string)
        return redirect_url
