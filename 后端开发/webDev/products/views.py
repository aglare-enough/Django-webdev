from django.shortcuts import render
from products.models import Product
from django.http import JsonResponse
# Create your views here.
def product_info(request):
    result=list()
    lanmus = ["当季限定","人气必喝榜","每日鲜食","瓶装饮品","喜茶制冰","果茶家族","暴柠家族","茗茶/牛乳茶","波波家族","热饮推荐","纯茶","加料","周边/茶叶"]
    for lanmu in lanmus:
        products = list()
        teas=Product.objects.filter(lanmu=lanmu)
        for pro in teas:
            obj = {
                'id':pro.id,
                'name':pro.name,
                'des':pro.description,
                'price':pro.price,
                'active':pro.active,
                '0糖0卡':pro.noneSugar,
                '绿色喜茶':pro.green.split() if pro.green is not None else pro.green,
                '状态':pro.state.split() if pro.state is not None else pro.state,
                '冰量':pro.ice_num.split() if pro.ice_num is not None else pro.ice_num,
                '冰球':pro.ice_ball.split() if pro.ice_ball is not None else pro.ice_ball,
                '冰球分装':pro.fen_ice.split() if pro.fen_ice is not None else pro.fen_ice,
                '甜度':pro.sweetness.split() if pro.sweetness is not None else pro.sweetness,
                '加料':pro.ingredient.split() if pro.ingredient is not None else pro.ingredient,
                '做法':pro.makeway.split() if pro.makeway is not None else pro.makeway,
                '柠檬片':pro.lemon.split() if pro.lemon is not None else pro.lemon,
                '柠檬片分装':pro.lemon_fen.split() if pro.lemon_fen is not None else pro.lemon_fen,
                '分装':pro.fen.split() if pro.fen is not None else pro.fen,
                '茶底':pro.tea_dreg.split() if pro.tea_dreg is not None else pro.tea_dreg,
                '口味':pro.taste.split() if pro.taste is not None else pro.taste,
                '特调糖烤菠萝片':pro.pineapple.split() if pro.pineapple is not None else pro.pineapple,
                '菠萝片分装':pro.pine_fen.split() if pro.pine_fen is not None else pro.pine_fen,
                '顶料分装':pro.fen.split() if pro.fen is not None else pro.fen,
                '椰奶冻':pro.yenai.split() if pro.yenai is not None else pro.yenai,
            }
            products.append(obj)
        x={
            lanmu:products
        }
        result.append(x)
    re={
        "data":result
    }
    return JsonResponse(re)