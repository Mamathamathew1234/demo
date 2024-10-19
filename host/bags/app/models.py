from django.db import models

# Create your models here.
class Register(models.Model):
    Name=models.CharField(max_length=20)
    User_Name=models.CharField(max_length=20)
    User_Email=models.EmailField(unique=True)
    UserPhone=models.IntegerField()
    Password=models.CharField(max_length=20)
    u_address = models.CharField(max_length=100)
    u_district = models.CharField(max_length=20)
    u_city = models.CharField(max_length=20)
    u_pincode = models.IntegerField()

class Products(models.Model):
    categorychoices=(
        ('a','men'),
        ('b','women'),
        ('c','kids'),
    )
    pname=models.CharField(max_length=200)
    price=models.IntegerField()
    description=models.CharField(max_length=1000)
    features=models.CharField(max_length=1000)
    category=models.CharField(max_length=100,default='a',choices=categorychoices)
    pimg=models.FileField()


class mycart(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    usr = models.ForeignKey(Register, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price=models.IntegerField()
    delivered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.usr}'

class Wishlist(models.Model):
    user_details=models.ForeignKey(Register,on_delete=models.CASCADE)
    item_details=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.CharField(max_length=30)
    status=models.IntegerField(default=0)



# class Single_Booking(models.Model):
#     customer = models.ForeignKey(Register,on_delete=models.CASCADE)
#     product = models.ForeignKey(Products,on_delete=models.CASCADE)
#     so_fname = models.CharField(max_length=20,null=False)
#     so_lname = models.CharField(max_length=20)
#     so_email = models.EmailField(null=False)
#     so_phone = models.IntegerField(null=False)
#     so_address = models.TextField(null=False)
#     so_district = models.CharField(max_length=20,null=False)
#     so_city = models.CharField(max_length=20,null=False)
#     so_pincode = models.IntegerField(null=False)
#     add_message = models.CharField(max_length=250)
#     order_status = (
#         ('Pending','Pending'),
#         ('Out For Shipping','Out For Shipping'),
#         ('Delivered','Delivered'),
#         ('Cancelled','Cancelled'),
#     )
#     status = models.CharField(max_length=150,choices=order_status,default='Pending')
#     quantity = models.IntegerField(null=False)
#     total_price = models.FloatField(null=False)
#     payment_mode = models.CharField(max_length=150, null=False)
#     payment_id = models.CharField(max_length=150, null=True)
#     order_id = models.CharField(max_length=150, null=False)
#     tracking_no = models.CharField(max_length=150, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self) -> str:
#         return f'{self.tracking_no}'
#
# # ------------ Multiple Booking ------------
# class Multiple_Booking(models.Model):
#     user = models.ForeignKey(Register,on_delete=models.CASCADE)
#     item = models.ForeignKey(Products,on_delete=models.CASCADE)
#     cart = models.ForeignKey(mycart,on_delete=models.CASCADE)
#     m_fname = models.CharField(max_length=20,null=False)
#     m_lname = models.CharField(max_length=20)
#     m_email = models.EmailField(null=False)
#     m_phone = models.IntegerField(null=False)
#     m_address = models.TextField(null=False)
#     m_district = models.CharField(max_length=20,null=False)
#     m_city = models.CharField(max_length=20,null=False)
#     m_pincode = models.IntegerField(null=False)
#     add_message = models.CharField(max_length=250)
#     order_status = (
#         ('Pending','Pending'),
#         ('Out For Shipping','Out For Shipping'),
#         ('Delivered','Delivered'),
#         ('Cancelled','Cancelled'),
#     )
#     status = models.CharField(max_length=150,choices=order_status,default='Pending')
#     quantity = models.IntegerField(null=False)
#     total_price = models.FloatField(null=False)
#     payment_mode = models.CharField(max_length=150, null=False)
#     payment_id = models.CharField(max_length=150, null=True)
#     order_id = models.CharField(max_length=150, null=False)
#     tracking_no = models.CharField(max_length=150, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class Order(models.Model):
#     user = models.ForeignKey(Register, on_delete=models.CASCADE)
#     quant = models.IntegerField(default=1)
#     t_price = models.FloatField()
#     oaddress = models.CharField(max_length=80)
#     ocity = models.CharField(max_length=20)
#     odistrict = models.CharField(max_length=20)
#     opincode = models.IntegerField()
#     ophone = models.IntegerField()
#     ofname = models.CharField(default='', max_length=30)
#     olname = models.CharField(default='', max_length=30)
#     additional = models.CharField(max_length=50)
#     payment_mode = models.CharField(max_length=150, null=False)
#     payment_id = models.CharField(max_length=150, null=True, default=00000)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     updated_at = models.DateField()
#
#
#     orderstatus = (
#         ('Pending', 'Pending'),
#         ('Shipped', 'Shipped'),
#         ('Out for Delivery', 'Out for Delivery'),
#         ('Delivered', 'Delivered'),
#         ('Cancelled', 'Cancelled')
#     )
#     status = models.CharField(max_length=150, choices=orderstatus, default='pending')
#     tracking_no = models.CharField(max_length=150, null=True)
#     def __str__(self) -> str:
#         return f'{self.tracking_no}'
class Order(models.Model):
    customer = models.ForeignKey(Register,on_delete=models.CASCADE)
    cart = models.ForeignKey(mycart, on_delete=models.CASCADE, null=True, blank=True)  # Adjust according to your requirements
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    so_fname = models.CharField(max_length=20,null=False)
    so_lname = models.CharField(max_length=20)
    so_email = models.EmailField(null=False)
    so_phone = models.IntegerField(null=False)
    so_address = models.TextField(null=False)
    so_district = models.CharField(max_length=20,null=False)
    so_city = models.CharField(max_length=20,null=False)
    so_pincode = models.IntegerField(null=False)
    add_message = models.CharField(max_length=250)
    order_status = (
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )
    status = models.CharField(max_length=150,choices=order_status,default='Pending')
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    order_id = models.CharField(max_length=150, null=False)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class orderitem(models.Model):
    orderdet = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


class Join(models.Model):
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
    phone=models.IntegerField()
    location=models.CharField(max_length=50)
    photo=models.FileField()
    license=models.FileField()
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    biodata=models.FileField()
    accoundnumber=models.IntegerField()
    status=models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.firstname
class profilepic(models.Model):
    user = models.OneToOneField(Join,on_delete=models.CASCADE)
    propic = models.FileField(upload_to='images/profilepic')
class alert(models.Model):
    item=models.CharField(max_length=100)
    messge=models.CharField(max_length=200)

class PasswordReset(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    #security
    token=models.CharField(max_length=4)

