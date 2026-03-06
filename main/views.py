import requests
import os
from collections import defaultdict

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from dotenv import load_dotenv
from django.db.models import Case as DCase, When, Value, IntegerField

from .models import Case


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
    return render(request, "services.html")


def _get_works_blocks():
    qs = (
        Case.objects.filter(
            is_published=True,
            show_on_works=True,
            works_position__in=[1, 2, 3],
        )
        .order_by("works_block", "works_position", "created_at")
    )

    buckets = defaultdict(list)
    for case in qs:
        buckets[case.works_block].append(case)

    return [buckets[k] for k in sorted(buckets.keys())]


def works(request):
    works_blocks = _get_works_blocks()

    limit = 1
    visible_blocks = works_blocks[:limit]
    has_more = len(visible_blocks) < len(works_blocks)

    return render(
        request,
        "our-works.html",
        {
            "works_blocks": visible_blocks,
            "has_more": has_more,
            "next_offset": limit,
        },
    )


def works_load_more(request):
    works_blocks = _get_works_blocks()

    limit = 1
    offset = int(request.GET.get("offset", 0))

    new_blocks = works_blocks[offset:offset + limit]
    next_offset = offset + limit
    has_more = next_offset < len(works_blocks)

    html = render_to_string(
        "includes/works_blocks.html",
        {"works_blocks": new_blocks},
        request=request,
    )

    return JsonResponse(
        {
            "html": html,
            "has_more": has_more,
            "next_offset": next_offset,
        }
    )


def techimpuls(request):
    return render(request, "techimpuls.html")


def triphouse(request):
    return render(request, "triphouse.html")


def moloko(request):
    return render(request, "moloko.html")


def bookingrent(request):
    return render(request, "bookingrent.html")


def sdelkipro(request):
    return render(request, "sdelkipro.html")


def case_detail(request, slug):
    case = get_object_or_404(
        Case.objects.prefetch_related("images"),
        slug=slug,
        is_published=True,
    )
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

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
            },
        )

        return redirect("home")
