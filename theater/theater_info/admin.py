from django.contrib import admin

from theater_info.models import *


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


class HallAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'theater']


class HallSectorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class SeatAdmin(admin.ModelAdmin):
    ordering = ('hall', 'row', 'place')
    search_fields = ('hall__name', 'row', 'place', 'standard_price')


class TroupeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'last_name', 'first_name',
                    'middle_name', 'title', 'art_group', 'actor']


# admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(HallSector, HallSectorAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Troupe, TroupeAdmin)
