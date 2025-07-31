from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import FavoriteFoods
from .tasks import get_favorite_foods

@login_required
def veggies(request):
    veggy_items = FavoriteFoods.objects.filter(veggy=True)

    data = [{"favorite_foods": item.foods} for item in veggy_items]

    return_data = {
        "vegitarians": data,
        "total": veggy_items.count()
    }
    return JsonResponse(return_data, safe=False)


@login_required
def foods(request):
    food_items = FavoriteFoods.objects.all()

    data = [{
        "question": item.question,
        "answer": item.answer,
        "favorite_foods": item.foods, 
        "vegitarian": item.veggy
        } 
        for item in food_items]

    return_data = {
        "foods": data,
        "total": food_items.count()
    }
    return JsonResponse(return_data, safe=False)


@login_required
def schedule_favorite_foods(request):
    amount_str = request.GET.get("amount")

    get_favorite_foods(int(amount_str) if amount_str else 100)
    
    return JsonResponse({"scheduled": True})