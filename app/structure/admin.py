from django.contrib import admin
from .models import *
from .forms import *
from cms.admin.placeholderadmin import PlaceholderAdminMixin

class PhoneOtdelInline(admin.TabularInline):
    model = Phone
    exclude = ['sotrudnik']
    extra = 0

class PhoneSotrudnikInline(admin.TabularInline):
    model = Phone
    exclude = ['otdel']
    extra = 0

@admin.register(CategoryOrganization)
class OrganizationAdmin(admin.ModelAdmin):
    # form = COrganizationForm
    list_display = ('name', )
    exclude = []

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm
    list_display = ('leveled_name', 'order', )
    exclude = ['level', 'list_order']

@admin.register(Otdel)
class OtdelAdmin(admin.ModelAdmin):
    form = OtdelForm
    inlines = (PhoneOtdelInline, )
    list_display = ('name', 'organization', 'order', )
    list_filter = ["organization" ]

@admin.register(Sotrudnik)
class SotrudnikAdmin(admin.ModelAdmin):
    form = SotrudnikForm
    inlines = (PhoneSotrudnikInline, )
    list_display = ('name', 'organization', 'otdel', 'order', )
    list_filter = ["organization", "otdel"]

class PhotoDepartmentInline(admin.TabularInline):
    model = PhotoDepartment
    exclude = ['order']
    extra = 3

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'activity')
    list_filter = ["organization", "activity"]
    exclude = []
    inlines = (PhotoDepartmentInline, )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', )
    exclude = []
# @admin.register(Phone)
# class PhoneAdmin(admin.ModelAdmin):
    # form = PhoneForm