from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from .views import MyOrder, Address, Address2, editadd, EditPwd, MyInfo, queryproducttotal, checkoutaddress

# urlpatterns += staticfiles_urlpatterns()

urlpatterns = [

    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    #  新增开始
    path('dashboard/', views.home, name="home"),
    path('myorders/', views.myorders, name="myorders"),
    path("home/", views.homepage, name="homepage"),
    path('dashboard2', views.dashboard, name='dashboard'),
    path('user/', views.userPage, name="user-page"),

    path('account/', views.accountSettings, name="account"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('detail/', views.slider, name="detail"),  # 商品详情
    path('biaoge/', views.biaoge, name="biaoge"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    #  新增结束

    # Leave as empty string for base url
    path("about/", views.about, name="about"),
    path("", views.homepage, name="homepage"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),
    path('store/', views.store, name="store"),
    path('shapes/', views.shapes, name="shapes"),
    path('search', views.search, name="search"),
    #	path('import', views.search, name="search"),
    path('cart/', views.cart, name="cart"),  # 购物车

    path('update_item/', views.update_item, name="update_item"),  # 添加购物车
    path('process_order/', views.process_order, name="process_order"),

    # test_email
    path('test_email/', views.test_email, name="test_email"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"),
         name="password_reset_complete"),

    # 新增
    # 添加URL
    path('view_order/', views.viewOrders, name='view_orders'),

    # 添加图片上传接口
    path('upload_pic/', views.uploadPic, name='upload_pic'),

    # 下载图片的接口
    path('download_pic/', views.downloadPic, name='download_pic'),

    path('designer/', views.designer_old, name="designer_old"),
    path('designer_new/', views.designer, name="designer"),

    path('home1', views.home1, name="home1"),

    path('myhome/', MyOrder.as_view(), name='view_orders'),  # 个人中心-我的订单
    path('address/', Address.as_view()),  # 地址管理
    path('address2/', Address2.as_view()),  # 地址管理2
    path('checkout/address/', checkoutaddress.as_view()),  # 结算页面的地址管理
    path('editpwd/', EditPwd.as_view()),  # 修改密码
    path('myinfo/', MyInfo.as_view()),  # 基本信息
    path('editadd/', editadd.as_view()),  # 修改地址
    path('getshopinfo/', views.GetShopInfoSession.as_view()),  # 购物车“继续”
    path('queryproducttotal', queryproducttotal),  # 查询商品库存与价格

    path('deladd/', views.deladd),  # 删除地址
    path('setdefault/', views.setdefault),  # 设置默认地址
    path('checkoutsetdefault/', views.checkoutsetdefault),  # 结算页面设置默认地址

    path('checkout/', views.checkout, name="checkout"),  # 结算页面
    path('adduserorder/', views.adduserorder),  # 添加用户订单
    path('updateuserorder/', views.updateuserorder),  # 修改用户订单状态
    path('deluserorder/', views.deluserorder),  # 删除用户订单

    path('updateproductname/', views.updateproductname),  # 修改商品名称
    path('adduserorder_query/', views.adduserorder_query),  # 编辑checkout的默认地址
    path('twoway/', views.twoway),  # 2种结算方式
    path('youkedizhi/', views.youkedizhi),  # 游客结算填写地址
    path('youkecheckout/', views.youkecheckout),  # 游客结算付款
    path('invoice/', views.invoice),  # 游客结算付款
    path('create_pdf/', views.create_pdf),  # 游客结算付款
    path('invoice2/', views.invoice2),  # 游客结算付款
    path('invoice3/', views.invoice3),  # 游客结算付款

    path('youke_pay/', views.youke_pay),  # 游客结算付款

]
