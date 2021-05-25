from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, response
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import time
from datetime import date
from django.db.models import Max, Min

from .models import User, Response, Pay_method, Category, Type, Additional, Transport, Deal
from .forms import NewUserForm, LoginForm, NewTransportForm
# Create your views here.

global local_transport
local_transport = {}

def search(f):
    def wrapper(request, *args, **kwargs):
        if request.GET.get('search_button') == 'SEARCH':
            # Creating dict for rendering search page
            instance = {}
            categoryes = Category.objects.all().order_by('pk')
            instance['categoryes'] = categoryes
            types = Type.objects.all().order_by('pk')
            instance['types'] = types

            # Get data from request
            location = request.GET['location'].upper()
            start_date_input = request.GET['start_date']
            end_date_input = request.GET['end_date']
            try:
                start_date = date.fromisoformat(start_date_input)
                end_date = date.fromisoformat(end_date_input)
            except:
                instance['error'] = 'Enter date in right format.'
                return render(request, 'transport/search.html', instance)

            if start_date < date.today() or end_date < date.today() or start_date >= end_date:
                instance['error'] = "You can't rent transport in the past!"
                return render(request, 'transport/search.html', instance)

            # How many days transport will be rented
            time_delta = end_date - start_date
            instance['time_delta'] = time_delta.days
            request.session['time_delta'] = time_delta.days

            # !!!!CEnge for filtering
            # Price range
            max_price = Transport.objects.aggregate(Max('price_per_day'))['price_per_day__max']
            min_price = Transport.objects.aggregate(Min('price_per_day'))['price_per_day__min']
            instance['max_price'] = max_price * time_delta.days
            instance['min_price'] = min_price * time_delta.days

            # Filtering
            filtered_transports = []
            all_transport = Transport.objects.all().order_by('-timestamp')
            for transport in all_transport:
                if location in transport.pick_up_location:
                    filtered_transports.append(transport)

            all_deals = Deal.objects.all()
            for deal in all_deals:
                if (deal.start_date <= start_date and end_date <= deal.close_date) or (start_date <= deal.start_date and deal.close_date <= end_date) or \
                    (deal.start_date <= start_date <= deal.close_date) or (deal.start_date <= end_date <= deal.close_date):
                    if deal.rent_transport in filtered_transports:
                        filtered_transports.remove(deal.rent_transport)
            

            #offers = [((transport.price_per_day * time_delta.days), transport) for transport in filtered_transports]
            offers = []
            for transport in filtered_transports:
                total_price = transport.price_per_day * time_delta.days
                ratings =[response.rating for response in transport.owner.received_responses.all()]
                responses_count = len(ratings)
                owner_rating = round((sum(ratings) / len(ratings)), 1)
                offers.append((owner_rating, responses_count,  total_price, transport))

            # Save result in global variable for filters
            global local_transport
            local_transport[request.user.pk] = offers

            instance['offers'] = offers
            return render(request, 'transport/search.html', instance)
        return f(request, *args, **kwargs)
    return wrapper

@search
def index(request):
    return render(request, 'transport/index.html')

def login_view(request):
    instance = {}
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            instance['error'] = "Invalid username and/or password."
            return render(request, "transport/login.html", instance)

    instance['form'] = LoginForm()
    return render(request, "transport/login.html", instance)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    instance = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmarion = request.POST['confirmation']
        email = request.POST['email']
        phone = request.POST['phone']

        if password != confirmarion:
            instance['error'] = "Passwords must match."
            return render(request, 'transport/login.html', instance)

        try:
            user = User.objects.create_user(username, email, password, phone=phone)
            #user.save()
        except IntegrityError:
            instance['error'] = "User already exists."
            return render(request, "network/register.html", instance)

        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    instance['form'] = NewUserForm()
    return render(request, 'transport/register.html', instance)

#!!!!!  add order
def get_offers(request):

    # Get start and end points
    start = int(request.GET.get('start') or 0)
    end = int(request.GET.get('end') or (start + 9))

    # Generate lists of offers
    data = []
    for offer in Transport.objects.all().order_by('-timestamp'):
        timestamp = offer.timestamp
        timestamp = timestamp.strftime('%b %d, %Y, %#I:%M %p')
        offer_data = {
            'id': offer.pk,
            'name': offer.name,
            'description': offer.description,
            'price_per_day': offer.price_per_day,
            'photo': 'media/' + offer.photo.name,
            'pick_up_location': offer.pick_up_location,
            'timestamp': timestamp
        }
        data.append(offer_data)

    # Artificially delay speed of response 
    time.sleep(1)

    # Return list of offers
    return JsonResponse({
        'offers': data
    }, status=200)

@login_required(login_url='login')
def add_offer(request):
    instance = {}
    
    if request.method == 'POST':
        form = NewTransportForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            try: 
                category = Category.objects.get(pk=form.cleaned_data['category'])
                type = Type.objects.get(pk=form.cleaned_data['type'])
            except: 
                    instance['error'] = 'Category and Type need to be entered.'
                    return render(request, 'transport/add_offer.html', instance)
            passenger_places = form.cleaned_data['passenger_places']
            baggage_places = form.cleaned_data['baggage_places']
            air_conditioner = form.cleaned_data['air_conditioner']
            automat_gearbox = form.cleaned_data['automat_gearbox']
            pick_up_location = form.cleaned_data['pick_up_location'].upper()
            price_per_day = form.cleaned_data['price_per_day']
            owner = request.user
            photo = request.FILES['photo']
            new_tr = Transport(name=name, description=description, category=category, type=type, pick_up_location=pick_up_location, \
                price_per_day=price_per_day, owner=owner, passenger_places=passenger_places, baggage_places=baggage_places, air_conditioner=air_conditioner, automat_gearbox=automat_gearbox, photo=photo)
            new_tr.save()
            instance['message'] = 'SUCCESS'
            return render(request, 'transport/add_offer.html', instance)
        instance['error'] = 'Invalid Input'
        return render(request, 'transport/add_offer.html', instance)
    instance['form'] = NewTransportForm()
    return render(request, 'transport/add_offer.html', instance)

# delete in the end
@search
def search_view(request):
    instance = {}
    categoryes = Category.objects.all().order_by('pk')
    instance['categoryes'] = categoryes
    types = Type.objects.all().order_by('pk')
    instance['types'] = types
    return render(request, 'transport/search.html', instance)

def offer_filter(request):
    global local_transport

    # Get order
    try:
        order = request.GET['order'].split('-')
        order_by = order[0]
        order_reverse = (order[1] == 'True')
    except: pass

    # Filtering prosess
    filters = request.GET['filters'].split(',')
    if not request.GET['filters']:
        filters = [category.category_name for category in Category.objects.all()] + [type.type_name for type in Type.objects.all()]
    filtered_transport = []
    local_transport_for_filtering = local_transport[request.user.pk]
    for owner_rating, responses_count, total_price, transport in local_transport_for_filtering:
        if (transport.category.category_name in filters) or (transport.type.type_name in filters):
            filtered_transport.append((owner_rating, responses_count, total_price, transport))

    # Construct data for response
    data_unsorted = []
    for owner_rating, responses_count, total_price, offer in filtered_transport:
        timestamp = offer.timestamp
        timestamp = timestamp.strftime('%b %d, %Y, %#I:%M %p')
        offer_data = {
            'id': offer.pk,
            'name': offer.name,
            'description': offer.description,
            'price_per_day': offer.price_per_day,
            'photo': 'media/' + offer.photo.name,
            'pick_up_location': offer.pick_up_location,
            'timestamp': timestamp,
            'time_delta': request.session['time_delta'],
            'total_price': total_price, 
            'owner_rating': owner_rating,
            'responses_count': responses_count
        }
        data_unsorted.append(offer_data)
    try:
        data = sorted(data_unsorted, key=lambda k: k[order_by], reverse=order_reverse)
    except: data = data_unsorted
    time.sleep(1)
    return JsonResponse({
        'offers' : data
    })
    
def details_view(request, transport_id):
    instance = {}
    offer = Transport.objects.get(pk=transport_id)
    instance['offer'] = offer

    if request.method == 'POST':
        rent_transport = offer
        owner = offer.owner
        client = request.user
        #start_date
        #close_date
        #additionals
        #total_price
        #pay_method

    # Find already reserved dates
    reserved_dates = [(deal.start_date, deal.close_date) for deal in offer.deals.all()]
    instance['reserved_dates'] = reserved_dates

    # Add aditionals
    adds = Additional.objects.all()
    instance['adds'] = adds

    # Get owner rating
    ratings =[response.rating for response in offer.owner.received_responses.all()]
    responses_count = len(ratings)
    owner_rating = round((sum(ratings) / len(ratings)), 1)
    instance['responses_count'] = responses_count
    instance['owner_rating'] = owner_rating

    return render(request, 'transport/details.html', instance)


