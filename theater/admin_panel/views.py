from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
import pdfkit

from admin_panel.recommendations_services import get_performances_popularity, get_time_popularity, \
    get_top_performances, get_least_popular_performances
from admin_panel.statistics_graph_services import *
from poster.models import Performance
from theater_info.core_utils import get_navigation_menu, admin_check


class AdminPanelView(View):
    """Страница администратора"""

    def get(self, request):
        if request.user.is_staff:
            if 'download' in request.GET:
                return self.generate_pdf(request)
            menu = get_navigation_menu(request.user)
            graphs = get_graphs_set()
            repertoire_list = Performance.objects.filter(repertoire=True)
            performances_popularity = get_performances_popularity()
            time_popularity = get_time_popularity()
            top_performances = get_top_performances()
            least_popular_performances = get_least_popular_performances()
            context = {
                "menu": menu,
                "graphs": graphs,
                "repertoire_list": repertoire_list,
                "performances_popularity": performances_popularity,
                "time_popularity": time_popularity,
                "top_performances": top_performances,
                "least_popular_performances": least_popular_performances,
            }
            return render(request, "admin_panel/admin_page.html", context=context)
        else:
            return redirect("main_page")

    def generate_pdf(self, request):
        repertoire_list = Performance.objects.filter(repertoire=True)
        performances_popularity = get_performances_popularity()
        time_popularity = get_time_popularity()
        top_performances = get_top_performances()
        least_popular_performances = get_least_popular_performances()
        context = {
            "repertoire_list": repertoire_list,
            "performances_popularity": performances_popularity,
            "time_popularity": time_popularity,
            "top_performances": top_performances,
            "least_popular_performances": least_popular_performances,
        }
        html_string = render_to_string('admin_panel/recommendations_pdf.html', context)
        pdf = pdfkit.from_string(html_string, False)

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="recommendations.pdf"'
        return response
