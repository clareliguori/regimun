from django.contrib import admin
from regimun_app.models import Conference, Committee, Country, School, \
    DelegatePosition, Delegate, FacultySponsor, FeeStructure

class ConferenceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Event information",{'fields': ['name','url_name','start_date','end_date','location']}),
        ("Organizer information",{'fields': ['organization_name','website_url','logo']}),
        ('Mailing Address', {'fields': ['address_line_1','address_line_2','city','state','zip','address_country']}),
    ]
    prepopulated_fields = {"url_name": ("name",)}

class CommitteeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url_name": ("name",)}

class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url_name": ("name",)}

class SchoolAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url_name": ("name",)}

admin.site.register(Conference, ConferenceAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(DelegatePosition)
admin.site.register(Delegate)
admin.site.register(FacultySponsor)
admin.site.register(FeeStructure)
