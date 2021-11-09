import calendar
import hashlib
import os
import uuid
import datetime
import json

import bleach
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.http import FileResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.utils import timezone
import json
import datetime
from django.views import View
from ecommerce import settings
from ecommerce.settings import BASE_DIR
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import OrderFilter
from .forms import CreateUserForm, ContactForm, CustomerForm, OrderForm, LoginForm
from .models import *
from .utils import cookieCart, cartData, guestOrder, guestordertodb
import base64

import time
from datetime import datetime


# @unauthenticated_user
# def register_page(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#
#             messages.success(request, 'Account was created for ' + username)
#
#             return redirect('login')
#
#     context = {'form': form}
#     return render(request, 'store/register.html', context)

def test_email(request):
    res = send_mail(
        '测试邮件发送标题',
        '测试邮件发送内容',
        settings.DEFAULT_FROM_EMAIL,
        [request.GET.get('email')]
    )
    if res == 1:     #这里 res == 1怎么理解， 如果邮件发送成功了，那就返回1即res就会等于1，==是比较两个值，如果res=1=1,那么返回邮件发送成功
        return HttpResponse('邮件发送成功')
    else:
        return HttpResponse('邮件发送失败')


@unauthenticated_user
def register_page(request):                 #整个流程讲一下
    form = CreateUserForm()
    if request.method == 'POST':
        name = request.POST.get('username')         #如果用户填好用户名并且点击提交，那么我们就能收到当前页面的post请求，然后就执行下面的语句。
        try:
            u = Customer.objects.get(name=name)
            if str(time.time()) < str(u.expires) and u.status == 0:
                u.delete()
                context = {'form': form}
                return render(request, 'store/register.html', context)
            else:
                return render(request, 'store/register.html', {'msg': '该账号已被注册'})
        except:
            pass                            #如果上面出现异常，就过了，就接着走
        form = CreateUserForm(request.POST) #下面是发送邮件验证注册
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            request.session['checkuname'] = username
            # 生成激活链接
            ticks = time.time()
            m2 = hashlib.md5()
            m2.update(str(ticks).encode("utf8"))
            pwdcode = str(m2.hexdigest()) + (str(uuid.uuid1()))
            # 计算5分钟后的时间戳
            future = datetime.datetime.now() + datetime.timedelta(minutes=5)
            res = calendar.timegm(future.utctimetuple())
            us = Customer.objects.get(name=username)
            us.encryption_link = str(pwdcode)
            us.expires = res
            us.save()
            # 转为正常时间
            timeArray = time.localtime(res)
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            # 发送邮件
            url = 'http://127.0.0.1:8000/checkcode/?code=' + str(pwdcode)
            res = send_mail('验证邮箱完成注册',
                            '请点击以下链接来完成邮箱验证【' + url + '】谢谢',
                            settings.DEFAULT_FROM_EMAIL,
                            [request.POST.get('email')])
            if res == 1:
                return render(request, 'store/register.html', {'msg': '已发送激活邮件，请在五分钟内激活'})
            else:
                return HttpResponse('邮件发送失败')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        else:
            messages.info(request, 'Captcha is incorrect')

    context = {'form': form}
    return render(request, 'store/register.html', context)


# 如果想让验证码停用，那么把以下的替换掉143-151行

# @unauthenticated_user
# def login_page(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         us = Customer.objects.get(name=username)
#         request.session['uid'] = us.id
#         request.session['username'] = username
#         login(request, user)
#         guestordertodb(request)
#         response = HttpResponseRedirect('/store')
#         response.delete_cookie('cart')
#         return response

# 如果想让验证码停用，那么把以上的替换掉143-151行
@unauthenticated_user
def login_page(request):
    form = LoginForm()          #这句话是什么意思，声明一下并且选中login页面用户要提交的表格
    if request.method == 'POST':            #如果用户提交了表格，提交了post request的用户信息，那么就执行下面的语句。
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # ==============注释以下代码开启谷歌机器人验证；关闭则不验证=============================
        us = Customer.objects.get(name=username)
        request.session['uid'] = us.id
        request.session['username'] = username
        login(request, user)
        guestordertodb(request)
        response = HttpResponseRedirect('/store')
        response.delete_cookie('cart')
        return response
        # ==============注释以上代码开启谷歌机器人验证；关闭则不验证=============================

        form = LoginForm(request.POST)      #如果用户登录成功了，那么就给这个用户创建一个session，并且这个session里面会包含这些数据。
        if form.is_valid():
            if user is not None:
                us = Customer.objects.get(name=username)
                request.session['uid'] = us.id
                request.session['username'] = username
                login(request, user)
                guestordertodb(request)
                response = HttpResponseRedirect('/store')
                response.delete_cookie('cart')
                return response
            else:
                messages.info(request, 'Username OR password is incorrect')
        else:
            messages.info(request, 'Captcha is incorrect')

    context = {'form': form}
    return render(request, 'store/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('store')


def store(request): #为什么要请求这些数据，request是请求的对象，也就是函数的参数
    data = cartData(request)   #这句话怎么理解， cartData(request)是什么, carData是utils里面的函数，在这里调用
    cartItems = data['cartItems']  #这句话怎么理解， 调用data里cartData里的值 即， cartItems = 0  # 商品总数
    id = request.GET.get('id')        #这句话怎么理解，获取上一页传过来的id，比如?id=2
    if id:   #这个if id是什么意思，如果有id,如果id不为空
        products = Product.objects.filter(category_id=id) #这句话怎么理解，在product表里找id=id的数据
    else:
        products = Product.objects.filter(category_id=110801) #整个if else在这里是要做什么
    context = {'products': products, 'cartItems': cartItems} #这个context怎么理解，在这里写了数据对接数据库，前端就可以通过大括号调用
    return render(request, 'store/store.html', context) # 这里写context和写大括号都一样


def shapes(request):
    data = cartData(request)

    cartItems = data['cartItems']

    id = request.GET.get('id');
    if id:
        products = Product.objects.filter(category_id=id)
    else:
        products = Product.objects.filter(category_id=110801)
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/shapes.html', context)


def search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    search = request.GET.get('search')
    # products = Product.objects.all()
    products = Product.objects.filter(name__icontains=search)
    context = {'products': products, 'cartItems': cartItems, "search": search}
    return render(request, 'store/search.html', context)


def cart(request):
    data = cartData(request) #这句话cartData(request)是什么操作？用utils里面cartData函数来处理request网页请求数据

    cartItems = data['cartItems']
    totalprice = data['totalprice']
    itemslist = data['itemslist']   #上面三个'itemslist'是从哪里获取对
    context = {'itemslist': itemslist, 'cartItems': cartItems, 'totalprice': totalprice} #这个操作怎么理解？
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    us = Customer.objects.get(name=request.user.customer)
    add = ShippingAddress.objects.filter(customer_id=us.id).order_by('-status')
    totalprice = 0
    no_dingzhi = 0
    yunfei = 0
    shui = 0
    for item in data['itemslist']:
        jsondata = OrderItem.objects.get(id=item['id']).product.jsondata     #product.jsondata是什么意思
        if not jsondata:
            no_dingzhi += (item['price'] * item['quantity'])     # +=是什么意思， 是累积的意思
        totalprice += (item['price'] * item['quantity'])
    if 0 < no_dingzhi and no_dingzhi < 100:
        yunfei = 10
    shui = totalprice - (totalprice / 1.2)
    amount = yunfei + totalprice
    context = {'items': data['itemslist'], 'order': None, 'cartItems': data['cartItems'], 'addinfo': add,
               'is_login': True, 'totalprice': totalprice, 'yunfei': yunfei, 'shui': shui, 'amount': amount}
    return render(request, 'store/checkout.html', context)


from django.forms.models import model_to_dict


def adduserorder_query(request): #这个函数是干嘛用的
    results = model_to_dict(ShippingAddress.objects.get(id=request.GET['id']),   #model_to_dict就是把括号里面每个queryset变成一个字典
                            fields=['customer', 'order', 'address', 'country', 'county', 'city', 'gs', 'postcode',
                                    'phone', 'uname'])
    return JsonResponse({'data': results, 'code': 0})


# 添加购物车
def update_item(request):
    try:   #为什么一上来就try，这是什么用意？如果以下代码但凡有一点错报错，那么就执行except语句。
        data = json.loads(request.body) #json.loads(request.body)是什么意思，把我们前端请求的数据变成字典，request是参数，request.body是数据
        action = data['action']  #data['action']又是什么意思, data这个字典里面肯定有action这个值，action就是去'action'这个值。
        if action == 'delall':   # 'delall'是从哪里获取的？
            OrderItem.objects.get(id=data['id']).delete()  #为什么要说这句话？object.get就是查一条id为data['id']的数据，查完了就把这个删除掉
            return JsonResponse('Item was deleted', safe=False) #JsonResponse是什么意思，就是把字典变成json返回给前端。safe=False就是如果不是Json也要显示。这里就想返回'Item was deleted'
        else:   #下面4个都是什么意思？代表的是什么？就是设置初始值
            count = 1
            color = ''
            type = ''
            price = 0
            try:  #try下面4个又是什么意思，else try讲的故事内容是什么，想干什么东西。如果上面4个值出现异常，比如空的，那么执行下面的语句。
                count = int(data['count'])
                color = data['color']
                type = data['type']
                price = float(data['price'])
            except Exception as ee:   #这个exception as ee是什么意思，如果上面的try语句报错，那么执行下面的return语句。ee就是前面的exception取了别名
                return JsonResponse('Data Error!', safe=False)   #('Data Error!', safe=False)这是什么意思
            if not color or not type or not price:   #if not, or not是什么意思，if not color 如果不是颜色就是真。If not 颜色 or not 价格 or not 质量，这三个只要至少有一个条件是true，那么这个if判断就是true。比如可以满足是价格和质量但是只要不是颜色就行。
                return JsonResponse('Data Error!', safe=False)
            productId = data['productId']
            customer = request.user.customer  #request.user.customer是什么操作，获取用户的客户，user是表，customer也是表
            product = Product.objects.get(id=productId) #Product.objects.get(id=productId)又是什么操作
            order, created = Order.objects.get_or_create(customer=customer, product=product, complete=False,
                                                         color=color, combo=type,
                                                         price=price, userorderid=0)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, color=color, combo=type,
                                                                 price=price) #上面几行不懂。 orderItem和created 是取的两个变量，.get_or_create是查询或者创建，有数据就查询，没有就创建
            if action == 'add':  #这个'add'是什么动作，在哪里声明的？
                orderItem.quantity = (orderItem.quantity + count)  #quantity是orderItem的附属品吗？查询orderItem的quantity这个数值然后追加新的数值。orderItem.quantity怎么理解？(orderItem.quantity + count)就是算术对吗？加1和减1。
            elif action == 'remove':
                orderItem.quantity = (orderItem.quantity - count)
            orderItem.save()

            if orderItem.quantity <= 0: #这句话怎么理解，是要做什么操作
                orderItem.delete()

            return JsonResponse('Item was added', safe=False)
    except Exception as e:  #这句话怎么理解，完成了什么操作？e代表前面的Exception，也是别名。
        print("错误：", e)
        return JsonResponse('Error!', safe=False)


def process_order(request):        #这个函数整体讲一下。328行判定订单是否被支付，如果被支付，那么就完成。
    transaction_id = datetime.datetime.now().timestamp()      #这句话是什么意思，等号右面是什么意思？设置时区格林威治时间
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


def about(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    id = request.GET.get('id');
    if id:
        products = Product.objects.filter(category_id=id)
    else:
        products = Product.objects.filter(category_id=110801)
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/about.html', context)


def profile(request):
    return render(request, 'store/profile.html')


def contact(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'products': products, 'cartItems': cartItems}

    if request.method == "GET":
        form = ContactForm()
    elif request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = bleach.clean(form.cleaned_data["name"])
            email = bleach.clean(form.cleaned_data["email"])
            message = bleach.clean(form.cleaned_data["message"])

            send_mail(
                f"{name} sent an email", message, email, [settings.DEFAULT_FROM_EMAIL]
            )

            # Use a new form to clean out the old data and render a success message
            return render(
                request, "contact.html", {"form": ContactForm(), "success": True}
            )
    else:
        raise NotImplementedError

    return render(request, "store/contact.html", {"form": form})


# 新增开始

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
# @admin_only
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
# @admin_only
def myorders(request):
    orders = Order.objects.filter(customer__user=request.user)
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    orders1 = orders.filter(product__image=None)
    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending, 'orders1': orders1}

    return render(request, 'store/myorders.html', context)


@login_required(login_url='login')
# @admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'accounts/orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    if request.method == "POST":
        Order.objects.filter(id=pk).update(delstatus=1)
        return HttpResponse("ok")
    else:
        order = Order.objects.filter(id=pk)
        context = {'item': order}
        return render(request, 'accounts/delete.html', context)


# def slider(request):
#     pk = request.GET.get('pk')
#     product = Product.objects.filter(pk=pk).first()
#     context = {'product': product}
#     return render(request, 'store/detail.html', context)

def slider(request):
    data = cartData(request)
    cartItems = data['cartItems']
    pk = request.GET.get('pk')
    info = Product.objects.get(pk=pk)
    products = Product.objects.filter(id=8)  # 轮播显示图片
    pdic = json.loads(info.pinfojson)
    colors = []
    combos = []         #把这些属性显示出来
    fcolor = ""
    fcombo = ""
    ftotal = 0
    for k, dt in enumerate(pdic['data']):
        if k == 0:
            fcolor = dt['color']
            fcombo = dt['combo']
        if dt['color'] not in colors:
            colors.append(dt['color'])
        if dt['combo'] not in combos:
            combos.append(dt['combo'])
    for item in pdic['data']:
        if item['color'] == fcolor and item['combo'] == fcombo:
            ftotal = item['total']                      #取pic['data']的值，
    # product = Product.objects.filter(pk=pk).first()
    # context = {'product': product}
    return render(request, 'store/detail.html',
                  {"info": info, 'cartItems': cartItems, 'products': products, 'colors': colors, 'combos': combos,
                   'pk': pk, 'ftotal': ftotal,
                   'fcolor': fcolor, 'fcombo': fcombo, 'request': request, 'pinfojson': info.pinfojson,
                   'imgs': pdic['imgs']})


def queryproducttotal(request):  #这个函数是干嘛用的，就是获取总价的函数。下面声明的这些东西怎么理解，(request.POST.get('pk'))是从哪里获取的pk
    pk = int(request.POST.get('pk'))   #从上一页传来的pk值，id
    color = request.POST.get('color')  #从上一页传来的color
    combo = request.POST.get('combo')
    info = Product.objects.get(pk=pk)#pk=pk怎么理解, pk是主键primary key
    pdic = json.loads(info.pinfojson)#这句话怎么理解,把字典变成json。括号里面的就是字典。
    total = 0    #为什么要等于0，设置的初始值。
    price = 0
    for item in pdic['data']:  #这个for循环是要做什么
        if item['color'] == color and item['combo'] == combo:
            total = item['total']
            price = item['price']
    return HttpResponse(json.dumps({
        "total": total,
        "price": price
    }))    #这个json.dumps是什么意思，把括号里面的内容变成一个字符串。


def biaoge(request):
    data = cartData(request)

    cartItems = data['cartItems']
    totalprice = data['totalprice']
    itemslist = data['itemslist']

    pk = request.GET.get('pk') #整个pk的流程是怎么样的，通过get request获取当前页面的pk值
    oid = request.GET.get('oid') #什么是oid，获取当前页面的id。
    product = Product.objects.filter(pk=pk).first() #这句话怎么理解，是操作什么的
    context = {'product': product, 'itemslist': itemslist, 'cartItems': cartItems, 'totalprice': totalprice} #context的用途
    if oid:   #这句话怎么理解
        context['oid'] = oid
    return render(request, 'store/biaoge.html', context)   #如果存在oid这个id，那就返回给前端，如果不存在就不给。


# 新增结束


# 新增
@login_required(login_url='login')
@admin_only
def home1(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'store/dashboard.html', context)


# 添加订单查看View函数
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewOrders(request):
    orders = []
    data = cartData(request)
    cartItems = data['cartItems']
    totalprice = data['totalprice']
    itemslist = data['itemslist']
    us = Customer.objects.get(name=request.user.customer)
    category = Category.objects.get(name=19)
    for order in Order.objects.filter(Q(customer=us) & ~Q(userorderid=0) & Q(delstatus=0)).order_by(
            '-date_created').all():
        if order.product and order.product.category == category:
            orders.append(order)
    return render(request, 'store/design_orders.html',
                  {'orders': orders, 'itemslist': itemslist, 'cartItems': cartItems, 'totalprice': totalprice})


# 添加商品+上传图片
def uploadPic(request):
    base64_str_front = request.POST.get('imgFront')
    base64_str_back = request.POST.get('imgBack')
    state1 = request.POST.get('state1')
    state2 = request.POST.get('state2')
    jsondata = request.POST.get('jsondata')
    img_name = request.GET.get('name')
    price = request.POST.get('price')
    total = request.POST.get('total')
    pk = request.POST.get('pk')
    imgdata = request.POST.get('imgdata')
    if not base64_str_front or not base64_str_back or not state1 or not state2:
        return HttpResponse('No data')

    b_front = base64.b64decode(base64_str_front)
    b_back = base64.b64decode(base64_str_back)

    path = os.path.join(BASE_DIR, 'upload')
    if not os.path.exists(path):
        os.makedirs(path)

    file_path_front = os.path.join(path, str(time.time()) + '_front')
    file_path_back = os.path.join(path, str(time.time()) + '_back')

    with open(file_path_front, 'wb') as f:
        f.write(b_front)

    with open(file_path_back, 'wb') as f:
        f.write(b_back)

    # order = Order(
    #     name=img_name,
    #     status='Pending',
    #     picture_front=file_path_front,
    #     picture_back=file_path_back,
    #     state1=state1,
    #     state2=state2
    # )
    # order.save()
    category = Category.objects.get(name=19)
    # v = base64.b64decode(file_path_front)
    product = Product(
        name=img_name,
        category=category,
        price=price,
        pos=0,
        state1=state1,
        state2=state2,
        image_new=imgdata,
        jsondata=jsondata,
        total=total,
        choosepk=pk
    )
    product.save()
    # result = {"Code": 0, "Msg": "", "Data": product.id}
    return HttpResponse(product.id)
    # return redirect('userinfo/cart.html')


# 正反面图片存储
def zfpicsave(request):
    try:
        base64_str = request.POST.get('b64')
        img = base64.b64decode(base64_str)
        path = os.path.join(BASE_DIR, 'upload')
        if not os.path.exists(path):
            os.makedirs(path)
        imgpath = os.path.join(path, str(time.time()) + '_front')
        with open(imgpath, 'wb') as f:
            f.write(img)
        print('jin', imgpath)
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


# 下载图片
def downloadPic(request):
    order_id = request.GET.get('oid')
    pic_type = request.GET.get('type')
    if not order_id or not pic_type:
        return HttpResponse('No parameters')
    order = Order.objects.get(id=order_id)
    if pic_type == 'front':
        file_path = order.picture_front
    else:
        file_path = order.picture_back
    file = open(file_path, 'rb')
    file_response = FileResponse(file)
    return file_response


def designer_old(request):
    # 添加修改的模式，edit不为空时为修改图片
    edit = request.GET.get('edit', None)
    pk = request.GET.get('pk')
    if edit:
        edit = True
    else:
        edit = False
    order_id = None
    order_object = None
    if edit:
        order_id = request.GET.get('oid')
        if order_id:
            order_object = Order.objects.get(id=order_id)
    context = {'title': 'hello', 'edit': edit, 'order_id': order_id, 'order': order_object, "User": request.user,
               'pk': pk}
    return render(request, 'store/designer_old.html', context)


def designer(request):
    edit = request.GET.get('edit', None)
    pk = request.GET.get('pk')
    if edit:
        edit = True
    else:
        edit = False
    order_id = None
    order_object = None
    if edit:
        order_id = request.GET.get('oid')
        if order_id:
            order_object = Order.objects.get(id=order_id)
    context = {'title': 'designer_new', 'edit': edit, 'order_id': order_id, 'order': order_object, "User": request.user,
               'pk': pk}
    return render(request, "store/designer.html", context)


def homepage(request):
    # 添加修改的模式，edit不为空时为修改图片
    edit = request.GET.get('edit', None)
    if edit:
        edit = True
    else:
        edit = False
    order_id = None
    order_object = None
    if edit:
        order_id = request.GET.get('oid')
        order_object = Order.objects.get(id=order_id)
        context = {'title': 'hello', 'edit': edit, 'order_id': order_id, 'order': order_object}
        return render(request, "store/designer.html", context)
    else:
        data = cartData(request)

        cartItems = data['cartItems']

        id = request.GET.get('id');
        if id:
            products = Product.objects.filter(category_id=id)
        else:
            products = Product.objects.filter(category_id=110801)
        context = {'products': products, 'cartItems': cartItems}
        return render(request, 'store/homepage.html', context)


class MyOrder(View):                #为什么括号里是view？这个函数讲一下.类函数。
    def get(self, request):
        # order = Order.objects.filter(customer=request.user.customer)
        pg = request.GET.get('page', None)
        status = request.GET.get('status', None)
        page_num = int(pg if pg != None else 1)
        us = Customer.objects.get(name=request.user.customer)
        ordinfo = Order.objects.filter(Q(customer=us.id))
        orderitems = []
        #先查询当前页面的这些数据

        if status is None:
            paginator = Paginator(UserOrder.objects.filter(Q(customer=us)).order_by('-date_added').all(), 5) #如果状态不为空，那就查分页
        else:
            paginator = Paginator(
                UserOrder.objects.filter(Q(customer=us) & Q(status=status)).order_by('-date_added').all(), 5)

        total = paginator.num_pages         #开始判断分页
        page = paginator.page(page_num)
        prev_page_num = page_num - 1 if page_num > 1 else 1
        next_page_num = page_num + 1 if total > page_num else page_num
        if total < page_num:
            return redirect('/myhome')
        for item in page.object_list:
            ords = []
            totalprice = 0
            for ord in Order.objects.filter(Q(customer=us.id) & Q(userorderid=item.userorderid)):
                try:
                    jsondata_ziti_totoal = 0
                    try:
                        list = json.loads(ord.product.jsondata)
                        for l_item in list:
                            jsondata_ziti_totoal += int(l_item['Zxs'])
                    except:
                        pass

                    prd = ord.orderitem_set.first().product
                    totalprice += ord.get_cart_total
                    ords.append({
                        "productname": prd.name,
                        "productprice": ord.price,
                        "productitems": ord.get_cart_items,
                        "productimg": prd.imageURL,
                        "producttotalprice": ord.get_cart_total,
                        "jsondata_ziti_totoal": jsondata_ziti_totoal
                    })
                except:
                    pass
            orderitems.append({
                "orderid": item.userorderid,
                "ords": ords,
                "createtime": item.date_added.strftime("%Y-%m-%d %H:%M:%S"),
                "ordertotalprice": totalprice,
                "yunfei": item.yunfei,
                "status": item.status,
                "ztaddress": item.ztaddress
            })
        uname = request.session.get('username')
        return render(
            request,
            'userinfo/myorder.html',
            {
                'uname': uname,
                'dinfo': ordinfo,
                'status': status if status is None else int(status),
                'page_num': page_num,
                'total': total,
                'orderitems': orderitems,
                'prev_page_num': prev_page_num,
                'next_page_num': next_page_num,
                'page': page,
                'page_range': paginator.get_elided_page_range()
            }
        )


class EditPwd(View):
    def get(self, request):
        uname = request.session.get('username')
        return render(request, 'userinfo/editpwd.html', {'uname': uname})

    def post(self, request):
        uname = request.session.get('username')
        pwd = request.POST.get('pwd')
        newpwd = request.POST.get('newpwd')
        newpwd1 = request.POST.get('newpwd1')
        if newpwd != newpwd1:
            return render(request, 'userinfo/editpwd.html', {'uname': uname, 'msg': '两次密码不一致'})

        res = request.user.check_password(pwd)  # 返回值为布尔值
        if res:
            request.user.set_password(newpwd)  # 只是修改对象属性
            request.user.save()  # 这才是真正的操作数据库修改密码
            logout(request)
            return redirect('/login/')
        else:
            return render(request, 'userinfo/editpwd.html', {'uname': uname, 'msg': '原密码错误'})


class editadd(View):

    def post(self, request):
        did = request.POST.get('did')
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        state = request.POST.get('state')  # 国家
        county = request.POST.get('county')  # 省份、城市
        city = request.POST.get('city')  # 城市
        addinfo = request.POST.get('addinfo')
        gs = request.POST.get('gs')
        moren = request.POST.get('moren')
        if postcode and name and phone and state and county and city and addinfo:
            pass
        else:
            return HttpResponse('请填写必填字段')
        add = ShippingAddress.objects.get(id=did)
        if moren:
            ShippingAddress.objects.filter(Q(customer=request.user.customer) & Q(status=1)).update(status=0)
            add.status = 1
        add.address = addinfo
        add.country = state
        add.county = county
        add.city = city
        add.gs = gs
        add.postcode = postcode
        # add.date_added = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        add.date_added = timezone.now()
        add.phone = phone
        add.uname = name
        add.save()
        ff = ShippingAddress.objects.get(id=did)
        return redirect('/address/')


class MyInfo(View):
    def get(self, request):
        uname = request.session.get('username')
        uinfo = Customer.objects.get(name=uname)
        print(uinfo.phone)
        msg = request.session.get('msg', '')
        return render(request, 'userinfo/myinfo.html', {'uname': uname, 'uinfo': uinfo, 'msg': msg})

    def post(self, request):
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        uinfo = Customer.objects.get(user=request.user)
        uinfo.phone = phone
        uinfo.email = email
        uinfo.save()
        request.session['msg'] = '保存成功'
        return redirect('/myinfo/')


# 获取购物车内数据存储到session内
class GetShopInfoSession(View):   #这个函数怎么理解
    def post(self, request):
        received_json_data = json.loads(request.body) #json.loads(request.body)怎么理解，为什么要这么做，把请求的数据转化成json。
        target = received_json_data['data']['val']   #received_json_data['data']['val']是干嘛用的，键值对，在received_json_data这个字典里取值
        zong = received_json_data['data']['jia']
        shu = received_json_data['data']['shu']
        key = str(uuid.uuid1())[:5]
        request.session['key'] = key   #这句话是干嘛用的,上面获取了key变量，把key变量赋值给session, session就是用户登录状态
        # print(zong)
        # print(shu)
        # # 处理数据 并存到session内或数据库内
        # print(target)
        uname = request.session.get('username', '000') #这句话怎么理解，是什么样的操作，从session里面查询2个值
        Temporary.objects.create(uname=uname, name='000', imageURL='000', nums='000', danjia='000', ttok=key
                                 , type='000', zongshu=shu, jiage=zong
                                 )    #Temporary.objects.create是什么意思，怎么理解，是什么操作。temporary是一个表，往这个表里插入数据。
        for i in target: #这个for循环是想干嘛
            cid = i.split('|')[0] #啥意思，为什么要split，取split后列表里对第几个值。中括号里面对数字就是第几个值。
            nums = i.split('|')[1]
            imgurl = i.split('|')[2]
            name = i.split('|')[3]
            jia = i.split('|')[4]
            Temporary.objects.create(uname=uname, name=name, imageURL=imgurl, nums=nums,
                                     danjia=jia.replace('\'', '').replace(']', ''), ttok=key
                                     , type=cid.replace('\'', '').replace('[', ''), zongshu='000', jiage='000'
                                     )
        data = {
            'data': 'OK'
        } #为什么'data': 'OK'，有什么用。声明了一个字典。
        return JsonResponse(data)


class Address(View):     #这个函数是干嘛用的？这个是我的地址里修改地址用的。把请求request的数据放到函数里当参数，然后执行下面的语句。
    def get(self, request):
        try:
            uname = request.session.get('username')
            us = Customer.objects.get(name=request.user.customer)
            add = ShippingAddress.objects.filter(customer_id=us.id).order_by('-status')
            code = request.GET.get('code', '')
            did = request.GET.get('id')
            if did:
                addinfo = ShippingAddress.objects.get(id=did)
                return render(request, 'userinfo/address.html',
                              {'info': addinfo, 'did': did, 'uname': uname, 'add': add, 'code': code, 'msg': ""})
            return render(request, 'userinfo/address.html', {'uname': uname, 'add': add, 'code': code, 'msg': ""})
        except Exception as e:
            return render(request, 'store/login.html')

    def post(self, request):
        d = ShippingAddress.objects.filter(customer=request.user.customer)
        # 判断地址数量 如果大于4 就返回消息。下面if先判断地址不能多于20条。判断完里再执行1044之后的，查询用户填好然后post的数据然后执行之后的代码。
        if len(d) >= 20:
            uname = request.session.get('username')
            us = Customer.objects.get(name=request.user.customer)
            add = ShippingAddress.objects.filter(customer_id=us.id).order_by('-status')
            return render(request, 'userinfo/address.html',
                          {'uname': uname, 'add': add, 'code': '', 'msg': '收货地址最多20个'})
        us = Customer.objects.get(name=request.user.customer)
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        state = request.POST.get('state')  # 国家
        county = request.POST.get('county')  # 城市、省份
        city = request.POST.get('city')  # 城市
        addinfo = request.POST.get('addinfo')
        gs = request.POST.get('gs')
        moren = request.POST.get('moren')
        if moren:
            try:
                d = ShippingAddress.objects.get(customer=request.user.customer, status=1)
                d.status = 0
                d.save()
            except:
                pass            #如果是默认的，那么执行下面的，创建新地址
            ShippingAddress.objects.create(
                customer=request.user.customer,
                address=addinfo,
                country=state,
                county=county,
                city=city,
                postcode=postcode,
                gs=gs,
                # date_added=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                date_added=timezone.now(),
                status='1',
                phone=phone,
                uname=name
            )               #如果不是默认的，先判断必填字段有没有填写，如果填好了，那么就创建新地址。
        else:
            if postcode and name and phone and state and county and city and addinfo:
                pass
            else:
                return HttpResponse('请填写必填字段')
            ShippingAddress.objects.create(
                customer=request.user.customer,
                address=addinfo,
                country=state,
                county=county,
                city=city,
                postcode=postcode,
                date_added=datetime.datetime.now(),
                status='0',
                phone=phone,
                uname=name
            )
        return redirect('/address/')


class Address2(View):                   #这个函数是干嘛用的？这个是结算里修改地址用的
    def get(self, request):
        try:
            uname = request.session.get('username')
            us = Customer.objects.get(name=request.user.customer)
            add = ShippingAddress.objects.filter(customer_id=us.id).order_by('-status')
            code = request.GET.get('code', '')
            did = request.GET.get('id')
            if did:
                addinfo = ShippingAddress.objects.get(id=did)
                return render(request, 'userinfo/address.html',
                              {'info': addinfo, 'did': did, 'uname': uname, 'add': add, 'code': code, 'msg': ""})
            return redirect(request, 'userinfo/address.html', {'uname': uname, 'add': add, 'code': code, 'msg': ""})
        except Exception as e:
            return render(request, 'store/login.html')

    def post(self, request):
        d = ShippingAddress.objects.filter(customer=request.user.customer)
        # 判断地址数量 如果大于4 就返回消息
        if len(d) >= 20:
            uname = request.session.get('username')
            us = Customer.objects.get(name=request.user.customer)
            add = ShippingAddress.objects.filter(customer_id=us.id).order_by('-status')
            return render(request, 'userinfo/address.html',
                          {'uname': uname, 'add': add, 'code': '', 'msg': '收货地址最多20个'})
        us = Customer.objects.get(name=request.user.customer)
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        state = request.POST.get('state')  # 国家
        county = request.POST.get('county')  # 城市、省份
        city = request.POST.get('city')  # 城市
        addinfo = request.POST.get('addinfo')
        gs = request.POST.get('gs')
        moren = request.POST.get('moren')
        id = request.POST.get('id')
        if moren:
            try:
                d = ShippingAddress.objects.get(customer=request.user.customer, status=1)
                d.status = 0
                d.save()
            except:
                pass
            ShippingAddress.objects.filter(id=id).update(
                customer=request.user.customer,
                address=addinfo,
                country=state,
                county=county,
                city=city,
                postcode=postcode,
                gs=gs,
                # date_added=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                date_added=timezone.now(),
                status='1',
                phone=phone,
                uname=name
            )
        else:
            if postcode and name and phone and state and county and city and addinfo:
                pass
            else:
                return HttpResponse('请填写必填字段')
            ShippingAddress.objects.filter(id=id).update(
                customer=request.user.customer,
                address=addinfo,
                country=state,
                county=county,
                city=city,
                postcode=postcode,
                date_added=timezone.now(),
                status='0',
                phone=phone,
                uname=name
            )
        return redirect('/checkout/')


class checkoutaddress(View):      #这个函数的故事流程是怎么样的，类视图，view是底层代码，view是继承
    def post(self, request):    #POST在相同的页面做post请求，输入地址信息然后做post请求，执行语句。
        d = ShippingAddress.objects.filter(customer=request.user.customer)
        # 判断地址数量 如果大于4 就返回消息
        if len(d) >= 20:
            uname = request.session.get('username')
            us = Customer.objects.get(name=request.user.customer)
            add = ShippingAddress.objects.filter(customer_id=us.id).order_by('-status')
            return render(request, 'userinfo/address.html',
                          {'uname': uname, 'add': add, 'code': '', 'msg': '收货地址最多20个'})
        us = Customer.objects.get(name=request.user.customer)
        postcode = request.POST.get('postcode')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        state = request.POST.get('state')  # 国家
        county = request.POST.get('county')  # 城市、省份
        city = request.POST.get('city')  # 城市
        addinfo = request.POST.get('addinfo')
        gs = request.POST.get('gs')
        moren = request.POST.get('moren')
        if moren:
            try:
                d = ShippingAddress.objects.get(customer=request.user.customer, status=1)
                d.status = 0
                d.save()
            except:
                pass
            ShippingAddress.objects.create(
                customer=request.user.customer,
                address=addinfo,
                country=state,
                county=county,
                city=city,
                postcode=postcode,
                gs=gs,
                # date_added=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                date_added=timezone.now(),
                status='1',
                phone=phone,
                uname=name
            )
        else:
            if postcode and name and phone and state and county and city and addinfo:
                pass
            else:
                return HttpResponse('请填写必填字段')
            ShippingAddress.objects.create(
                customer=request.user.customer,
                address=addinfo,
                country=state,
                county=county,
                city=city,
                postcode=postcode,
                date_added=datetime.datetime.now(),
                status='0',
                phone=phone,
                uname=name
            )
        return redirect('/checkout/')


def deladd(request):
    try:
        id = request.GET.get('id')
        ShippingAddress.objects.get(id=id).delete()
    except Exception as e:
        pass
    return redirect('/address/')


def setdefault(request):
    try:
        id = request.GET.get('id')
        ShippingAddress.objects.filter(customer=request.user.customer).update(status=0)
        ShippingAddress.objects.filter(id=id).update(status=1)
    except Exception as e:
        print(e)
        pass
    return redirect('/address/')


def checkoutsetdefault(request):
    try:
        id = request.GET.get('id')
        ShippingAddress.objects.filter(customer=request.user.customer).update(status=0)    #这里面update(status = 0)是什么意思？应该就是把状态改成未付款
        ShippingAddress.objects.filter(id=id).update(status=1)   #这里面status=1又是什么意思？把状态改成1对应的状态
    except Exception as e:
        print(e)
        pass
    return redirect('/checkout/')


def adduserorder(request):
    try:
        jiage = float(request.POST.get('jiage'))
        yunfei = float(request.POST.get('yunfei'))
        shui = float(request.POST.get('shui'))
        addressid = request.POST.get('addressid')
        ztaddress = request.POST.get('ztaddress')
        with transaction.atomic():        #with语句是干嘛用的，然后.atomic是什么意思，这句话是什么意思？整个with 语句表达了什么？自动提交，提交到我们的数据库的表。transaction.atomic: 原子性，给别人转钱失败了就又回到自己的账户里。
            us = Customer.objects.get(name=request.user.customer)
            if not ztaddress:
                address = ShippingAddress.objects.get(id=int(addressid))
                userorder = UserOrder(
                    customer=us,
                    addressid=address,
                    price=jiage,
                    yunfei=yunfei,
                    shui=shui
                )
            else:
                userorder = UserOrder(
                    customer=us,
                    price=jiage,
                    yunfei=yunfei,
                    shui=shui,
                    ztaddress=ztaddress
                )
            userorder.save()
            order = Order.objects.filter(Q(customer=us) & Q(userorderid=0))
            order.update(userorderid=userorder.userorderid)
            OrderItem.objects.filter(order=order.first()).update(userorderid=userorder.userorderid)
            return HttpResponse(json.dumps({
                "code": 0,
                "msg": "结算成功",
                "data": userorder.userorderid
            }))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            "code": -1,
            "msg": "结算失败",
            "data": ""
        }))


def updateuserorder(request):
    try:
        order_id = request.POST.get('order_id', None)   #这里面括号里为什么有两个，为什么有None?这些都是AJAX传过来的数值
        UserOrder.objects.filter(userorderid=order_id).update(status=2)   #这里面status=2是什么意思？应该就是把状态改为已付款
        u = UserOrder.objects.filter(userorderid=order_id)
        try:
            send_email(u.first().customer.email, order_id)  # 调用发送邮件
        except:
            pass
        return HttpResponse(json.dumps({
            "code": 0,
            "msg": "结算成功",
            "data": {
                "a1": u.first().price,
                "a2": u.first().status,
            }
        }))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            "code": -1,
            "msg": "结算失败",
            "data": ""
        }))


def deluserorder(request):
    try:
        userorderid = float(request.GET.get('id'))
        with transaction.atomic():
            us = Customer.objects.get(name=request.user.customer)
            UserOrder.objects.filter(Q(customer=us) & Q(userorderid=userorderid)).delete()
            order = Order.objects.filter(Q(customer=us) & Q(userorderid=userorderid))
            OrderItem.objects.filter(order=order.first()).delete()
            order.delete()
    except Exception as e:
        print(e)
    return redirect('/myhome/')


def updateproductname(request):
    try:
        pid = request.POST.get('pid')
        name = request.POST.get('name')
        Product.objects.filter(id=pid).update(name=name)
        return HttpResponse(json.dumps({
            "code": 0
        }))
    except Exception as e:
        return HttpResponse(json.dumps({
            "code": -1
        }))


def twoway(request):
    return render(request, 'store/twoway.html')


def youkedizhi(request):
    return render(request, 'store/youkedizhi.html')


def youkecheckout(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        items = []
        itemstotal = 0
        totalprice = 0
        no_dingzhi_totalprice = 0
        yunfei = 0
        for item in cart.keys():
            product = Product.objects.filter(id=item.split('_')[0]).first()     #这句话什么意思？.first是什么意思？取整个列表符合条件的第一条数据
            items.append({
                'img': product.imageURL,
                'name': product.name,
                'price': product.price,
                'quantity': cart[item]['quantity']
            })                                              #items.append是什么意思？往列表中追加数据
            if not product.jsondata:
                no_dingzhi_totalprice += (float(product.price) * int(cart[item]['quantity']))
            itemstotal += int(cart[item]['quantity'])
            totalprice += (float(product.price) * int(cart[item]['quantity']))
        if 0 < no_dingzhi_totalprice and no_dingzhi_totalprice < 100:
            yunfei = 10
        shui = totalprice - (totalprice / 1.2)
        amount = yunfei + totalprice
        context = {'items': items, 'itemstotal': itemstotal, 'cartItems': itemstotal, 'totalprice': totalprice,
                   'yunfei': yunfei, 'shui': shui, 'amount': amount}
        return render(request, 'store/youkecheckout.html', context)
    except:
        return redirect('/')


from urllib.parse import unquote
from django.forms.models import model_to_dict


def invoice(request):
    gmf = request.GET.get('gmf')
    gmx = unquote(request.GET.get('gmx'))
    print(gmx)
    yfje = request.GET.get('yfje')
    bz = request.GET.get('bz')
    no = str(gmf + "-" + datetime.now().strftime('%Y%m%d%H%M'))
    date = str(datetime.now().strftime('%d/%m/%Y'))
    data1 = model_to_dict(ShippingAddress.objects.filter(customer=gmf).first())
    list_product = []
    list_total = []
    for i in gmx.split('^'):
        try:
            print(i)
            coll = {}
            info = i.split('_')
            price = (Product.objects.get(name=info[0]))
            coll['name'] = info[0]
            coll['price'] = price.price
            coll['quantity'] = info[1]
            coll['total_price'] = float(price.price) * int(info[1])
            coll['img'] = price.image.url
            coll['info'] = price.info
            list_total.append(price.price * int(info[1]))
            list_product.append(coll)
        except:
            pass

    yue = sum(list_total) - float(yfje)
    data2 = {'list_product': list_product, 'list_total': sum(list_total), 'list_total20': 1.2 * sum(list_total),
             'list_total0': 0.2 * sum(list_total)}
    # return JsonResponse()
    return render(request, 'invoice/invoice.html',
                  {'date': date, 'no': no, 'data1': data1, 'data2': data2, 'yue': yue, 'bz': bz, 'yfje': yfje})


def invoice2(request):
    gmf = request.GET.get('gmf')
    gmx = unquote(request.GET.get('gmx'))
    print(gmx)
    yfje = request.GET.get('yfje')
    bz = request.GET.get('bz')
    no = str(gmf + "-" + datetime.now().strftime('%Y%m%d%H%M'))
    date = str(datetime.now().strftime('%d/%m/%Y'))
    data1 = model_to_dict(ShippingAddress.objects.filter(customer=gmf).first())
    list_product = []
    list_total = []
    lens = len(gmx.split('^'))
    print(
        lens
    )
    if lens <= 6:
        pages = 1
    else:
        if (lens - 6) % 2 == 0:
            pages = (lens - 6) // 10 + 1
        else:
            pages = (lens - 6) // 10 + 2
    print(pages)
    for i in gmx.split('^'):
        try:
            print(i)
            coll = {}
            info = i.split('_')
            product = (Product.objects.get(name=info[0]))
            coll['name'] = product.name
            coll['price'] = product.price
            coll['quantity'] = info[1]
            coll['total_price'] = float(product.price) * int(info[1])
            coll['img'] = product.image.url
            coll['info'] = product.info
            list_total.append(product.price * int(info[1]))
            list_product.append(coll)
        except:
            pass
    list_all2 = []
    print(pages)
    for p in range(1, pages + 1):
        list_all = []
        if p == 1:
            list_all.append(list_product[0:6])
        else:
            list_all.append(list_product[(p - 2) * 10 + 6:(p - 1) * 10 + 16])  # 6-16 16-26 26-36
        list_all2.append(list_all)

    yue = sum(list_total) - float(yfje)
    data2 = {'list_product': list_all2, 'list_total': sum(list_total), 'list_total20': 1.2 * sum(list_total),
             'list_total0': 0.2 * sum(list_total)}
    # return JsonResponse()
    return JsonResponse({'date': date, 'no': no, 'data1': data1, 'data2': data2, 'yue': yue, 'bz': bz, 'yfje': yfje})


# def jiemian(request):
#     return render(request, 'invoice/jiemian.html')

def create_pdf(request):
    return render(request, 'invoice/jiemian.html')


def invoice3(request):
    gmf = request.GET.get('gmf')
    gmx = unquote(request.GET.get('gmx'))
    yfje = request.GET.get('yfje')
    bz = request.GET.get('bz')

    items = []
    groups = []
    total = 0

    for pair in gmx.split('^'):

        if len(pair.strip()) <= 0:
            continue

        name, quantity = pair.split('_')
        product = (Product.objects.get(name=name))

        item = {
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'total_price': float(product.price) * int(quantity),
            'img': product.image.url,
            'info': product.info
        }
        items.append(item)

        total += item['total_price']

    # 分组的关键点
    split_points = [(2, 6), (6, 11), (6, 11), (6, 11), (6, 11), (6, 11), (6, 11), (6, 11), (6, 11)]

    # 把查询出来的数据适当分组（即分页）
    for min_point, max_point in split_points:
        if len(items) == 0:
            groups.append({'items': items})
            break
        elif len(items) <= min_point:
            groups.append({'items': items})
            break
        elif min_point < len(items) <= max_point:
            groups.append({'items': items[0: len(items)]})
            del items[0: len(items)]
        else:
            groups.append({'items': items[0: max_point]})
            del items[0: max_point]

    # 第一个分组要加上 banner info 内容块
    groups[0]['banner'] = True
    groups[0]['info'] = True

    # 最后一个分组要加上 balance、cart、footer 内容块
    groups[-1]['balance'] = True
    groups[-1]['cart'] = True
    groups[-1]['footer'] = True

    no = str(gmf + "-" + datetime.now().strftime('%Y%m%d%H%M'))
    shopping_address = model_to_dict(ShippingAddress.objects.filter(customer=gmf).first())
    date = str(datetime.now().strftime('%d/%m/%Y'))
    yue = total - float(yfje)
    total20 = 1.2 * total
    total0 = 0.2 * total
    yue2 = total20 - float(yfje)

    return render(request, 'invoice/invoice.3.html', {
        'groups': groups,
        'no': no,
        'shopping_address': shopping_address,
        'date': date,
        'bz': bz,
        'yfje': yfje,
        'yue': yue,
        'total': total,
        'total20': total20,
        'total0': total0,
        'yue2': yue2,
    })


def youke_pay(request):
    try:
        data = json.loads(request.POST.get('json_data'))   #这里youkeorder是表。cmd + click可以从model找到
        ykdata = youkeorder(
            receiver=data['receiver'],
            get_way=data['get_way'],
            phone=data['phone'],
            email=data['email'],
            company=data['company'],
            totalprices=float(data['TotalPrices']),
            yunfei=float(data['Yunfei']),
            amount=float(data['Amount']),
            shui=float(data['Shui']),
            nation=data['nation'],
            province=data['province'],
            city=data['city'],
            postcode=data['postcode'],
            addinfo=data['addinfo'],
            items=int(data['Items']),
            itemsjson=json.dumps(data['ItemsJson'])
        )
        ykdata.save()           #这句话是什么意思，存到哪里？存到数据库，ykdata是变量，存到youkeorder表。
        send_email(data['email'], ykdata.id)  # 调用发送邮件
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': 'error',
            'data': ''
        }))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': 'error',
            'data': ''
        }))


# 客户下单完成自动发邮件

# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string
#
# def success(request, email_address):
#     template = render_to_string('email/email_template.html', {'name':request.Customer.objects.get(name=email_address)}, {'orderid':request.item.userorderid}) #name是用户的名字
#
#     email = EmailMessage(
#         'Thanks for purchasing the eCommerce course!', #邮件标题
#         "Hi {{name}}!"
#         ""
#         "Thanks for placing the order with AutoSqueak!"
#         "The order number is {{orderid}}"
#         "If you have any question please do not hesitate to contact us with your order number provided."
#         ""
#         "Kind regards,"
#         "AutoSqueak", #邮件内容body
#         settings.EMAIL_HOST_USER, #发件人邮箱
#         ['dennis@dess.com'], #收件人邮箱，是当前购买的登录的用户的邮箱，可以是list形式多人多个邮箱#
#     )
#     email.fail_silently=False
#     email.send()
#
#     project = Project.objects.get(id=uid)
#     context = {'project':project}
#
#     return render(request, 'base/success.html', context)

def send_email(email, orderid):
    """
    发送邮件
    :param email: 接收者
    :param orderid: 订单号
    :return:
    """
    try:
        from django.core.mail import EmailMessage
        from django.conf import settings
        from django.template.loader import render_to_string
        template = render_to_string('email/email_template.html', {'name': email, 'orderid': orderid})  # name是用户的名字

        email = EmailMessage(
            'Thanks for purchasing the eCommerce course!',  # 邮件标题
            template,  # 邮件内容body
            settings.EMAIL_HOST_USER,  # 发件人邮箱
            [email],  # 收件人邮箱，是当前购买的登录的用户的邮箱，可以是list形式多人多个邮箱#
        )
        email.fail_silently = False
        email.send()
        return True
    except Exception as e:
        return False

    # project = Project.objects.get(id=uid)
    # context = {'project':project}

    # return render(request, 'base/success.html', context)
