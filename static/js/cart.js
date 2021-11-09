var updateBtns = document.getElementsByClassName('update-cart')


for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var color = this.dataset.color
        var type = this.dataset.combo
        var price = parseFloat(this.dataset.price)
        var count = parseInt(this.dataset.count)
        var action = this.dataset.action

        if (user == 'AnonymousUser') {
            addCookieItem(productId, color, type, price, count, action)
        } else {
            updateUserOrder(productId, color, type, price, count, action)
        }
    })
}

function updateUserOrder(productId, color, type, price, count, action) {
    console.log('updateUserOrder,User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'count': count,
            'color': color,
            'type': type,
            'price': price,
            'action': action
        })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload()
            //location.href = '/cart/'
        });
}

function addCookieItem(productId, color, type, price, count, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId + "_" + color + "_" + type + "_" + price] == undefined) {
            cart[productId + "_" + color + "_" + type + "_" + price] = {
                'quantity': count,
                "color": color,
                "type": type,
                "price": price
            }

        } else {
            cart[productId + "_" + color + "_" + type + "_" + price]['quantity'] += count
        }
    }

    if (action == 'remove') {
        cart[productId + "_" + color + "_" + type + "_" + price]['quantity'] -= count

        if (cart[productId + "_" + color + "_" + type + "_" + price]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[productId + "_" + color + "_" + type + "_" + price];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
    //location.href = '/cart/'
}

function updateUserOrder_d(productId, color, type, price, count, action) {
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'color': color,
            'type': type,
            'price': price,
            'count': count,
            'action': action
        })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            alert("添加购物车成功！")
            //location.reload()
            location.href = '/cart/'
        });
}

function addCookieItem_d(productId, color, type, price, count, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId + "_" + color + "_" + type + "_" + price] == undefined) {
            cart[productId + "_" + color + "_" + type + "_" + price] = {
                'quantity': count,
                "color": color,
                "type": type,
                "price": price
            }

        } else {
            cart[productId + "_" + color + "_" + type + "_" + price]['quantity'] += count
        }
    }

    if (action == 'remove') {
        cart[productId + "_" + color + "_" + type + "_" + price]['quantity'] -= count

        if (cart[productId + "_" + color + "_" + type + "_" + price]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[productId + "_" + color + "_" + type + "_" + price];
        }
    }
    console.log('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    alert("添加购物车成功！")
    //location.reload()
    location.href = '/cart/'
}
