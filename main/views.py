import requests
import os
from django.shortcuts import render, redirect
from dotenv import load_dotenv

from django.shortcuts import render, get_object_or_404
from .models import Case
from django.db.models import Case as DCase, When, Value, IntegerField
from collections import defaultdict


home_cases = (
    Case.objects.filter(is_published=True, show_on_home=True)
    .annotate(
        home_sort=DCase(
            When(home_position__in=[1, 2, 3], then="home_position"),
            default=Value(99),
            output_field=IntegerField(),
        )
    )
    .order_by("home_sort", "created_at")
)


def index(request):
    home_cases = (
        Case.objects.filter(is_published=True, show_on_home=True)
        .order_by("home_position", "created_at")
    )
    return render(request, "index.html", {"home_cases": home_cases})

def services(request):
    return render(request, 'services.html')

def works(request):
    qs = (
        Case.objects.filter(is_published=True, show_on_works=True, works_position__in=[1, 2, 3])
        .order_by("works_block", "works_position", "created_at")
    )

    buckets = defaultdict(list)
    for c in qs:
        buckets[c.works_block].append(c)

    works_blocks = [buckets[k] for k in sorted(buckets.keys())]

    return render(request, "our-works.html", {"works_blocks": works_blocks})

def techimpuls(request):
    return render(request, 'techimpuls.html')

def triphouse(request):
    return render(request, 'triphouse.html')

def moloko(request):
    return render(request, "moloko.html")

def bookingrent(request):
    return render(request, "bookingrent.html")

def sdelkipro(request):
    return render(request, "sdelkipro.html")


def case_detail(request, slug):
    case = get_object_or_404(Case.objects.prefetch_related("images"), slug=slug, is_published=True)
    return render(request, "case-detail.html", {"case": case})

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def contact_form(request):
    if request.method == "POST":

        name = request.POST.get("name")
        surname = request.POST.get("surname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        company = request.POST.get("company")
        description = request.POST.get("desk_project")

        message = f"""
Новая заявка с сайта PlumIT:

Имя: {name}
Фамилия: {surname}
Телефон: {phone}
Email: {email}
Компания: {company}

Описание:
{description}
"""

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })

        return redirect('home')