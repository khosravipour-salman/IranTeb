from django.contrib import admin
from .models import DoctorAddress, DoctorCity
from doctors.models import (
    DoctorUser, DoctorSpecialist, Telephone,
    CommentForDoctor, WeekDays, DoctorShift,
    DoctorExperoence,DoctorCity,DoctorAddress
)
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from doctors.forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()

admin.site.unregister(Group)
admin.site.register(DoctorSpecialist)
admin.site.register(Telephone)
admin.site.register(CommentForDoctor)
admin.site.register(WeekDays)
admin.site.register(DoctorShift)
admin.site.register(DoctorExperoence)
admin.site.register(DoctorCity)
admin.site.register(DoctorAddress)


class DoctorAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['first_name', 'last_name','full_name', 'email', 'phone_number','is_staff', 'is_active', 'date_joined', 'last_seen', ]    

    list_filter = ['is_staff']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name','full_name' ,'email', 'phone_number', 'visit_time','doctor_specialist','gender','city' )}),
        # ('Personal info', {'fields': ('phone_number', 'bio', 'profile_image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'last_seen', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'password_2',)}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


# admin.site.register(User, UserAdmin)
admin.site.register(DoctorUser, DoctorAdmin)