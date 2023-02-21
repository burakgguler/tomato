from django.contrib import admin

from address.models import City, Country, District, Township

admin.site.register(City)
admin.site.register(Country)
admin.site.register(District)
admin.site.register(Township)
