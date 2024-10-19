"""
URL configuration for bags project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,),

    #---------------------------HOMEPAGE--------------------------
    path('about',views.about),
    path('coming',views.coming),
    path('contact',views.contact),
    path('shop', views.shop),

    #------------------------LOGIN-----------------------------
    path('login',views.login),


    #--------------------------LOGOUT---------------------------

    path('logout', views.logout),

    #------------------------REGISTER--------------------------
    path('register',views.register),
    path('r1',views.r1),

    path('single/<int:id>/', views.single, name='single'),

    # --------------- SINGLE BOOKING -----------------
    path('singles/<int:d>/', views.singles, name='single'),
    path('single_booking/<int:product_id>', views.single_booking, name='single_booking'),
    path('single_razor/<int:product_id>', views.single_razor, name='single_razor'),
    path('razor_pay/<int:price>', views.razorpaycheck),
    path('success', views.success, name='success'),

# --------------- MULTIPLE BOOKING -----------------
    path('checkout', views.checkout, name='checkout'),
    path('multiple_booking',views.multiple_booking, name='multiple_booking'),
    path('multiple_razor', views.multiple_razor, name='multiple_razor'),
    path('razor_pay2', views.razorpaycheck2),
    # path('success2',views.success2, name='success2'),

# --------------- FORGOT/RESET PASSWORD -----------------
    path('forgot', views.forgot_password_user, name="forgot"),
    path('reset/<token>', views.reset_password_user, name='reset_password'),



#---------------------USER----------------------
    path('userhome',views.userhome),
    path('user_about',views.user_about),
    path('user_collection',views.user_collection),
    path('user_contact',views.user_contact),
    path('user_orders', views.user_orders),

#---------------------ADMIN-----------------------
    path('adminhome',views.adminhome),
    path('addcollection',views.addcollection),
    path('viewuser',views.viewuser),
    path('view_deliveryboy',views.view_deliveryboy),
    path('delete_del/<int:id>',views.delete_del),
    path('booking',views.userbooking),
    path('statusup/<wal>', views.statusup, name="statusup"),
    path('product_details',views.product_details),
    path('delete/<int:id>',views.delete),
    path('update/<int:id>',views.update),
    path('updating/<int:id>',views.updating),
    path('updis',views.updis),
#----------------------CART-------------------------
    path('viewcart',views.viewcart),
    path('cart/<int:d>',views.cart1),
    path('update_cart',views.update_cart),
    path('delete_cart/<int:d>',views.delete_cart),
    path('minuscart/<int:de>',views.minuscart),
    path('pluscart/<int:de>',views.pluscart),


#-----------------------WISHLIST---------------------
    path('wishlist/<int:d>',views.wishlist),
    path('view_wishlist',views.view_wishlist),
    path('delete_wishlist/<int:d>',views.delete_wishlist),

#------------------------PROFILE------------------------
    path('usr_profile',views.usr_profile),
    path('pro_edit/<int:id>',views.pro_edit),
    path('profile_edit/<int:id>',views.profile_edit),

#-----------------------employee-------------------

    path('join', views.join),
    path('jr', views.jr),
    path('del_home', views.del_home),
    path('emp_cash', views.emp_cash),
    path('del_orders', views.del_orders),
    # path('volapcard', views.volapcard),
    path('del_profile',views.del_profile),
    path('del_profile_update', views.del_profile_update),
    # path('emp_chnagepassword/<int:d>', views.emp_chnagepassword),
    # path('stock_slert', views.stock_slert),
    # path('emp_stockmessage', views.emp_stockmessage),

]


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

