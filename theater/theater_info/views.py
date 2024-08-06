from django.shortcuts import render
from django.views import View

from theater_info.core_utils import get_navigation_menu
from theater_info.models import Theater, Troupe


class MainPageView(View):
    """Главная страница театра"""

    def get(self, request):
        menu = get_navigation_menu(request.user)

        context = {
            "menu": menu,
        }
        return render(request, "theater_info/main_page.html", context=context)


class TheaterInfoView(View):
    """Информация о кинотеатре"""

    def get(self, request):
        menu = get_navigation_menu(request.user)
        theaters = Theater.objects.all()
        context = {
            "menu": menu,
            "theater_list": theaters,
        }
        return render(request, "theater_info/theater_contacts.html", context=context)


class TroupeView(View):
    """Труппа кинотеатра"""

    def get(self, request):
        menu = get_navigation_menu(request.user)
        actors = Troupe.objects.filter(actor=True)
        art_group = Troupe.objects.filter(art_group=True)
        context = {
            "menu": menu,
            "actor_list": actors,
            "art_group_list": art_group,
        }
        return render(request, "theater_info/troupe.html", context=context)


class TroupeMemberView(View):
    """Член труппы"""

    def get(self, request, pk):
        menu = get_navigation_menu(request.user)
        member = Troupe.objects.get(pk=pk)
        context = {
            "menu": menu,
            'member': member,
        }
        return render(request, "theater_info/troupe_member_details.html", context=context)
