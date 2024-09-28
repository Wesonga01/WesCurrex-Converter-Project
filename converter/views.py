import requests
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request, 'converter/home.html')

def get_exchange_rate(api_key, base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if target_currency in data['conversion_rates']:
            return data['conversion_rates'][target_currency]
        else:
            raise ValueError(f"Target currency {target_currency} not found in response.")
    else:
        raise ValueError(f"Error fetching data: {response.status_code}")

def convert_currency(request):
    if request.method == 'POST':
        base_currency = request.POST['base_currency']
        target_currency = request.POST['target_currency']
        amount = float(request.POST['amount'])

        api_key = "f2ba033c19a79a7064ce0b1e"

        try:
            rate = get_exchange_rate(api_key, base_currency, target_currency)
            converted_amount = amount * rate
            return JsonResponse({'converted_amount': converted_amount, 'rate': rate})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'converter/home.html')
