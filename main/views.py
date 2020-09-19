from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import donate_model, transaction_model
from .paytm import generate_checksum , verify_checksum
from django.conf import settings
from django.db.models import Q, Count
from django.contrib import messages
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    today = date.today()

    if request.POST.get('save'):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        '''if donate_model.objects.filter(Q(phone=phone), Q(email=email)).exists():
            donate_model.objects.create(name=name, phone=phone, email=email, amount=amount)
            messages.success(request, "Thank you for donating again")
            return redirect('/')

        else:'''

        donate_model.objects.create(name=name, phone=phone, email=email, amount=amount)
        transaction = transaction_model.objects.create(made_by=name, made_on=today,amount=amount)
        transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)
        transaction.checksum = checksum
        transaction.save()
        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'main/redirect.html', context=paytm_params)

    return render(request, 'main/index.html')

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'main/callback.html', context=received_data)
        return render(request, 'main/callback.html', context=received_data)

    return render(request, 'main/index.html')      