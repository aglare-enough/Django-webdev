## 喜茶GO系统API接口

> ### 注册
>
> url : "customers/register"
>
> 前端通过http post 请求在请求体中将注册账户信息发给后端
>
> ```json
> //请求体格式
> {
>     "username":"" ,	//必填
>     "password":"" ,	//必填
>     "phonenumber":"",
>     "email":"",
> }
> ```
>
> ```json
> //后端返回
> //注册成功
> {
>     "ret":0,  //返回0代表注册成功，无异常
>     "msg":"注册成功"
> }
> //电话号码已被注册
> {
>     "ret":1,
>     "msg":"电话号码已被注册"
> }
> //用户名已存在
> {
>     "ret":1,
>     "msg":"用户名已存在"
> }
> ```
>
> ### 登录
>
> url: "customers/login"
>
> 前端通过http post 请求将登录信息通过请求体发送给后端进行验证
>
> ```json
> //请求体数据格式
> {
>     "username":"",
>     "password":"",
> }
> //后端返回
> {
>     "ret":0,
>     "token":"",
>     "version":"",  //token版本
>     "user_id":""
> }
> //后端将返回token,token版本，user_id,前端在进行后续用户登陆后的操作时都需要将token以及token_version传给后端进行验证
> 
> ```
>
>
> <h3 id="token">Token</h3>
>
> 前端在像后端传token进行验证时需将，token放在请求头的Authorization中   <a href="https://blog.csdn.net/h5_since/article/details/108092294?utm_term=vue%E6%B7%BB%E5%8A%A0Authorization&utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduweb~default-2-108092294&spm=3001.4430">参考</a>
>
> authorization的格式是```Bearer jwt ${token_version} ${token}``` 必须得这样<^-^>
>
> <u>以下提到的所有传token都是这种格式</u>
>
> ### 登出
>
> url : "customers/${user_id}/logout/"
>
> 无需其他信息，只需传入token
>
> 返回数据如下：
>
> ```json
> {"ret":0,"msg":"用户${user.username}退出,请弃用token"}
> ```
>
> ### 获取个人信息
>
> url : "customers/${user_id}/info/" get请求 传入token即可，无需其他参数
>
> ```json
> {
>         "id":user.id,
>         "username":user.username,
>         "phonenumber":user.phonenumber,
>         "wallet":user.wallet,
>         "email":user.email,
>         "first_name":user.first_name,
>         "last_name":user.last_name
>    }
> ```
>
> 
>
> ### 获取商品信息
>
> url: "products/info/"
>
> http get请求，无需任何参数
>
> 后端返回数据格式如下：
>
> 由于数据有点多，不在这里写了，在response.json文件中，将其中的中文unicode码复制到<a href="https://www.bejson.com/jsonviewernew/">json在线解析工具</a>可以清楚的看到结构
>
> ### 下单API
>
> url: "customers/order"
>
> > ```json
> > // 前端通过http post请求将订单发送给后端，需将token附带在请求头中,订单信息放在请求体中
> > // 请求体数据格式如下：
> > {
> >     user_id:id,
> >     username:name,
> >     
> >     //pro 商品列表存放下单的所有商品
> >     pro:[
> >         //商品1
> >         {
> >             'pro_name':name,
> >             'num':(int),  			//该商品下单的数量
> >             //以下的奶茶附带属性直接传入用选中的值的字符串即可，若没有该状态值则传回空字符串，eg:
> >             '0糖0卡':"原创0糖0卡￥1",
> >             '绿色喜茶':"",
> >             '状态':"",
> >             '冰量':"",
> >             '冰球':"",
> >             '冰球分装':"",
> >             '甜度':"",
> >             '加料':"",
> >             '做法':"",
> >             '柠檬片':"",
> >             '柠檬片分装':"",
> >             '分装':"",
> >             '茶底':"",
> >             '口味':"",
> >             '特调糖烤菠萝片':"",
> >             '菠萝片分装':"",
> >             '顶料分装':"",
> >             '椰奶冻':"",
> >         },{//商品2
> >             
> >         }，……
> >     ],
> >     
> >     //收件地址
> >     'address':"",
> >     
> >     //收件人
> >     'peo':"",
> >     
> >     //电话
> >     'phonenumber':""
> >     
> > }
> > //后端在收到该数据时，会计算该订单价钱并且返回相关订单数据入下
> > {
> >         'ret':0,
> >         'msg':'下单成功',
> >         'pr':price,
> >         'order_id':o.id			//前端需要存储订单id在支付时需要用到
> > }
> > ```
>
> ### 支付
>
> url : "customers/order/pay"
>
> 前端通过http post请求在请求体中附带order_id,以及在请求头中附带token(具体方式<a href="#token">如上</a>)
>
> ```json
> //数据格式
> {
>     "order_id":""
> }
> //余额不足则返回
> {
>     "msg":"余额不足"
> }
> //成功则返回
> {
>     "msg":"支付成功"
> }
> ```
>
> ### 充值
>
> url :"cutomers/${user_id}/topup"(其中user_id时要充值的用户的user_id)
>
> 前端通过http post请求，同样需要传入token
>
> ```json
> //请求体数据格式
> {
>     "num":（int）   //充值钱数，由于是虚拟的所以没有调用其他支付接口，请求就直接充值
> }
> ```
>
> ### 查询当前用户订单
>
> url : "cutomers/order/query_order"
>
> http get请求 在请求头中附带token即可无需其他参数
>
> ```json
> //返回
> {
>     "inf": [ //inf字段对应该用户的订单列表
>        //订单1 
>         {
>             //商品名列表
>             "pro": [
>                 "浓暴柠"，"嫩暴柠"
>             ],
>             
>             "address": "sfiuewgufqgiwieq",
>             "peo": "hahaha",
>             "phonenumber": "13297128110",
>             "price": 44,
>             //此处列表对应商品名列表，商品列表中的商品的各个特征依次为下列列表中的值
>             //例如商品列表中的第一个"浓暴柠"对应conf列表的第一个"原创0糖0卡￥1 dsajgf eygf sidew iuewi dueywi saifygie saufhi fnoqewuh sadfiu3e sdfyg3ew       fwqefe"
>             //第二个”嫩暴柠“则对应""
>             "conf": [
>                 "原创0糖0卡￥1 dsajgf eygf sidew iuewi dueywi saifygie saufhi fnoqewuh sadfiu3e sdfyg3ew       fwqefe"，""
>                
>             ],
>             "num": [
>                 2，2  //此处列表对应商品名列表，商品列表中的商品数量依次为num列表中的int数
>             ],
>             "time": "2021-08-02 09:20:08.964607"  //订单支付时间
>         }
>     ]
> }
> ```
>
> ### 查询历史订单
>
> url : "customers/order/query_hisorder"
>
> 请求方式同上，但是只需token,无需其他参数，数据返回格式同上
>
> 
>
> ### 订单一分钟后结束    ajax短链接                                  <u>必须</u>
>
> http post请求在请求头中附带token，无需其他参数
>
> url: "customers/order/make"
>
> 前端```每隔一秒钟```向后端该url发送请求是否有订单结束 
>
> http短轮询（short polling）：服务端收到请求后无论是否有数据都立即返回，浏览器收到响应后间隔一段时间后重新发送相同的请求。

