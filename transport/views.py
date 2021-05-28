from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import time
from datetime import date, timedelta
from django.db.models import Max, Min

from .models import User, Response, Pay_method, Category, Type, Additional, Transport, Deal
from .forms import NewUserForm, LoginForm, NewTransportForm, NewReviewForm 

# Create your views here.
global local_transport
local_transport = {}

def search(f):
    def wrapper(request, *args, **kwargs):
        if request.GET.get('search_button'):
            # Creating dict for rendering search page
            instance = {}
            categoryes = Category.objects.all().order_by('pk')
            instance['categoryes'] = categoryes
            types = Type.objects.all().order_by('pk')
            instance['types'] = types

            # Get data from request
            location = request.GET.get('location', '').upper()
            start_date_input = request.GET.get('start_date', date.today().isoformat())
            end_date_input = request.GET.get('end_date', (date.today() + timedelta(days=1)).isoformat())
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
            
            offers = []
            for transport in filtered_transports:
                total_price = transport.price_per_day * time_delta.days
                ratings =[response.rating for response in transport.owner.received_responses.all()]
                responses_count = len(ratings)
                try: owner_rating = round((sum(ratings) / len(ratings)), 1)
                except: owner_rating = 1.0
                offers.append((owner_rating, responses_count,  total_price, transport))

            instance['offers'] = offers

            # Save result in global variable for filters
            global local_transport
            local_transport[request.user.pk] = offers
            
            return render(request, 'transport/search.html', instance)
        return f(request, *args, **kwargs)
    return wrapper

@search
def index(request):
    return render(request, 'transport/index.html')

@search
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

@search
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@search
def register(request):
    instance = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmarion = request.POST['confirmation']
        email = request.POST['email']
        phone = request.POST['phone']
        adress = request.POST.get('adress', False)
        about = request.POST.get('about', False)
        if password != confirmarion:
            instance['error'] = "Passwords must match."
            return render(request, 'transport/login.html', instance)

        try:
            user = User.objects.create_user(username, email, password, phone=phone, adress=adress, about=about)
            #user.save()
        except IntegrityError:
            instance['error'] = "User already exists."
            return render(request, "network/register.html", instance)

        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    instance['form'] = NewUserForm()
    return render(request, 'transport/register.html', instance)

@search
def get_offers(request):

    offers = Transport.objects.all()
    count_rating_offer = []
    for offer in offers:
        ratings = [response.rating for response in offer.owner.received_responses.all()]
        responses_count = len(ratings)
        try: owner_rating = round((sum(ratings) / len(ratings)), 1)
        except: owner_rating = 1.0
        count_rating_offer.append((responses_count, owner_rating, offer))

    # Generate lists of offers
    data_unsorted = []
    for rating_count, owner_rating, offer in count_rating_offer:
        timestamp = offer.timestamp
        timestamp = timestamp.strftime('%b %d, %Y, %#I:%M %p')
        offer_data = {
            'id': offer.pk,
            'name': offer.name,
            'description': offer.description,
            'price_per_day': offer.price_per_day,
            'photo': 'media/' + offer.photo.name,
            'pick_up_location': offer.pick_up_location,
            'passenger_places': offer.passenger_places,
            'air_conditioner': offer.air_conditioner,
            'baggage_places': offer.baggage_places,
            'automat_gearbox': offer.automat_gearbox,
            'timestamp': timestamp,
            'details': f'/details/{offer.pk}',
            'rating_count': rating_count,
            'owner_rating': owner_rating,
            'owner_page': f'/user/{offer.owner.pk}'
        }
        data_unsorted.append(offer_data)

    # Get start and end points for data portion
    start = int(request.GET.get('start') or 0)
    end = int(request.GET.get('end') or (start + 9))
    order = (request.GET.get('order') or 'timestamp.True').split('.')
    orde_value = order[0]
    reverse_value = (order[1] == 'True')

    if end > Transport.objects.count(): 
        end = Transport.objects.count()

    # Data sorting
    try:
        data = sorted(data_unsorted, key=lambda k: k[orde_value], reverse=reverse_value)
    except: pass

    data_portion = []
    for offer_index in range(start-1, end):
        data_portion.append(data[offer_index])

    # Artificially delay speed of response 
    time.sleep(0.5)

    # Return list of offers
    return JsonResponse({
        'offers': data_portion,
        'max': len(data)
    }, status=200)

@search
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
            instance['form'] = NewTransportForm()
            instance['message'] = 'SUCCESS'
            return render(request, 'transport/add_offer.html', instance)
        instance['error'] = 'Invalid Input'
        return render(request, 'transport/add_offer.html', instance)
    instance['form'] = NewTransportForm()
    return render(request, 'transport/add_offer.html', instance)

@search
def search_view(request):
    instance = {}
    categoryes = Category.objects.all().order_by('pk')
    instance['categoryes'] = categoryes
    types = Type.objects.all().order_by('pk')
    instance['types'] = types
    return render(request, 'transport/search.html', instance)

@search
def offer_filter(request):
    global local_transpor
    # Get order
    try:
        order = request.GET['order'].split('-')
        order_by = order[0]
        order_reverse = (order[1] == 'True')
    except: pass

    # Filtering prosess
    filters = request.GET['filters'].split(',')
    if not request.GET['filters']:
        filters = [f"cat_{category.pk}" for category in Category.objects.all()] + [f"type_{type.pk}" for type in Type.objects.all()]
    filtered_transport = []
    local_transport_for_filtering = local_transport[request.user.pk]
    for owner_rating, responses_count, total_price, transport in local_transport_for_filtering:
        if (f"cat_{transport.category.pk}" in filters) or (f"type_{transport.type.pk}" in filters):
            filtered_transport.append((owner_rating, responses_count, total_price, transport))

    # Get max-min price from filtered_transport
    filtered_transport_prices = [total_price for owner_rating, responses_count, total_price, transport in filtered_transport]
    try:
        filtered_max_price = max(filtered_transport_prices)
        filtered_min_price = min(filtered_transport_prices)
    except:
        filtered_max_price = 0
        filtered_min_price = 0

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
            'responses_count': responses_count,
            'passenger_places': offer.passenger_places,
            'air_conditioner': offer.air_conditioner,
            'baggage_places': offer.baggage_places,
            'automat_gearbox': offer.automat_gearbox,
            'owner': offer.owner.username,
            'details': f'/details/{offer.pk}',
            'owner_page': f'/user/{offer.owner.pk}'
        }
        data_unsorted.append(offer_data)
    try:
        data = sorted(data_unsorted, key=lambda k: k[order_by], reverse=order_reverse)
    except: data = data_unsorted
    time.sleep(0.5)
    return JsonResponse({
        'offers' : data,
        'max_price': filtered_max_price,
        'min_price': filtered_min_price
    }, status=200)

@search
@login_required(login_url='login')    
def details_view(request, transport_id):
    instance = {}
    offer = Transport.objects.get(pk=transport_id)
    instance['offer'] = offer

    # Find already reserved dates
    reserved_dates = [(deal.start_date, deal.close_date) for deal in offer.deals.all()]
    for start_date, close_date in reserved_dates:
        if close_date < date.today():
            reserved_dates.remove((start_date, close_date))
    instance['reserved_dates'] = reserved_dates

    # Add aditionals
    adds = Additional.objects.all()
    instance['adds'] = adds

    # Add pay_methods
    pay_methods = Pay_method.objects.all()
    instance['pay_methods'] = pay_methods

    # Get owner rating
    ratings =[response.rating for response in offer.owner.received_responses.all()]
    responses_count = len(ratings)
    try: owner_rating = round((sum(ratings) / len(ratings)), 1)
    except: owner_rating = 1.0
    instance['responses_count'] = responses_count
    instance['owner_rating'] = owner_rating

    # Creating Deal
    if request.method == 'POST':
        rent_transport = offer
        owner = offer.owner
        client = request.user
        deliver_to = request.POST.get('deliver_to', False)
        pick_up_from = request.POST.get('pick_up_from', False)
        total_price = request.POST['total']

        if not request.POST.get('pay_method', False):
            instance['error'] = 'Pay method needs to be choosen.'
            return render(request, 'transport/details.html', instance)
        pay_method = Pay_method.objects.get(pk=request.POST["pay_method"])

        try:
            start_date = date.fromisoformat(request.POST['details_start_date'])
            close_date = date.fromisoformat(request.POST['details_end_date'])
        except: 
            instance['error'] = '"Pick-up" date and "Drop-off" date need to be entered.'
            return render(request, 'transport/details.html', instance)
        
        # Get aditionals from post
        additionals = []
        for add in adds:
            if request.POST.get(f'add_{add.pk}', False):
                additionals.append(add.pk)

        # Insert data to the Deal table
        try:
            Deal.objects.create(rent_transport=rent_transport, owner=owner, client=client, start_date=start_date, close_date=close_date, \
                deliver_to=deliver_to, pick_up_from=pick_up_from, total_price=total_price, pay_method=pay_method)
        except:
            instance['error'] = "Insert error"
            return render(request, 'transport/details.html', instance)

        # If success
        instance['transport'] = offer
        return render(request, 'transport/success.html', instance)
    return render(request, 'transport/details.html', instance)

@search
@login_required(login_url='login') 
def user_view(request, id):
    instance = {}
    user_page_info = User.objects.get(pk=id)
    instance['user_page_info'] = user_page_info

    # Get owner rating
    ratings =[response.rating for response in user_page_info.received_responses.all()]
    responses_count = len(ratings)
    try: owner_rating = round((sum(ratings) / len(ratings)), 1)
    except ZeroDivisionError: owner_rating = 1.0
    instance['responses_count'] = responses_count
    instance['owner_rating'] = owner_rating

    offers = Transport.objects.filter(owner=user_page_info)
    instance['offers'] = offers

    deals = Deal.objects.all()
    offer_deals = [(offer, offer.deals.all()) for offer in offers]
    filtered_offer_deals =[]
    for offer, deals in offer_deals:
        filtered_deals = []
        for deal in deals:
            if deal.start_date > date.today():
                filtered_deals.append(deal)
        filtered_offer_deals.append((offer, filtered_deals))
    instance['transport_deals'] = filtered_offer_deals

    reviews = Response.objects.filter(on_user=user_page_info).order_by("-timestamp")
    instance['reviews'] = reviews

    if request.GET.get('review_inp'):
        if request.method == 'POST':
            text = request.POST['text']
            rating = request.POST['rating']
            author = request.user
            on_user = user_page_info
            try: Response.objects.create(text=text, rating=rating, author=author, on_user=on_user)
            except: 
                instance["error"] = "Insert error"
                return render(request, 'transport/new_review.html', instance)
            return HttpResponseRedirect(f'/user/{user_page_info.pk}')
        instance['user_page_info'] = user_page_info
        instance['form'] = NewReviewForm()
        return render(request, 'transport/new_review.html', instance)

    return render(request, 'transport/user_page.html', instance)
