from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserSafetyForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import paho.mqtt.client as mqtt
import certifi
import time
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def home(request):
    return render(request, 'user/home.html')
    
@login_required
def push(request):
    def on_publish(client,userdata,result):
        print("data published \n")
        pass


    def on_message(client,userdata, msg):
        print("response: " + str(msg.payload))
        time.sleep(4)
        client.publish('STEM/1/CRX-401/student',payload=msg.payload)

    client = mqtt.Client()
    client.on_publish = on_publish
    client.tls_set(ca_certs=certifi.where())

    client.username_pw_set('solace-cloud-client', 'chhe5o2afe2pdvu66oj6tgd05k')
    client.connect('mr-connection-pi5rgecxa7b.messaging.solace.cloud',port=8443)
    time.sleep(4)
    client.publish('STEM/1/CRX-401/student',payload='Are you safe')
    client.subscribe('response')

    client.on_message=on_message
    return render(request, 'user/success.html')



@csrf_exempt
def get_response(request):
  if request.method == 'POST':
    response = request.POST.get('response', '')
    id = request.user.employee.id
    employee = Employee.objects.get(id=id)
    if response == "true":
        print('HERE')
        employee.safe = True
        employee.save()
    else:
        print("NO HERE")
        employee.safe = False
        employee.save()
    
    # return render(request, 'user/success.html')
    return redirect('success')
  else:
    return redirect('success')

    # return render(request, 'user/success.html')

@login_required
def safety_reset(request):
    Employee.objects.filter(safe=True).update(safe=False)
    return redirect('safety')

@login_required
def safety(request):
    safe_users = Employee.objects.filter(safe=True)
    non_safe_users = Employee.objects.filter(safe=False)
    print(len(safe_users), len(non_safe_users))
    count_non_safe = len(non_safe_users)
    count_safe = len(safe_users)
    context = {
        'safe' : safe_users,
        'not_safe' : non_safe_users,
        'count_safe' : count_safe,
        'count_not_safe' : count_non_safe,
    }
    return render(request, 'user/safety.html', context = context)

@login_required
def success(request):
    return render(request, 'user/success.html')

@login_required
def subscription(request):
    if request.method == 'POST':
        subscription_data = json.loads(request.body.decode('utf-8'))
        print(subscription_data)
        return JsonResponse({'success': True})
    return render(request, 'user/success.html')

# # @login_required
# def respond(request, pk):
#     if request.method == "POST":
#         safeForm = UserSafetyForm(request.POST, instance=Employee.objects.get(id=pk))
#         if safeForm.is_valid():
#             safeForm.save()
#             return redirect(f'/respond/{pk}')
#     else:
#         safeForm = UserSafetyForm(instance=Employee.objects.get(id=pk))
#     return render(request, 'user/respond.html', {"safeForm": safeForm})


@login_required
def respond(request):
    if request.method == "POST":
        safeForm = UserSafetyForm(request.POST, instance=request.user.employee)
        if safeForm.is_valid():
            safeForm.save()
            return redirect(f'/respond')
    else:
        safeForm = UserSafetyForm(instance=request.user.employee)
    return render(request, 'user/respond.html', {"safeForm": safeForm})

def register(request):
    if request.method == "POST":
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            return redirect('user-home')
    else:
        u_form = UserRegisterForm()

    return render(request, 'user/register.html', {"u_form": u_form})


