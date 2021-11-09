from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# 新增的模型
class Temporary(models.Model):
    uname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    imageURL = models.TextField(null=True)
    ttok = models.CharField(max_length=200)
    nums = models.CharField(max_length=200)
    jiage = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    danjia = models.CharField(max_length=200)
    zongshu = models.CharField(max_length=200)


# 修改的模型
# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     phone = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200)
#     profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#
#     def __str__(self):
#         return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=0)
    encryption_link = models.CharField(max_length=200, null=True)
    expires = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


# 文章分类
class Category(models.Model):
    name = models.CharField('Category', max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Category', blank=True, null=True)
    price = models.FloatField()  # 总价
    total = models.IntegerField(default=0)  # 总数
    pos = models.IntegerField(default=0)  # 销售量
    info = models.TextField(null=True)  # 商品介绍
    size = models.TextField(null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_new = models.CharField(max_length=65535, null=True, blank=True)
    state1 = models.CharField(max_length=65535, null=True)
    state2 = models.CharField(max_length=65535, null=True)
    jsondata = models.CharField(max_length=65535, null=True)  # json
    color = models.CharField(max_length=65535, null=True)  # 颜色
    combo = models.CharField(max_length=65535, null=True)  # 版本
    pinfojson = models.CharField(max_length=65535, null=True)  # 商品配置详情
    choosepk = models.CharField(max_length=65535, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            if self.image:
                url = self.image.url
            else:
                url = self.image_new
        except:
            url = ''
        return url


# 游客订单表
class youkeorder(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.CharField(max_length=65535, null=False)  # 收货人
    get_way = models.CharField(max_length=65535, null=False)  # 派送方式
    phone = models.CharField(max_length=65535, null=False)  # 电话
    email = models.CharField(max_length=65535, null=False)  # 邮箱
    company = models.CharField(max_length=65535, null=False)  # 公司
    totalprices = models.FloatField(null=False)  # 商品总价
    yunfei = models.FloatField(null=False)  # 运费
    amount = models.FloatField(null=False)  # 支付价格
    shui = models.FloatField(null=False)  # 税
    nation = models.CharField(max_length=65535, null=False)  # 国家
    province = models.CharField(max_length=65535, null=False)  # 省份
    city = models.CharField(max_length=65535, null=False)  # 城市
    postcode = models.CharField(max_length=65535, null=False)  # 邮编
    addinfo = models.CharField(max_length=65535, null=False)  # 详细地址
    items = models.IntegerField(default=0, null=False)  # 商品数量
    itemsjson = models.CharField(max_length=65535, null=False)  # 购买商品的详细json
    createtime = models.DateTimeField(auto_now_add=True)  # 购买时间


# 修改过的表
# class Order(models.Model):
#     STATUS = (
#         ('Pending', 'Pending'),
#         ('Out for delivery', 'Out for delivery'),
#         ('Delivered', 'Delivered'),
#     )
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=100, null=True)
#     note = models.CharField(max_length=1000, null=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
#     status = models.CharField(max_length=200, null=True, choices=STATUS)  # 新增
#     # 添加订单名称
#     name = models.CharField(max_length=128, null=True)
#     # 添加了存储正面图片路径的字段
#     picture_front = models.CharField(max_length=1024, null=True)
#     # 背面图片存储路径
#     picture_back = models.CharField(max_length=1024, null=True)
#     # 添加了存储绘图状态的字段
#     state1 = models.CharField(max_length=65535, null=True)
#     state2 = models.CharField(max_length=65535, null=True)
#
#     def __str__(self):
#         return str(self.id)
#
#     @property
#     def shipping(self):
#         shipping = False
#         orderitems = self.orderitem_set.all()
#         for i in orderitems:
#             if i.product.digital == False:
#                 shipping = True
#         return shipping
#
#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total
#
#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total

# 订单
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    total = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)  # 新增
    # 添加订单名称
    name = models.CharField(max_length=128, null=True)
    # 添加了存储正面图片路径的字段
    picture_front = models.CharField(max_length=1024, null=True)
    # 背面图片存储路径
    picture_back = models.CharField(max_length=1024, null=True)
    # 添加了存储绘图状态的字段
    state1 = models.CharField(max_length=65535, null=True)
    state2 = models.CharField(max_length=65535, null=True)
    color = models.CharField(max_length=65535, null=True)  # 颜色
    combo = models.CharField(max_length=65535, null=True)  # 版本
    price = models.FloatField()  # 单价
    userorderid = models.IntegerField(default=0, null=True)  # 订单ID
    delstatus = models.IntegerField(default=0, null=True)  # 删除标识， 0表示正常，1表示删除

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)  # 数量
    color = models.CharField(max_length=65535, null=True)  # 颜色
    combo = models.CharField(max_length=65535, null=True)  # 版本
    price = models.FloatField()  # 单价
    date_added = models.DateTimeField(auto_now_add=True)
    userorderid = models.IntegerField(default=0, null=True)  # 订单ID

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total


# 收货地址    修改过的表
# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     address = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     state = models.CharField(max_length=200, null=False)
#     zipcode = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.address

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='客户id')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='订单id')
    address = models.CharField(max_length=200, null=False, verbose_name='地址')
    country = models.CharField(max_length=200, null=True, verbose_name='国家')
    county = models.CharField(max_length=200, default='b', null=False, verbose_name='省')
    city = models.CharField(max_length=200, null=False, verbose_name='城市')
    gs = models.CharField(max_length=200, null=True, verbose_name='公司')
    postcode = models.CharField(max_length=200, default='b', null=False, verbose_name='邮编')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='地址添加日期')
    status = models.IntegerField(default=1, null=True, verbose_name='默认收货地址1为默认')
    phone = models.CharField(max_length=30, null=True)
    uname = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.address


class UserOrder(models.Model):
    userorderid = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='客户id')
    addressid = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, verbose_name='地址id')
    price = models.FloatField()  # 价格
    yunfei = models.FloatField()  # 运费
    shui = models.FloatField()  # 税
    ztaddress = models.CharField(max_length=1000, null=True, verbose_name='自提地址')
    status = models.IntegerField(default=1, null=True, verbose_name='订单状态；0完成；1未付款；2已付款；3已发货')
    date_added = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        print('URL:', url)
        return url


class Draw(models.Model):
    color = models.CharField(max_length=20, verbose_name='颜色')
    price = models.FloatField(verbose_name='价格')
    digital = models.SmallIntegerField(verbose_name='数字大小')
    dingzhiproduct = models.BooleanField(default=True)
    objects = models.Manager()

    def __str__(self):
        return self.price


class Upload(models.Model):
    Imgname = models.FileField(upload_to="img/")
