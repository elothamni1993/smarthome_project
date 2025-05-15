from django.shortcuts import render, redirect
from django import template


def home(request):
    return render(request, 'smarthome/home.html')

device_states = {
    'lights': {
        'living_room': False,
        'kitchen': False,
        'bedroom': True,
        'bathroom': False,
    }
}

from datetime import datetime
import pytz

from django.shortcuts import render, redirect
from datetime import datetime

device_states = {
    'lights': {
        'living_room': False,
        'kitchen': False,
        'bedroom': True,
        'bathroom': False,
    }
}

def lights_view(request):
    now = datetime.now()
    hour = now.hour
    current_time = now.strftime('%H:%M')

    # Auto-mode: si entre 8h et 18h, éteindre tout
    auto_mode = 8 <= hour < 18
    if auto_mode:
        for room in device_states['lights']:
            device_states['lights'][room] = False

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'on_all':
            for room in device_states['lights']:
                device_states['lights'][room] = True
        elif action == 'off_all':
            for room in device_states['lights']:
                device_states['lights'][room] = False
        else:
            room = request.POST.get('room')
            if room in device_states['lights']:
                device_states['lights'][room] = not device_states['lights'][room]
        return redirect('lights')

    return render(request, 'smarthome/lights.html', {
        'lights': device_states['lights'],
        'current_time': current_time,
        'auto_mode': auto_mode
    })



def curtains_view(request):
    return render(request, 'smarthome/curtains.html')


def pool_view(request):
    if 'pool' not in request.session:
        request.session['pool'] = {
            'level': 60,
            'temperature': 25,
            'target_temperature': 28,
            'heater_on': False,
            'heater_type': 'electrique'
        }

    pool_state = request.session['pool']
    pool_state.setdefault('target_temperature', 28)

    if request.method == 'POST':
        if 'refill' in request.POST:
            pool_state['level'] = min(pool_state['level'] + 10, 100)
        elif 'drain' in request.POST:
            pool_state['level'] = max(pool_state['level'] - 10, 0)
        elif 'temperature' in request.POST:
            pool_state['target_temperature'] = int(request.POST['temperature'])
        elif 'toggle_heater' in request.POST:
            pool_state['heater_on'] = not pool_state.get('heater_on', False)
        elif 'heater_type' in request.POST:
            pool_state['heater_type'] = request.POST['heater_type']

    # Simulation du chauffage
    if pool_state['heater_on'] and pool_state['temperature'] < pool_state['target_temperature']:
        pool_state['temperature'] += 0.2
    elif pool_state['temperature'] >= pool_state['target_temperature']:
        pool_state['heater_on'] = False  # Désactiver le chauffage

    request.session['pool'] = pool_state
    return render(request, 'smarthome/pool.html', {'pool': pool_state})



# État global de la porte (ouvert = True, fermé = False)
garage_state = {
    'door_open': False
}

door_state = {'open': False}

def garage_view(request):
    if request.method == 'POST':
        door_state['open'] = not door_state['open']
        return redirect('garage')
    return render(request, 'smarthome/garage.html', {
        'door_open': door_state['open']
    })
