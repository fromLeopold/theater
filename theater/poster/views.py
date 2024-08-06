from collections import defaultdict
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import View

from poster.models import Performance, Session
from theater_info.core_utils import get_navigation_menu


class RepertoireView(View):
    """Репертуар"""

    def get(self, request):
        menu = get_navigation_menu(request.user)
        repertoire = Performance.objects.filter(repertoire=True)
        context = {
            "menu": menu,
            "repertoire_list": repertoire,
        }
        return render(request, "poster/repertoire.html", context=context)


class PerformanceSessionsView(View):
    """Сеансы на спектакль"""

    def get(self, request, slug):
        menu = get_navigation_menu(request.user)
        performance = get_object_or_404(Performance, url=slug)
        today = datetime.today()
        sessions = Session.objects.filter(performance=performance, date__gte=today).order_by("date")
        sessions_by_month = defaultdict(list)
        for session in sessions:
            month = session.date.strftime('%B')
            sessions_by_month[month].append(session)
        sessions_by_month = dict(sessions_by_month)
        context = {
            "menu": menu,
            "performance": performance,
            "session_dict_by_month": sessions_by_month,
        }
        return render(request, "poster/performance_sessions.html", context=context)


class AfishaView(View):
    """Афиша"""

    def get(self, request):
        menu = get_navigation_menu(request.user)
        today = datetime.today()
        sessions = Session.objects.filter(date__gte=today).order_by("date")
        context = {
            "menu": menu,
            "session_list": sessions,
        }
        return render(request, "poster/afisha.html", context=context)

