from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Register)

admin.site.register(Products)

admin.site.register(mycart)

admin.site.register(Wishlist)

# admin.site.register(Single_Booking)
#
# admin.site.register(Multiple_Booking)

admin.site.register(Order)

admin.site.register(orderitem)

admin.site.register(Join)

admin.site.register(alert)

admin.site.register(profilepic)


admin.site.register(PasswordReset)