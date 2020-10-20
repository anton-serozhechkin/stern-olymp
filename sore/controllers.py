from django.conf import settings
import re
import json
from .models import UserInEvent
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
        if not params:
        	responce = self.__getErrorHandlerResponse('Пустые параметры')
        if not method in self._supportedPartnerMethods:
        	responce = self.__getErrorHandlerResponse('Метод не поддерживается')
        #signature = self.getSignature(params, method);
        #if params['signature'] != signature:
        #	raise Exception('Wrong signature')
        if not 'signature' in params:
            responce = self.__getErrorHandlerResponse('Не найдено подписи')
        if float(params['orderSum']) != float(settings.PRICE):
            responce = self.__getErrorHandlerResponse('Сумма оплаты и сумма услуги не совпадают')
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