from django.shortcuts import render , get_object_or_404
from third.models import Restaurant

from django.core.paginator import Paginator;
from third.forms import RestaurantForm
from django.http import HttpResponseRedirect


def list(request) :
    
    restaurant = Restaurant.objects.all()
    paginator = Paginator(restaurant, 5)

    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = {
        'restaurants' : items
    }

    return render(request, 'third/list.html', context)


def detail(request, id) :
    restaurant = get_object_or_404(Restaurant, id=id)

    context = {
        'restaurant' : restaurant
    }

    return render(request, 'third/detail.html', context)

#C:

def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list/')
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form' : form})

#D: 데이터의 pk값을 입력받아 삭제하는 서비스
def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    item.delete()
    return HttpResponseRedirect('/third/list/')

def update(request):
    if request.method == 'POST' and 'id' in request.POST:
        item = Restaurant.objects.get(pk=request.POST.get('id'))
        form = RestaurantForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
    elif request.method == 'GET':
        item = Restaurant.objects.get(pk=request.GET.get('id'))
        form = RestaurantForm(instance=item)
        return render(request, 'third/update.html', {'form' : form})
    return HttpResponseRedirect('/third/list/')