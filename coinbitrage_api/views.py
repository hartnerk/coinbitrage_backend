from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import AlertSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.http import HttpResponse, JsonResponse
from .models import Alert
import json
from django.core.serializers import serialize 
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from .forms import AlertForm
from django.views.decorators.csrf import csrf_exempt  
import requests
import os
from twilio.rest import Client
import os
import environ

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
X_CW_API_KEY = os.environ['X_CW_API_KEY']
PHONE_NUMBER = os.environ['PHONE_NUMBER']

# Create your views here.
@api_view(['GET'])
def get_alerts(request):
    data={'token': request.headers['Authorization'].split(' ')[1]}
    try:
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        request.user = user
    except ValidationError as v:
        print("validation error", v)
    user = User.objects.get(id=user.id)
    data = user.alerts.all()
    new_data = json.loads(serialize('json', data))
    return JsonResponse(data=new_data, safe=False)

def get_alert_by_id(request, alert_id):
    data={'token': request.headers['Authorization'].split(' ')[1]}
    try:
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        request.user = user
    except ValidationError as v:
        print("validation error", v)
    user = User.objects.get(id=user.id)
    data = user.alerts.filter(id=alert_id)
    new_data = json.loads(serialize('json', data))
    return JsonResponse(data=new_data, status=200, safe=False)
    
@csrf_exempt
def new_alert(request):
    if request.method=='POST':
        data = json.load(request)  
        form = AlertForm(data)
        if form.is_valid():
            alert_form = form.save(commit=False)
            form.save()
            new_data = json.loads(serialize('json', [alert_form]))
            return JsonResponse(data=new_data, status=200, safe=False)
            
@csrf_exempt
def edit_alert(request, alert_id):
    data={'token': request.headers['Authorization'].split(' ')[1]}
    try:
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        request.user = user
    except ValidationError as v:
        print("validation error", v)
    user = User.objects.get(id=user.id)
    alert = user.alerts.get(id=alert_id)
    if request.method =='POST':
        data = json.load(request)
        form = AlertForm(data, instance=alert)
        if form.is_valid():
            alert_form = form.save(commit=False)
            form.save()
            new_data = json.loads(serialize('json', [alert_form]))
            return JsonResponse(data=new_data, status=200, safe=False)

@csrf_exempt
def delete_alert(request, alert_id):
    data={'token': request.headers['Authorization'].split(' ')[1]}
    try:
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        request.user = user
    except ValidationError as v:
        print("validation error", v)
    user = User.objects.get(id=user.id)
    alert = user.alerts.get(id=alert_id)
    if request.method == 'POST':
        alert.delete()
        return JsonResponse(data={'status': 'Successfully deleted Alert'}, status=200)

def sendText(exchange_array, user):
    user = User.objects.get(id=user.id)
    data = user.alerts.all()
    all_alerts = json.loads(serialize('json', data))
    for alert in all_alerts:
        if((exchange_array['exachnge_prices'][0]['coin']==(alert['fields']['coin'].lower()+'usd'))and(alert['fields']['enabled'])):
            valueone=exchange_array['exachnge_prices'][0]['rate']
            valuetwo=exchange_array['exachnge_prices'][-1]['rate']
            if(((valuetwo-valueone)/((valueone+valuetwo)/2)*100)>alert['fields']['threshold']):
                print(account_sid)
                print(auth_token)
                client = Client(account_sid, auth_token)
                message = client.messages.create(  
                                            messaging_service_sid='MG5450e28b8d71ce150a530845df0caa76',
                                            body='well',       
                                            to=PHONE_NUMBER
                                        ) 
                print(message.sid)
    return 



def get_biggest_dif(updated_prices_json, coin_id):
    coin_id = coin_id.lower()
    exachnge_prices=[]
    exchange_obj={
        "exchange": '',
        "coin": '',
        "rate": ''
    }
    for result in updated_prices_json['result']:
        resultsplit=result.split(':')
        if(resultsplit[0]=='market' and resultsplit[2]==coin_id.lower()+'usd'):
            exchange_obj['exchange']=resultsplit[1]
            exchange_obj['coin']=resultsplit[2]
            exchange_obj['rate']=updated_prices_json['result'][result]
            temp=json.dumps(exchange_obj)
            exachnge_prices.append(json.loads(temp))
    exachnge_prices.sort(key = lambda x: x['rate'])
    if(len(exachnge_prices)>0):
        return {"exachnge_prices": exachnge_prices}
    else:
        return{"exachnge_prices": 'API does not support: '+coin_id}


def best_arbitrage(request, coin_id):
    data={'token': request.headers['Authorization'].split(' ')[1]}
    try:
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        request.user = user
    except ValidationError as v:
        print("validation error", v)
    
    header={'X-CW-API-Key': X_CW_API_KEY}

    r = requests.get('https://api.cryptowat.ch/markets/prices',  headers=header)
    json_response = r.json()
    if r.status_code == 200:
        biggest_dif_response = get_biggest_dif(json_response, coin_id)
        sendText(biggest_dif_response, user )
        return JsonResponse(biggest_dif_response, safe=False)
    else:
        return HttpResponse('Could not get data')

