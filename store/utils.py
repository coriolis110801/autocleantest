import json

from django.db.models import Q

from .models import *
from django.utils import timezone


def cookieCart(request):                #这个函数产生了各种结算和购物车需要的数据
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    cartItems = 0  # 商品总数
    totalprice = 0  # 商品总价
    itemslist = []
    for k, i in enumerate(cart):
        try:
            product = Product.objects.get(id=i.split('_')[0])
            if product:
                itemslist.append({
                    'id': k,
                    'img': product.imageURL,
                    'name': product.name,
                    'price': cart[i]['price'],
                    'color': cart[i]['color'],
                    'combo': cart[i]['type'],
                    'totalprice': float(cart[i]['price']) * int(cart[i]['quantity']),
                    'productid': product.id,
                    'quantity': cart[i]['quantity']
                })
                cartItems += int(cart[i]['quantity'])
                totalprice += (float(cart[i]['price']) * int(cart[i]['quantity']))
        except Exception as e:
            pass
    newitemslist = reversed(itemslist)
    return {'cartItems': cartItems, 'itemslist': newitemslist, 'totalprice': totalprice}


def cartData(request):                  #这个函数也产生了各种结算和购物车需要的数据
    cartItems = 0  # 商品总数
    totalprice = 0  # 商品总价
    order = None
    items = None
    itemslist = []

    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            for item in Order.objects.filter(Q(customer=customer) & Q(userorderid=0)).order_by('-date_created'):
                order, adddata = Order.objects.get_or_create(customer=customer, complete=False, color=item.color,
                                                             combo=item.combo, price=item.price, userorderid=0,
                                                             delstatus=0, product=item.product)
                temp = order.orderitem_set.order_by('date_added').all()
                if temp:
                    jsondata_ziti_totoal = 0
                    try:
                        list = json.loads(temp[0].product.jsondata)
                        for l_item in list:
                            jsondata_ziti_totoal += int(l_item['Zxs'])
                    except:
                        pass
                    itemslist.append({
                        'id': temp[0].id,
                        'img': temp[0].product.imageURL,
                        'name': temp[0].product.name,
                        'price': temp[0].price,
                        'color': temp[0].color,
                        'combo': temp[0].combo,
                        'totalprice': temp[0].get_total,
                        'productid': temp[0].product.id,
                        'quantity': temp[0].quantity,
                        'jsondata_ziti_totoal':jsondata_ziti_totoal
                    })
                    cartItems += order.get_cart_items
                    totalprice += order.get_cart_total
        else:
            r = cookieCart(request)
            return r
    except Exception as e:
        print(e)
        pass

    return {'cartItems': cartItems, 'itemslist': itemslist, 'totalprice': totalprice}


def guestOrder(request, data):              #这个函数产生了各种游客结算和购物车需要的数据
    try:
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['cartItems']
        print('获取了：', items)
        customer, created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name = name
        customer.save()
        print('jinrulexiam')
        for item in items:
            product = Product.objects.get(id=item['productid'])
            order, created = Order.objects.get_or_create(customer=customer, complete=False, color=item['color'],
                                                         combo=item['combo'],
                                                         price=item['price'])
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, color=item['color'],
                                                                 combo=item['combo'],
                                                                 price=item['price'])
        print('ffdsf')
        return customer, None
    except Exception as e:
        print("guestOrder出错：", e)
        return None, None


def guestordertodb(request):
    cookieData = cookieCart(request)        #从utils的调用第一个函数里面的request作为参数
    items = cookieData['itemslist']         #调用缓存的数据
    customer = request.user.customer
    for item in items:
        product = Product.objects.get(id=item['productid'])
        order, created = Order.objects.get_or_create(customer=customer, product=product, complete=False,
                                                     color=item['color'], combo=item['combo'],
                                                     price=item['price'], userorderid=0)
        order.date_created = timezone.now()
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, color=item['color'], combo=item['combo'],
                                                             price=item['price'])
        orderItem.quantity = (orderItem.quantity + int(item['quantity']))
        orderItem.date_added = timezone.now()
        orderItem.save()            #遍历120-123行的数据，然后在数据库创建新数据
        if orderItem.quantity <= 0:
            orderItem.delete()
