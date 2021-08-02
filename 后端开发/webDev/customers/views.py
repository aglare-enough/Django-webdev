from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse
from customers.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from customers.utils.jwt_auth import create_token
from datetime import datetime
from webDev.settings import JWT_AUTH
from customers.extension.auth import authen
from products.models import Classify,Product
from customers.models import Order,PayedOrder,HisOrder
from json import loads
#from rest_framework.views import APIView #导入APIView

def login_page(request):
    #pass
    return JsonResponse({'ret':0})
    #return render(request,html)

def rigister_page(request):
    pass

def login_(request):
    username=request.POST.get('username')
    #print(username)
    password=request.POST.get('password')
    #print(password)
    user = authenticate(username=username,password=password)
    if user:
        #login(request,user)
        payload={
            'user_id':user.id,
            'username':username,
            'exp':''
        }
        token=create_token(payload=payload,timeout=JWT_AUTH['JWT_EXPIRATION_DELTA'])
        user.is_active=True
        user.jwt_version = str(datetime.now()).replace(' ','')
        user.save()
        return JsonResponse({'ret':0,'token':token,'version':user.jwt_version})
    else:
        user=User.objects.filter(username=username).first()
        if user is None:
            return JsonResponse({'ret':1,'msg':'用户名不存在'})
        else:
            if user.password==password:
                payload = {
                    'user_id': user.id,
                    'username': username,
                    'exp': ''
                }
                token = create_token(payload=payload, timeout=JWT_AUTH['JWT_EXPIRATION_DELTA'])
                user.jwt_version=str(datetime.now()).replace(' ','')
                user.is_active=True
                user.save()
                return JsonResponse({'ret': 0, 'token': token,'version':user.jwt_version,'user_id':user.id})
            else:
                return JsonResponse({'ret':1,'msg':'密码错误'})


def rigister(request):
    username=request.POST.get('username')
    u = User.objects.filter(username=username)
    #print(username)
    if any(u):
        return JsonResponse({'ret':1,'msg':'用户名已存在'})
    password=request.POST.get('password')
    #print(password)
    phonenumber=request.POST.get('phonenumber')
    mail=request.POST.get('email')
    p=User.objects.filter(phonenumber=phonenumber)
    if any(p):
        return JsonResponse({'ret':1,'msg':'该电话号码已被注册'})
    date_joined=str(datetime.now())
    c = User(username=username,password=password,phonenumber=phonenumber,is_superuser=False,is_active=True,is_staff=False,date_joined=date_joined,email=mail,wallet=100)
    c.save()
    return JsonResponse({'ret':0,'msg':'注册成功'})


def signout(request):
    #logout(request)
    user=authen(request)
    if user is None:
        return JsonResponse({'error':'用户已退出登录'})
    user.last_login=str(datetime.now())
    user.is_active=False
    user.jwt_version=None
    user.save()
    return JsonResponse({'ret':0,'msg':f'用户{user.username}退出,请弃用token'})

def personal_info(request,i):
    user=authen(request)
    if user is None:
        return JsonResponse({'error':'用户已退出登录'})
    if i!= str(user.id):
        return login_page(request)
    return JsonResponse({
        'id':user.id,
        'username':user.username,
        'phonenumber':user.phonenumber,
        'wallet':user.wallet,
        'email':user.email,
        'first_name':user.first_name,
        'last_name':user.last_name
    })



def order(request):
    user = authen(request)
    if user is None:
        return JsonResponse({'error': '用户已退出登录'})
    user_id = request.POST.get('user_id')
    pro = loads(request.POST.get('pro'))
    #print(pro)
    p_str = ""
    id_str=""
    price=0
    #time=str(datetime.now())
    for p in pro:
        print(p," ")
        price+=int(Product.objects.filter(name=p['pro_name']).first().price)*int(p['num'])
        sli=str(p)
        i=0
        while i<len(sli):
            if sli[i]=='￥':
                price+=int(sli[i+1])*int(p['num'])
            i+=1
        p_str+=p['pro_name']+" "
        oth=p['0糖0卡']+" "+p['绿色喜茶']+" "+p['状态']+" "+p['冰量']+" "+p['冰球']+" "+p['冰球分装']+" "+p['甜度']+" "+p['加料']+" "+p['做法']+" "+p['柠檬片']+" "+p['柠檬片分装']+" "+p['分装']+" "+p['茶底']+" "+p['口味']+" "+p['特调糖烤菠萝片']+" "+p['菠萝片分装']+" "+p['顶料分装']+" "+p['椰奶冻']
        tea=Classify(num=p['num'],oth=oth)
        tea.save()
        id_str+=str(tea.id)+" "
    address = request.POST.get('address')
    peo = request.POST.get('peo')
    phonenumber = request.POST.get('phonenumber')
    o = Order(peo=peo,address=address,phonenumber=phonenumber,user_id=user_id,pro=p_str,conf=id_str,price=price)
    o.save()
    return JsonResponse({
        'ret':0,
        'msg':'下单成功',
        'pr':price,
        'order_id':o.id
    })


#计算时间差
def cal_difftime(date1, date2):
    print(date1,date2)
    date3=datetime.strptime(date1,"%Y-%m-%d %H:%M:%S.%f")  # 字符串转换为datetime类型
    date4=datetime.strptime(date2,"%Y-%m-%d %H:%M:%S.%f")  # 字符串转换为datetime类型
    times = str(date4 - date3).split(':')
    return int(times[1])


def pay(request):
    user = authen(request)
    if user is None:
        return JsonResponse({'error': '用户已退出登录'})
    order_id = request.POST.get('order_id')
    o=Order.objects.filter(id=order_id).first()
    if user.wallet >= o.price:
        user.wallet-=o.price
    else:
        return JsonResponse({
            'msg':'余额不足'
        })
    user.save()
    po=PayedOrder(pro=o.pro,conf=o.conf,address=o.address,phonenumber=o.phonenumber,peo=o.peo,user_id=o.user_id,price=o.price)
    if len(PayedOrder.objects.filter(start=1))==0:
        time = str(datetime.now())
        po.time_joined=time
        po.start=1
        po.save()
    return JsonResponse({
        'msg':'支付成功',
    })



def topup(request,i):
    user = authen(request)
    #print(user.id)
    if i!= str(user.id):
        return JsonResponse({'error':'用户id错误'})
    if user is None:
        return JsonResponse({'error': '用户已退出登录'})
    num = request.POST.get('num')
    user.wallet+=int(num)
    user.save()
    return JsonResponse({
        'msg':'用户充值成功',
        'wallet':user.wallet
    })



def make(request):
    p = PayedOrder.objects.filter(start=1).first()
    if p is None:
        return  JsonResponse({"msg":"无正在制作的订单"})
    if cal_difftime(p.time_joined,str(datetime.now()))>=1:
        h = HisOrder(pro=p.pro,conf=p.conf,address=p.address,phonenumber=p.phonenumber,peo=p.peo,user_id=p.user_id,price=p.price)
        next_order = PayedOrder.objects.filter(id=p.id+1).first()
        if next_order is not None:
            next_order.start=1
            next_order.time_joined=str(datetime.now())
            next_order.save()
        h.save()
        p.delete()
    return JsonResponse({"msg":"一个订单完成了"})


def query_order(request):
    user = authen(request)
    if user is None:
        return JsonResponse({'error': '用户已退出登录'})
    orders = PayedOrder.objects.filter(user_id=user.id)
    objlist=[]
    for o in orders:
        li=list()
        num = list()
        for i in o.conf.split():
            c = Classify.objects.filter(id=int(i)).first()
            des=c.oth
            li.append(des)
            num.append(c.num)
        obj = {
            "pro":o.pro.split(),
            "address":o.address,
            "peo":o.peo,
            "phonenumber":o.phonenumber,
            "price":o.price,
            "conf":li,
            "num":num,
            "time":o.time_joined,
        }
        objlist.append(obj)
    dic = {
        "inf":objlist
    }
    return JsonResponse(dic)



def query_hisorder(request):
    user = authen(request)
    if user is None:
        return JsonResponse({'error': '用户已退出登录'})
    orders = HisOrder.objects.filter(user_id=user.id)
    objlist = []
    for o in orders:
        li=list()
        num = list()
        for i in o.conf.split():
            c = Classify.objects.filter(id=int(i)).first()
            des=c.oth
            li.append(des)
            num.append(c.num)
        obj = {
            "pro":o.pro.split(),
            "address":o.address,
            "peo":o.peo,
            "phonenumber":o.phonenumber,
            "price":o.price,
            "conf":li,
            "num":num,
            "time":o.time_joined
        }
        objlist.append(obj)
    dic = {
        "inf":objlist
    }
    return JsonResponse(dic)