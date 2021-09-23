[TOC]

## 1. Locust中的user behavior相关日志(由frontend生成)

### 1.1 index ("/", get)

```python
def index(l):
    l.client.get("/")
```

```json
//request started
{"http.req.id":"a624545d-2054-4e1f-9bad-5cad25d92cd3","http.req.method":"GET","http.req.path":"/","message":"request started","session":"4836a96f-1e39-4257-8f00-53e97d6286ca","severity":"debug","timestamp":"2021-07-09T10:49:35.219584086Z"}

//home
{"currency":"EUR","http.req.id":"a624545d-2054-4e1f-9bad-5cad25d92cd3","http.req.method":"GET","http.req.path":"/","message":"home","session":"4836a96f-1e39-4257-8f00-53e97d6286ca","severity":"info","timestamp":"2021-07-09T10:49:35.219622897Z"}

//request complete
{"http.req.id":"a624545d-2054-4e1f-9bad-5cad25d92cd3","http.req.method":"GET","http.req.path":"/","http.resp.bytes":10685,"http.resp.status":200,"http.resp.took_ms":46,"message":"request complete","session":"4836a96f-1e39-4257-8f00-53e97d6286ca","severity":"debug","timestamp":"2021-07-09T10:49:35.265781967Z"}

```

### 1.2 setCurrency ("/setCurrency", post)

```python
def setCurrency(l):
    currencies = ['EUR', 'USD', 'JPY', 'CAD']
    l.client.post("/setCurrency",
        {'currency_code': random.choice(currencies)})
```

```json
//request started
{"http.req.id":"e49e4e8b-b09f-4290-a7ac-1aa70abb587c","http.req.method":"POST","http.req.path":"/setCurrency","message":"request started","session":"42c50e10-8772-43d2-915f-20d1a466aa08","severity":"debug","timestamp":"2021-07-09T10:49:24.469963292Z"}

//setting currency
{"curr.new":"EUR","curr.old":"JPY","http.req.id":"e49e4e8b-b09f-4290-a7ac-1aa70abb587c","http.req.method":"POST","http.req.path":"/setCurrency","message":"setting currency","session":"42c50e10-8772-43d2-915f-20d1a466aa08","severity":"debug","timestamp":"2021-07-09T10:49:24.470098453Z"}

//request complete
{"http.req.id":"e49e4e8b-b09f-4290-a7ac-1aa70abb587c","http.req.method":"POST","http.req.path":"/setCurrency","http.resp.bytes":0,"http.resp.status":302,"http.resp.took_ms":0,"message":"request complete","session":"42c50e10-8772-43d2-915f-20d1a466aa08","severity":"debug","timestamp":"2021-07-09T10:49:24.47014419Z"}

```

### 1.3 browseProduct ("/product/{id}", get)

```python
def browseProduct(l):
    l.client.get("/product/" + random.choice(products))
```

```json
//request started
{"http.req.id":"9a1905d4-7e6b-448d-876e-9de921862cce","http.req.method":"GET","http.req.path":"/product/L9ECAV7KIM","message":"request started","session":"ed30349d-f173-4910-ab7a-4fbd9e223ef4","severity":"debug","timestamp":"2021-07-09T10:37:20.272817343Z"}

//serving product page
{"currency":"JPY","http.req.id":"9a1905d4-7e6b-448d-876e-9de921862cce","http.req.method":"GET","http.req.path":"/product/L9ECAV7KIM","id":"L9ECAV7KIM","message":"serving product page","session":"ed30349d-f173-4910-ab7a-4fbd9e223ef4","severity":"debug","timestamp":"2021-07-09T10:37:20.273208093Z"}

//request complete
{"http.req.id":"9a1905d4-7e6b-448d-876e-9de921862cce","http.req.method":"GET","http.req.path":"/product/L9ECAV7KIM","http.resp.bytes":7998,"http.resp.status":200,"http.resp.took_ms":39,"message":"request complete","session":"ed30349d-f173-4910-ab7a-4fbd9e223ef4","severity":"debug","timestamp":"2021-07-09T10:37:20.312397447Z"}

```

### 1.4 viewCart ("/cart", get)

```python
def viewCart(l):
    l.client.get("/cart")
```

```json
// request started
{"http.req.id":"ba65736f-4f30-4b4c-b81d-66bb50bae586","http.req.method":"GET","http.req.path":"/cart","message":"request started","session":"92d951e2-e7e1-4d15-b614-27c701039b15","severity":"debug","timestamp":"2021-07-09T10:49:10.55029747Z"}

// view user cart
{"http.req.id":"ba65736f-4f30-4b4c-b81d-66bb50bae586","http.req.method":"GET","http.req.path":"/cart","message":"view user cart","session":"92d951e2-e7e1-4d15-b614-27c701039b15","severity":"debug","timestamp":"2021-07-09T10:49:10.550368128Z"}

// request complete
{"http.req.id":"ba65736f-4f30-4b4c-b81d-66bb50bae586","http.req.method":"GET","http.req.path":"/cart","http.resp.bytes":16402,"http.resp.status":200,"http.resp.took_ms":48,"message":"request complete","session":"92d951e2-e7e1-4d15-b614-27c701039b15","severity":"debug","timestamp":"2021-07-09T10:49:10.598350998Z"}
```

### 1.5 addToCart (...; "/cart", post)

```python
def addToCart(l):
    product = random.choice(products)
    l.client.get("/product/" + product)
    l.client.post("/cart", {
        'product_id': product,
        'quantity': random.choice([1,2,3,4,5,10])})
```

```json
// l.client.get("/product/" + product)对应的日志参见1.3

// request started
{"http.req.id":"672e85d2-42ca-4098-a63c-2eac6547fbff","http.req.method":"POST","http.req.path":"/cart","message":"request started","session":"8874231e-29f7-4311-b810-e64849961c3b","severity":"debug","timestamp":"2021-07-09T10:49:20.985270493Z"}

// adding to cart
{"http.req.id":"672e85d2-42ca-4098-a63c-2eac6547fbff","http.req.method":"POST","http.req.path":"/cart","message":"adding to cart","product":"1YMWWN1N4O","quantity":2,"session":"8874231e-29f7-4311-b810-e64849961c3b","severity":"debug","timestamp":"2021-07-09T10:49:20.985361608Z"}

// request complete
{"http.req.id":"87212dc9-56d6-4bad-81c5-c29955bb20f3","http.req.method":"POST","http.req.path":"/cart","http.resp.bytes":0,"http.resp.status":302,"http.resp.took_ms":8,"message":"request complete","session":"6b95accf-a270-446b-b9ad-b47c2524e719","severity":"debug","timestamp":"2021-07-09T10:49:21.273213201Z"}
```

### 1.6 checkout (...; "/cart/checkout", post)

```python
def checkout(l):
    addToCart(l)
    l.client.post("/cart/checkout", {
        'email': 'someone@example.com',
        'street_address': '1600 Amphitheatre Parkway',
        'zip_code': '94043',
        'city': 'Mountain View',
        'state': 'CA',
        'country': 'United States',
        'credit_card_number': '4432-8015-6152-0454',
        'credit_card_expiration_month': '1',
        'credit_card_expiration_year': '2039',
        'credit_card_cvv': '672',
    })
```

```json
// addToCart(l)对应的日志参见1.5

//request started
{"http.req.id":"3b4fcf39-a596-49c5-a8a9-b9dbd63259c4","http.req.method":"POST","http.req.path":"/cart/checkout","message":"request started","session":"592e34b8-5ede-4b45-aa8f-de1681a459ba","severity":"debug","timestamp":"2021-07-09T10:50:07.076583405Z"}

//placing order
{"http.req.id":"3b4fcf39-a596-49c5-a8a9-b9dbd63259c4","http.req.method":"POST","http.req.path":"/cart/checkout","message":"placing order","session":"592e34b8-5ede-4b45-aa8f-de1681a459ba","severity":"debug","timestamp":"2021-07-09T10:50:07.076650515Z"}

//order placed
{"http.req.id":"3b4fcf39-a596-49c5-a8a9-b9dbd63259c4","http.req.method":"POST","http.req.path":"/cart/checkout","message":"order placed","order":"6c92d2c7-e0a3-11eb-979d-8249c9057ce3","session":"592e34b8-5ede-4b45-aa8f-de1681a459ba","severity":"info","timestamp":"2021-07-09T10:50:07.204529253Z"}

//request complete
{"http.req.id":"3b4fcf39-a596-49c5-a8a9-b9dbd63259c4","http.req.method":"POST","http.req.path":"/cart/checkout","http.resp.bytes":6376,"http.resp.status":200,"http.resp.took_ms":151,"message":"request complete","session":"592e34b8-5ede-4b45-aa8f-de1681a459ba","severity":"debug","timestamp":"2021-07-09T10:50:07.228080949Z"}
```


## 2. histershop中的service相关日志(由各service生成)

### 2.1 ad service

```json
// context_words=[photography, vintage]
{"logEvent":"received ad request (context_words=[photography, vintage])","time":"2021-07-09T10:49:53.246Z"}

// context_words=[]
{"logEvent":"received ad request (context_words=[])","time":"2021-07-09T10:49:53.164Z"}
```

### 2.2 cart service

```json
GetCartAsync called with userId=ab5c716e-f00a-4174-a6e1-0c58336eec8f
      Request starting HTTP/2 POST http://cartservice-2:7070/hipstershop.CartService/GetCart application/grpc 
      Executing endpoint 'gRPC - /hipstershop.CartService/GetCart'
      Executed endpoint 'gRPC - /hipstershop.CartService/GetCart'
      Request finished in 1.2207ms 200 application/grpc

EmptyCartAsync called with userId=ab5c716e-f00a-4174-a6e1-0c58336eec8f
      Request starting HTTP/2 POST http://cartservice:7070/hipstershop.CartService/EmptyCart application/grpc 
      Executing endpoint 'gRPC - /hipstershop.CartService/EmptyCart'
      Executed endpoint 'gRPC - /hipstershop.CartService/EmptyCart'
      Request finished in 1.4518ms 200 application/grpc

AddItemAsync called with userId=8874231e-29f7-4311-b810-e64849961c3b, productId=0PUK6V6EV0, quantity=10
      Request starting HTTP/2 POST http://cartservice:7070/hipstershop.CartService/AddItem application/grpc
      Executing endpoint 'gRPC - /hipstershop.CartService/AddItem'
      Executed endpoint 'gRPC - /hipstershop.CartService/AddItem'
      Request finished in 0.8163ms 200 application/grpc

 [40m[32minfo[39m[22m[49m: Microsoft.AspNetCore.Routing.EndpointMiddleware[0]
 [40m[32minfo[39m[22m[49m: Microsoft.AspNetCore.Routing.EndpointMiddleware[1]
 [40m[32minfo[39m[22m[49m: Microsoft.AspNetCore.Hosting.Diagnostics[1]
 [40m[32minfo[39m[22m[49m: Microsoft.AspNetCore.Hosting.Diagnostics[2]
```


### 2.3 checkout service

```json
// [PlaceOrder] user_id="63c65184-4326-411d-bdca-0134dfb346e7" user_currency="USD"
{"message":"[PlaceOrder] user_id=\"63c65184-4326-411d-bdca-0134dfb346e7\" user_currency=\"USD\"","severity":"info","timestamp":"2021-07-09T10:18:30.950076717Z"}

// order confirmation email sent to "someone@example.com
{"message":"order confirmation email sent to \"someone@example.com\"","severity":"info","timestamp":"2021-07-09T10:18:33.915076569Z"}
```

### 2.4 currency service

```json
// received conversion request
{"severity":"info","time":1625825913633,"message":"received conversion request","pid":1,"hostname":"currencyservice-2-67648fdbc9-mbdhf","name":"currencyservice-server","v":1}

// conversion request successful
{"severity":"info","time":1625825913626,"message":"conversion request successful","pid":1,"hostname":"currencyservice-2-67648fdbc9-mbdhf","name":"currencyservice-server","v":1}

// Getting supported currencies...
{"severity":"info","time":1625825913657,"message":"Getting supported currencies...","pid":1,"hostname":"currencyservice-2-67648fdbc9-mbdhf","name":"currencyservice-server","v":1}

```

### 2.5 email service

```json
// A request to send order confirmation email to someone@example.com has been received.
{"timestamp": 1625826903.9210935, "severity": "INFO", "name": "emailservice-server", "message": "A request to send order confirmation email to someone@example.com has been received."}
```


### 2.6 payment service

```json
// PaymentService#Charge invoked with request {"amount":{"currency_code":"EUR","units":"50","nanos":897832817},"credit_card":{"credit_card_number":"4432-8015-6152-0454","credit_card_cvv":672,"credit_card_expiration_year":2039,"credit_card_expiration_month":1}}
{"severity":"info","time":1625825913216,"message":"PaymentService#Charge invoked with request {\"amount\":{\"currency_code\":\"EUR\",\"units\":\"50\",\"nanos\":897832817},\"credit_card\":{\"credit_card_number\":\"4432-8015-6152-0454\",\"credit_card_cvv\":672,\"credit_card_expiration_year\":2039,\"credit_card_expiration_month\":1}}","pid":1,"hostname":"paymentservice-2-5cfb69ddf6-dq7nv","name":"paymentservice-server","v":1}

// Transaction processed: visa ending 0454     Amount: EUR50.897832817
{"severity":"info","time":1625825913216,"message":"Transaction processed: visa ending 0454     Amount: EUR50.897832817","pid":1,"hostname":"paymentservice-2-5cfb69ddf6-dq7nv","name":"paymentservice-charge","v":1}

// payment went through (transaction_id: eaa1857f-ca7f-416a-bb74-95a168963a96)
{"message":"payment went through (transaction_id: eaa1857f-ca7f-416a-bb74-95a168963a96)","severity":"info","timestamp":"2021-07-09T10:22:35.308320358Z"}

```
### 2.7 product service

```json
//没有找到product相关的日志
```

### 2.8 recommendation service

```json
// [Recv ListRecommendations] product_ids=['L9ECAV7KIM', '0PUK6V6EV0', 'LS4PSXUNUM', '66VCHSJNUP', '2ZYFJ3GM2N']
{"timestamp": 1625826905.73139, "severity": "INFO", "name": "recommendationservice-server", "message": "[Recv ListRecommendations] product_ids=['L9ECAV7KIM', '0PUK6V6EV0', 'LS4PSXUNUM', '66VCHSJNUP', '2ZYFJ3GM2N']"}
```

### 2.9 shipping service

```json
// [GetQuote] received request
{"message":"[GetQuote] received request","severity":"info","timestamp":"2021-07-09T10:18:32.736979791Z"}

// [GetQuote] completed request
{"message":"[GetQuote] completed request","severity":"info","timestamp":"2021-07-09T10:18:32.737020755Z"}

// [ShipOrder] received request
{"message":"[ShipOrder] received request","severity":"info","timestamp":"2021-07-09T10:22:35.311407609Z"}

// [ShipOrder] completed request
{"message":"[ShipOrder] completed request","severity":"info","timestamp":"2021-07-09T10:22:35.311451535Z"}
```


## 3. session示例

```json
// 76eece30-664d-4a1a-a926-8c63cc581d2e
// 用户在frontend执行了adding to cart与view user cart两部分操作。根据frontend分析.md，这两个操作对应一系列的接口调用。由于并非service的日志都记录了session信息，故各service的日志不能完全捕获

// request started
{"http.req.id":"b5eff7a2-9971-483e-8e6d-2520a15161eb","http.req.method":"POST","http.req.path":"/cart","message":"request started","session":"76eece30-664d-4a1a-a926-8c63cc581d2e","severity":"debug","timestamp":"2021-07-09T10:35:04.908969258Z"}

// adding to cart
{"http.req.id":"b5eff7a2-9971-483e-8e6d-2520a15161eb","http.req.method":"POST","http.req.path":"/cart","message":"adding to cart","product":"OLJCESPC7Z","quantity":3,"session":"76eece30-664d-4a1a-a926-8c63cc581d2e","severity":"debug","timestamp":"2021-07-09T10:35:04.909035272Z"}

// request complete
{"http.req.id":"b5eff7a2-9971-483e-8e6d-2520a15161eb","http.req.method":"POST","http.req.path":"/cart","http.resp.bytes":0,"http.resp.status":302,"http.resp.took_ms":8,"message":"request complete","session":"76eece30-664d-4a1a-a926-8c63cc581d2e","severity":"debug","timestamp":"2021-07-09T10:35:04.91703Z"}

// request started
{"http.req.id":"c99c82b0-bd21-40f1-9d59-9f42b6523906","http.req.method":"GET","http.req.path":"/cart","message":"request started","session":"76eece30-664d-4a1a-a926-8c63cc581d2e","severity":"debug","timestamp":"2021-07-09T10:35:04.918270572Z"}

// request complete
{"http.req.id":"c99c82b0-bd21-40f1-9d59-9f42b6523906","http.req.method":"GET","http.req.path":"/cart","http.resp.bytes":16398,"http.resp.status":200,"http.resp.took_ms":37,"message":"request complete","session":"76eece30-664d-4a1a-a926-8c63cc581d2e","severity":"debug","timestamp":"2021-07-09T10:35:04.955502458Z"}

// 此处省略了一部分2.2中的日志
AddItemAsync called with userId=76eece30-664d-4a1a-a926-8c63cc581d2e, productId=OLJCESPC7Z, quantity=3

GetCartAsync called with userId=76eece30-664d-4a1a-a926-8c63cc581d2e

// view user cart
{"http.req.id":"c2f87090-384a-4a67-9576-972da07503bb","http.req.method":"GET","http.req.path":"/cart","message":"view user cart","session":"76eece30-664d-4a1a-a926-8c63cc581d2e","severity":"debug","timestamp":"2021-07-09T10:35:08.957130106Z"}

GetCartAsync called with userId=76eece30-664d-4a1a-a926-8c63cc581d2e
```

## 4. 其他

* session 与 userId 一一对应。
* 包含session的日志都是"http.req.method"的形式，也都是Locust中的user behavior相关日志
* 包含session的日志一共有2305676条（frontend-log collection）
* 不同的用户session一共有30436个（session collection）