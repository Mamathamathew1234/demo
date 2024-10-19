from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from .models import *
import random
from django.core.mail import send_mail
import datetime
from django.utils.crypto import get_random_string

from django.shortcuts import get_object_or_404
# import razorpay

# Create your views here.

#----------------------------HOME PAGES--------------------------------

def index(re):
    return render(re, 'index.html')

def about(re):
    return render(re,'about.html')

def coming(re):
    return render(re,'coming.html')

def contact(re):
    return render(re,'contact.html')

def shop(re):
        a = Products.objects.all()
        print(a)
        return render(re, 'shop.html', {'d': a})


#----------------------------LOGIN-----------------------------------

def login(request):
    if request.method=='POST':
        p=request.POST['username']
        q=request.POST['password']
        try:
            datas=Register.objects.get(User_Name=p)
            if datas.Password==q:
                request.session['user']=p
                return redirect(userhome)
            else:
                messages.add_message(request,messages.INFO,"Invalid Password")
        except:
            try:
                datas = Join.objects.get(username=p)
                if datas.password == q:
                    request.session['emp'] = p
                    return redirect(del_home)

                else:
                    messages.add_message(request, messages.INFO, "Admin Not Login")
            except Exception:
                    if p == 'admin' and q == 'Admin@123':
                        request.session['ad'] = p
                        return redirect(adminhome)
                    else:
                      messages.add_message(request,messages.INFO,"Invalid Password")
    return render(request,'login.html')

#----------------------------------LOGOUT-----------------------------------

def logout(re):
        if 'user' in re.session:
            re.session.flush()
        return redirect(index)

#---------------------------------REGISTER--------------------------------

def register(request):
    if request.method=="POST":
        name=request.POST['a']
        username=request.POST['b']
        useremail=request.POST['c']
        userphone=request.POST['d']
        password=request.POST['e']
        city=request.POST['f']
        district=request.POST['g']
        pincode=request.POST['h']
        address=request.POST['i']

        try:
            existing_email=Register.objects.filter(User_Email=useremail).exists()
            existing_username=Register.objects.filter(User_Name=username).exists()
            if existing_email:
                messages.error(request,'Email ID is already registered.Please log in.')
            elif existing_username:
                messages.error(request,'Username is already taken.')
            else:
                data=Register.objects.create(Name=name,UserPhone=userphone,Password=password,User_Name=username,User_Email=useremail,u_address=address,u_city=city,u_district=district,u_pincode=pincode)
                data.save()
                # z=data.email
                # send_mail('Congrats!!!','Successfully registered ','settings.EMAIL_HOST_USER',[z],
                #          fail_silently=False)
                messages.success(request,'Registration successfully!!!')
                # return redirect(login)
                return render(request,'register.html')

        except Exception:
            return redirect(r1)
    return render(request,'register.html')


def r1(re):
    return render(re,'register.html')



def single(re,id):
    if 'user' in re.session:
        b=Products.objects.get(pk=id)
        print(b)
        return render(re,'single.html',{'e':b})




# ---------------------------- SINGLE BOOKING ---------------------------
def singles(request, d):
    if 'user' in request.session:
        user = Register.objects.get(User_Name=request.session['user'])
        product = Products.objects.get(pk=d)
        return render(request, 'singlepay.html', {'data': user, 'pdata': product})
    return redirect(userhome)

def single_booking(request, product_id):
    if 'user' not in request.session:
        return redirect(userhome)

    product = get_object_or_404(Products, pk=product_id)
    user = get_object_or_404(Register, User_Name=request.session['user'])
    crt = mycart.objects.filter(usr=user).first()


    if request.method == "POST":
        so_fname = request.POST.get('sofname', '')
        so_lname = request.POST.get('solname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        so_city = request.POST.get('scity', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('add_det', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')

        total_price=product.price

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'watch' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'watch' + str(random.randint(1111111, 9999999))

        single_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt,
            so_fname=so_fname,
            so_lname=so_lname,
            so_email=so_email,
            so_phone=so_phone,
            so_address=so_address,
            so_district=so_district,
            so_city=so_city,
            so_pincode=so_pincode,
            add_message=add_message,
            quantity=quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        single_booking.save()

        messages.success(request, 'Your order has been placed successfully')

        # if paymode == 'RazorPay':
        #     return redirect('single_booking', price=total_price)
        #     # return JsonResponse({'status': 'Your order has been placed successfully'})
        #
        # return redirect('single_booking', product_id=product.id)

    return redirect(userhome)

# razorpay

def single_razor(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    user = get_object_or_404(Register, User_Name=request.session['user'])
    crt = mycart.objects.filter(usr=user).first()


    if request.method == "POST":
        print("hello")
        so_fname = request.POST.get('sofname', '')
        so_lname = request.POST.get('solname', '')
        so_email = request.POST.get('semail', '')
        so_phone = int(request.POST.get('sphone', 10))
        so_address = request.POST.get('sadrs', '')
        so_district = request.POST.get('sdistrict', '')
        so_city = request.POST.get('scity', '')
        so_pincode = int(request.POST.get('spincode', 6))
        add_message = request.POST.get('notes', '')
        quantity = int(request.POST.get('singleqty', 1))
        total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        print(paymode,total_price)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'watch' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'watch' + str(random.randint(1111111, 9999999))

        single_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt,
            so_fname=so_fname,
            so_lname=so_lname,
            so_email=so_email,
            so_phone=so_phone,
            so_address=so_address,
            so_district=so_district,
            so_city=so_city,
            so_pincode=so_pincode,
            add_message=add_message,
            quantity=quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        single_booking.save()
        # if paymode == 'RazorPay':
        return redirect(razorpaycheck,product.price)
    #     return JsonResponse({'status': 'Your order has been placed successfully'})
    #
    # return redirect(usr_home)


def razorpaycheck(request,price):
    if 'user' in request.session:
        u = Register.objects.get(User_Name=request.session['user'])
        s = Order.objects.filter(customer=u)
        t = price*100
        return render(request, "payment.html", {'amount': t})

    return render(request, "payment.html")



#-----------------------------Multiple boooking-----------------

def checkout(request):
    # c = d
    mp = []
    t = 0
    if 'user' in request.session:
        user = Register.objects.get(User_Name=request.session['user'])
        mp=mycart.objects.filter(usr=user)
        c=mp
        t=0
        print (mp)
        for i in c:
            t = t + (i.products.price * i.quantity)
        return render(request, 'multiple_booking.html', {'data': user, 'pdata':mp,'t':t})
    return redirect(userhome)

def multiple_booking(request):
    if 'user' not in request.session:
        return redirect('userhome')

    user = get_object_or_404(Register, User_Name=request.session['user'])
    crt = mycart.objects.filter(usr=user)
    # crt = mycart.object.filter(usr=user).delete()
    t=0
    for i in crt:
        t = t + (i.products.price * i.quantity)
        total = t
        quty=i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(userhome)
    if request.method == "POST":
        m_fname = request.POST.get('sofname', '')
        m_lname = request.POST.get('solname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_city = request.POST.get('scity', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('add_det', '')
        m_quantity = int(request.POST.get('multyqty', 1))
        m_quantity =quty
        total_price = int(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        total_price =total
        product_id =crt_i. products.pk
        product = get_object_or_404(Products, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'watch' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'watch' + str(random.randint(1111111, 9999999))

        multiple_booking =Order.objects.create(
            customer=user,
            product=product,
            cart=crt_i ,
            so_fname=m_fname,
            so_lname=m_lname,
            so_email=m_email,
            so_phone=m_phone,
            so_address=m_address,
            so_district=m_district,
            so_city=m_city,
            so_pincode=m_pincode,
            add_message=m_add_message,
            quantity=m_quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        multiple_booking.save()
        mycart.objects.filter(usr=user).delete()
        messages.success(request, 'Your order has been placed successfully')
        return redirect(userhome)

    return redirect(checkout)




def razorpaycheck2(request):
    if 'user' in request.session:
        u = Register.objects.get(User_Name=request.session['user'])
        s = Order.objects.filter(customer=u)
        mp = mycart.objects.filter(usr=u)
        c = mp
        t = 0
        print(mp)
        for i in c:
            t = t + (i.products.price * i.quantity)
            total=t*100
        return render(request, "payment.html", {'amount': total})

    return render(request, "payment.html")


def multiple_razor(request):
    if 'user' not in request.session:
        return redirect(userhome)

    user = get_object_or_404(Register, User_Name=request.session['user'])
    crt = mycart.objects.filter(usr=user)
    t=0
    for i in crt:
        t = t + (i.products.price * i.quantity)
        total = t
        quty = i.quantity

    if crt.exists():
        crt_i = crt.first()
    else:
        messages.error(request, 'No cart found for the user')
        return redirect(userhome)


    if request.method == "POST":
        print("hello")
        m_fname = request.POST.get('sofname', '')
        m_lname = request.POST.get('solname', '')
        m_email = request.POST.get('semail', '')
        m_phone = int(request.POST.get('sphone', 10))
        m_address = request.POST.get('sadrs', '')
        m_district = request.POST.get('sdistrict', '')
        m_city = request.POST.get('scity', '')
        m_pincode = int(request.POST.get('spincode', 6))
        m_add_message = request.POST.get('notes', '')
        m_quantity = int(request.POST.get('singleqty', 1))
        m_quantity=quty
        # total_price = float(request.POST.get('total', 0))
        paymode = request.POST.get('payment_mode', '')
        # print(paymode,total_price)
        total_price =total
        product_id = crt_i.products.pk
        product = get_object_or_404(Products, id=product_id)

        order_id = 'ordid' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = 'ordid' + str(random.randint(1111111, 9999999))

        tracking_no = 'watch' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=tracking_no).exists():
            tracking_no = 'watch' + str(random.randint(1111111, 9999999))

        multiple_booking = Order.objects.create(
            customer=user,
            product=product,
            cart=crt_i ,
            so_fname=m_fname,
            so_lname=m_lname,
            so_email=m_email,
            so_phone=m_phone,
            so_address=m_address,
            so_district=m_district,
            so_city=m_city,
            so_pincode=m_pincode,
            add_message=m_add_message,
            quantity=m_quantity,
            status='Pending',
            payment_mode=paymode,
            payment_id=None,
            order_id=order_id,
            tracking_no=tracking_no,
            total_price=total_price,
        )
        # multiple_booking.save()
        # # if paymode == 'RazorPay':
        # return redirect(razorpaycheck2,product.price)

        multiple_booking.save()
        messages.success(request, 'Your order has been placed successfully')
        return redirect(razorpaycheck2)

# def placeorder(r):
#     if 'user' in r.session:
#         f=Products.objects.all()
#         details=Register.objects.get(User_Name=r.session['user'])
#         print(details)
#         usr = Register.objects.get(User_Name = details.User_Name)
#         c = mycart.objects.filter(usr=details).all()
#         t=0
#         for i in c:
#             t=t+(i.products.price*i.quantity)
#         if r.method == 'POST':
#             if r.POST.get('save')=='save':
#                 ofname = r.POST.get('fname')
#                 olname = r.POST.get('lname')
#                 # email = r.POST.get('email')
#                 ophone = r.POST.get('phone')
#                 oaddress = r.POST.get('address')
#                 ocity = r.POST.get('city')
#                 odistrict = r.POST.get('district')
#                 opincode = r.POST.get('pincode')
#                 pro = Order.objects.filter(user=usr).first()
#                 if pro:
#                     pro.ofname = r.POST.get('fname')
#                     pro.olname = r.POST.get('lname')
#                     # pro.email = r.POST.get('email')
#                     pro.ophone = r.POST.get('phone')
#                     pro.oaddress = r.POST.get('address')
#                     pro.ocity = r.POST.get('city')
#                     pro.odistrict = r.POST.get('district')
#                     pro.opincode = r.POST.get('pincode')
#                     pro.save()
#                 else:
#                     cr = Order.objects.create(user=usr,fname=ofname,lname=olname,phone=ophone,address=oaddress,city=ocity,district=odistrict,pincode=opincode)
#                     cr.save()
#                 return redirect(placeorder)
#             else:
#                 neworder = Order()
#                 neworder.user = usr
#                 neworder.ofname = r.POST.get('fname')
#                 neworder.olname = r.POST.get('lname')
#                 # neworder.email = r.POST.get('email')
#                 neworder.ophone = r.POST.get('phone')
#                 neworder.oaddress = r.POST.get('address')
#                 neworder.ocity = r.POST.get('city')
#                 neworder.odistrict = r.POST.get('district')
#                 neworder.opincode = r.POST.get('pincode')
#
#                 neworder.t_price = t
#
#                 neworder.payment_mode = r.POST.get('payment_mode')
#                 neworder.payment_id = r.POST.get('payment_id')
#
#                 trackno = 'bag'+str(random.randint(1111111,9999999))
#                 while Order.objects.filter(tracking_no=trackno) is None:
#                     trackno = 'ecart'+str(random.randint(1111111,9999999))
#                 neworder.tracking_no = trackno
#                 neworder.save()
#
#                 for item in c:
#                     orderitem.objects.create(
#                         orderdet = neworder,
#                         product = item.item_details,
#                         price = item.item_details.price,
#                         quantity = item.quantity
#                     )
#                 datas=orderitem.objects.all()
#                 da=mycart.objects.all()
#                 for i in da:
#                     for j in c:
#                         if i.pname==j.products.pname:
#                              sum=i.qut-j.quantity
#                              dat=Products.objects.filter(pname=j.products.pname).update(qut=sum)
#                              if sum<5:
#                                 z='ekartqwe@gmail.com'
#                                 send_mail('Stock Messsage', f'{j.products.pname},{"Out Of Stock"}','settings.EMAIL_HOST_USER',[z],fail_silently=False)
#                 mycart.objects.filter(usr=details).delete()
#                 messages.success(r, 'Your order has been placed successfully')
#                 payMode = r.POST.get('payment_mode')
#                 if payMode == "Razorpay":
#                     return JsonResponse({'status':'Your order has been placed successfully'})
#         return redirect(checkout)

def success(re):
    return redirect(user_orders)



#-------------------------userhome-------------------------------

def userhome(re):
    return render(re,'user home.html')

def user_collection(re):
    if 'user' in re.session:
        user=Register.objects.get(User_Name=re.session['user'])
        l=[]
        datas=''
        try:
            datas=mycart.objects.filter(usr=user)
            d1=datas
            print(datas)
            for i in datas:
                l.append(i.products)
        except:
            pass
        data= Products.objects.all()
        print(l)
        return render(re,'user_collection.html', {'data':data,'datas':l,'d1':d1})
    return redirect(login)

def user_about(re):
    return render(re,'user_about.html')
    return redirect(userhome)

def user_contact(re):
    return render(re,'user_contact.html')
    return redirect(userhome)


def user_orders(re):
    if 'user' in re.session:
        user = Register.objects.get(User_Name=re.session['user'])
        data = Order.objects.filter( customer=user)
        # datas=Multiple_Booking.objects.all()
        return render(re,'user_orders.html',{'order' : data})
    return redirect(userhome)

#-----------------------------------------adminhome--------------------------------------------

def adminhome(re):
    return render(re,'admin home.html')

def addcollection(re):
        if re.method == 'POST':
            n = re.POST.get('pname')
            dc = re.POST.get('description')
            f = re.POST.get('features')
            p = re.POST.get('price')
            c = re.POST.get('category')
            img = re.FILES.get('pimg')
            obj = Products.objects.create(pname=n, price=p, description=dc, features=f, category=c,
                                          pimg=img)
            messages.success(re,'successfully..!')
            obj.save()
        return render(re,'add collection.html')

def viewuser(request):
        if 'ad' in request.session:
            data= Register.objects.all()
            print(data)
            return render(request, 'view user.html', {'d':data})
        return redirect(adminhome)

def view_deliveryboy(re):
    if 'ad' in re.session:
        data = Join.objects.all()
        return render(re,'view_deliveryboy.html',{'d':data})
    return redirect(adminhome)

def delete_del(re,id):
    if 'ad' in re.session:
        data = Join.objects.get(pk=id)
        data.delete()
        messages.success(re,'...Delivery Person Deleted...')
        return redirect(view_deliveryboy)



def userbooking(re):
    if 'ad'in re.session:
      orders = Order.objects.all()
      return render(re, 'user booking.html', {'orders': orders})
    return redirect(adminhome)

def product_details(re):
    if 'ad' in re.session:
        data = Products.objects.all()
        return render(re, 'product_details.html',{'d':data})
    return redirect(adminhome)

def delete(re,id):
    if 'ad' in re.session:
        data = Products.objects.get(pk=id)
        data.delete()
        messages.success(re,'...Product Deleted...')
        return redirect(product_details)

def update(re,id):
    if 'ad' in re.session:
        data = Products.objects.get(pk=id)
        return render(re,'update_product.html',{'d':data})

def updating(re,id):
    if 'ad' in re.session:
        nm = re.POST['upname']
        dtn = re.POST['updescription']
        # qty = re.POST['upquan']
        pce = re.POST['upprice']
        Products.objects.filter(pk=id).update(pname=nm,description=dtn,price=pce)
        return redirect(updis)
    return render(re,'update_product.html')

def updis(re):
    updata = Products.objects.all()
    messages.success(re,'...Product Updated Successfully...')
    return render(re,'update_display.html',{'udp':updata})


def statusup(r,wal):
    if r.method == "POST":
        st = Order.objects.get(id=wal)
        st.status = r.POST.get('status')
        st.save()
    return redirect(userbooking)


#-----------------------------------cart---------------------------------------


def viewcart(request):
    if 'user' in request.session:
        pp = Products.objects.all()
        details = Register.objects.get(User_Name=request.session['user'])  # single user details get
        datas2 = mycart.objects.filter(usr=details)
        c = datas2
        sum = []
        l = 0
        d = Products.objects.all()
        t = 0

        sub = {}
        su = datas2
        for i in su:
            sub[i.products] = [i.quantity, i.pk, i.products.price * i.quantity]
        print(sub)
        for i in c:
            t = t + (i.products.price * i.quantity)
        for i in sub:
            sum.append(sub[i])
        print(sum)

    return render(request, 'view_cart.html', {'datas': datas2, 'total': t, 'sub': sub, 'cl': sub, 'd': d})


def cart1(request, d):
    if 'user' in request.session:
        a = Register.objects.get(User_Name=request.session['user'])
        b = Products.objects.get(pk=d)

        datas = mycart.objects.create(usr=a, products=b,total_price=0)
        datas.save()
        messages.success(request,'cart add successfully..!')
        return redirect(viewcart)
    return redirect(login)



def update_cart(request):
    if request.session['user']:
        l = []
        if request.method == 'POST':
            total_price = request.POST['overall_total']
            quantity = request.POST['quantity']
            print(total_price)
        return redirect(viewcart)
    return redirect(login)


def minuscart(d2, de):
    if 'user' in d2.session:
        c = mycart.objects.get(id=de)
        if c.quantity > 1:
            c.quantity = c.quantity - 1
            c.save()
        else:
            c.delete()
    return redirect(viewcart)


def pluscart(d3, de):
    if 'user' in d3.session:
        c = mycart.objects.get(id=de)
        c.quantity = c.quantity + 1
        c.save()
    return redirect(viewcart)

def delete_cart(request,d):
    datas=mycart.objects.get(pk=d)
    datas.delete()
    return redirect(viewcart)

#----------------------wishlist------------------


# def wishlist(request,d):
#     if 'user' in request.session:
#         p=Register.objects.get(User_Name=request.session['user'])
#         q=Products.objects.get(pk=d)
#         wishlist,created=Wishlist.objects.get_or_create(user_details=p,item_details=q)
#         if q in wishlist.objects.all():
#             messages.success(request,"already exist")
#         else:
#             datas = Wishlist.objects.create(user_details=p, item_details=q)
#             datas.save()
#         return redirect(userhome)
#     return redirect(login)
def wishlist(request, d):
    if 'user' in request.session:
        try:
            user = Register.objects.get(User_Name=request.session['user'])
            product = Products.objects.get(pk=d)

            # Check if product is already in user's wishlist
            wishlist_item, created = Wishlist.objects.get_or_create(user_details=user, item_details=product)

            if created:
                messages.success(request, "Item added to wishlist successfully.")
            else:
                messages.info(request, "Item is already in your wishlist.")

            return redirect(user_collection)  # Replace with your actual user home URL name

        except Register.DoesNotExist:
            messages.error(request, "User does not exist.")  # Handle the case where user is not found
            return redirect(login)  # Replace with your actual login URL name

        except Products.DoesNotExist:
            messages.error(request, "Product does not exist.")  # Handle the case where product is not found
            return redirect(userhome)  # Redirect to a suitable page

    return redirect(login)
def view_wishlist(request):
    if 'user' in request.session:
        details=Register.objects.get(User_Name=request.session['user'])
        datas=Wishlist.objects.filter(user_details=details)
        l=[]
        l2=[]
        for i in datas:
            l.append(i.item_details)
        datas2=mycart.objects.filter(usr=details)
        for i in datas2:
            l2.append(i.products)
        datas3=mycart.objects.filter(usr=details)
        return render(request,'view_wishlist.html',{'datas':datas,'datas1':l,'datas2':l2})
    return redirect(r1)

def delete_wishlist(request,d):
    datas=Wishlist.objects.get(pk=d)
    datas.delete()
    return redirect(view_wishlist)


from .forms import *


#--------------------------profile----------------------------


def usr_profile(re):
    if 'user' in re.session:
        u = Register.objects.get(User_Name=re.session['user'])
        return render(re,'profile.html',{'user':u})
    return redirect(userhome)

def pro_edit(re,id):
    if 'user' in re.session:
        u = Register.objects.get(pk=id)
        if re.method == 'POST':
            u.Name=re.POST['name']
            u.User_Name = re.POST['username']
            u.User_Email = re.POST['email']
            u.UserPhone = re.POST['nmbr']
            u.u_address = re.POST['adrss']
            u.u_district = re.POST['udistrict']
            u.u_city = re.POST['ucity']
            u.u_pincode  = re.POST['upincode']
            try:
                u.u_img = re.FILES['user_img']
                import os
                os.remove()
                u.save()
            except:
                u.save()
                return redirect(profile_edit,id)
        return render(re,'profile_edit.html',{'d':u})
    return redirect(userhome)


def profile_edit(re,id):
    if 'user' in re.session:
        if re.method == 'POST':
            form=UserProfileForm(re.POST,re.FILES)
            if form.is_valid():
                a=form.cleaned_data['Name']
                b=form.cleaned_data['User_Name']
                c=form.cleaned_data['User_Email']
                d=form.cleaned_data['UserPhone']
                e=form.cleaned_data['Password']
                f=form.cleaned_data['u_address']
                g=form.cleaned_data['u_district']
                h=form.cleaned_data['u_city']
                # i = form.cleaned_data['user_img']
                j=form.cleaned_data['u_pincode ']

                Register.objects.filter(pk=id).update(Name=a,User_Name=b,User_Email=c,UserPhone=d,Password=e,u_address=f,u_district=g,u_city=h,u_pincode=j)
                messages.success(re,'...Profile Updated Successfully...')
                return redirect(usr_profile)
        # data = Register.objects.all()
        # return render(re,'profile_edit.html',{'d':data})
        # form=UserProfileForm()
        # return render(re,'profile_edit.html',{'form':form})
    return redirect(usr_profile)



# ---------------------------- FORGOT/RESET PASSWORD -USER  ---------------------------
def forgot_password_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Register.objects.get(User_Email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password_user)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password_user)

    return render(request, 'forgot_password.html')

def reset_password_user(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.Password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'resetpassword.html',{'token':token})


# ----------------------------Employee------------------------------------

def join(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        location=request.POST['location']
        photo=request.FILES['photo']
        license=request.FILES['license']
        username=request.POST['username']
        password=request.POST['password']
        biodata=request.FILES['biodata']
        accoundnumber=request.POST['accoundnumber']
        request.session['emp']=username
        data=Join.objects.create(firstname=firstname,lastname=lastname,email=email,phone=phone,location=location,photo=photo,license=license,username=username,password=password,biodata=biodata,accoundnumber=accoundnumber)
        data.save()
        messages.success(request,'join successfullyy.!')
    return redirect(jr)

def jr(request):
    return render(request,'join.html')

def stock_slert(request):
    if request.method=='POST':
        item=request.POST['sr']
        messge=request.POST['messge']
        data=alert.objects.create(item=item,messge=messge)
        data.save()
    return redirect(del_orders)

def del_home(request):
    if 'emp' in request.session:
        return render(request,'del_home.html')
    else:
        return redirect(jr)
def emp_chnagepassword(request,d):
    if request.session['emp']:
        datas=Join.objects.filter(pk=d)
        if request.method=='POST':
            # username=request.POST['username']
            password=request.POST['password']
            cr=Join.objects.filter(pk=d).update(password=password)
        return render(request,'emp_changepassword.html',{'datas':datas})
    return redirect(login)
def emp_cash(request):
    if 'emp' in request.session:
        datas=Join.objects.get(username=request.session['emp'])
        return render(request,'emp_cash.html',{'datas':datas})
    return redirect(jr)

def del_orders(re):
    if 'emp' in re.session:
        data = Order.objects.all()
        return render(re,'del_orders.html',{'order' : data})
    return redirect(del_home)

def del_profile_update(request):
    if 'emp' in request.session:
        emp=Join.objects.filter(username=request.session['emp']).first()
        pro=profilepic.objects.filter(user=emp).first()
        if request.method=='POST':
            emp.firstname=request.POST.get('firstname')
            emp.lastname=request.POST.get('lastname')
            emp.accoundnumber=request.POST.get('accoundnumber')
            emp.email=request.POST.get('email')
            emp.phone=request.POST.get('phone')
            emp.location=request.POST.get('location')
            photo=request.FILES.get('Photo')
            if photo == None:
                emp.save()
            else:
                if pro:
                    pro.user=emp
                    pro.propic=photo
                    emp.save()
                    pro.save()
                else:
                    cr=profilepic.objects.create(user=emp,propic=photo)
                    cr.save()
            return redirect(del_home)
        return render(request,'del_profile_update.html',{'datas':emp,'pro':pro})
    return redirect(login)
def del_profile(request):
    if 'emp' in request.session:
        datas=Join.objects.filter(username=request.session['emp'])
        emp=Join.objects.filter(username=request.session['emp']).first()
        pro=profilepic.objects.filter(user=emp).first()
    return render(request,'del_profile.html',{'datas':datas,'pro':pro})
def emp_stockmessage(request):
    d='baggage@gmail.com'
    datas=Products.objects.all()
    return render(request,'emp_stockmessage.html',{'d':d,'datas':datas})

