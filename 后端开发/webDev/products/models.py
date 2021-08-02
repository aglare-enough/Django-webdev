from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)             #商品描述
    price = models.IntegerField()                              #商品价格
    ingredient = models.CharField(max_length=50,null=True)               #加料
    active = models.IntegerField(default='1')
    noneSugar = models.CharField(max_length=50,null=True)                 #0糖0卡
    green = models.CharField(max_length=50,null=True)                     #绿色喜茶
    state = models.CharField(max_length=50,null=True)                     #状态
    ice_num = models.CharField(max_length=50,null=True)                   #冰量
    ice_ball = models.CharField(max_length=50,null=True)                  #冰球
    fen_ice = models.CharField(max_length=20,null=True)                   #冰球分装
    sweetness = models.CharField(max_length=40,null=True)                 #甜度
    lemon = models.CharField(max_length=40,null=True)                     #柠檬片
    lemon_fen = models.CharField(max_length=40,null=True)                 #柠檬片分装
    tea_dreg = models.CharField(max_length=40,null=True)                  #茶底
    makeway = models.CharField(max_length=40,null=True)                   #做法
    taste = models.CharField(max_length=40,null=True)                     #口味
    pineapple = models.CharField(max_length=40,null=True)                 #特调糖烤菠萝片
    pine_fen = models.CharField(max_length=40,null=True)                  #菠萝片分装
    fen = models.CharField(max_length=40,null=True)                       #顶料分装
    yenai = models.CharField(max_length=40,null=True)                     #椰奶冻
    lanmu = models.CharField(max_length=40,null=True)


class Classify(models.Model):
    oth = models.CharField(max_length=255)
    num = models.IntegerField(default=1)