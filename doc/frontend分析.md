[TOC]

##1. 路由

frontend在main.go中提供了以下路由，每条路由都有对应的log，具体可参见“service日志分析.md”。

```javascript
//以下六条在locust中被执行	
	r.HandleFunc("/", svc.homeHandler).Methods(http.MethodGet, http.MethodHead)
	r.HandleFunc("/product/{id}", svc.productHandler).Methods(http.MethodGet, http.MethodHead)
	r.HandleFunc("/cart", svc.viewCartHandler).Methods(http.MethodGet, http.MethodHead)
	r.HandleFunc("/cart", svc.addToCartHandler).Methods(http.MethodPost)
	r.HandleFunc("/setCurrency", svc.setCurrencyHandler).Methods(http.MethodPost)
	r.HandleFunc("/cart/checkout", svc.placeOrderHandler).Methods(http.MethodPost)
//以下两条在locust中没有被执行
	r.HandleFunc("/cart/empty", svc.emptyCartHandler).Methods(http.MethodPost)
	r.HandleFunc("/logout", svc.logoutHandler).Methods(http.MethodGet)
//以下三条在流量模拟中没什么用
	r.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir("./static/"))))
	r.HandleFunc("/robots.txt", func(w http.ResponseWriter, _ *http.Request) { fmt.Fprint(w, "User-agent: *\nDisallow: /") })
	r.HandleFunc("/_healthz", func(w http.ResponseWriter, _ *http.Request) { fmt.Fprint(w, "ok") })
```


## 2. handler (与路由一一对应)

### 2.1 homeHandler("/", get)

service日志包括"currency"以及"session"参数，参数完整。

```javascript
// pb.NewCurrencyServiceClient(fe.currencySvcConn).GetSupportedCurrencies(ctx, &pb.Empty{})
fe.getCurrencies(r.Context()) 
// pb.NewProductCatalogServiceClient(fe.productCatalogSvcConn).ListProducts(ctx, &pb.Empty{})
fe.getProducts(r.Context()) 
//  pb.NewCartServiceClient(fe.cartSvcConn).GetCart(ctx, &pb.GetCartRequest{UserId: userID})
fe.getCart(r.Context(), sessionID(r)) 
// pb.NewCurrencyServiceClient(fe.currencySvcConn).Convert(ctx, &pb.CurrencyConversionRequest{
//			From:   money,
//			ToCode: currency
//  })
fe.convertCurrency(r.Context(), p.GetPriceUsd(), currentCurrency(r)) // 多次调用；p 来自于fe.getProducts(r.Context())
// pb.NewAdServiceClient(fe.adSvcConn).GetAds(ctx, &pb.AdRequest{ContextKeys: ctxKeys,})
fe.chooseAd(r.Context(), []string{}, log) // 调用fe.getAd(ctx, ctxKeys)；第二个参数为空，即此处context_keys为空 
```

### 2.2 productHandler("/product/{id}", get)

service日志包括"currency"、"session"、"id"（商品id），参数完整

```javascript
// pb.NewProductCatalogServiceClient(fe.productCatalogSvcConn).GetProduct(ctx, &pb.GetProductRequest{Id: id})
fe.getProduct(r.Context(), id) // 返回结果为变量p
fe.getCurrencies(r.Context()) 
fe.getCart(r.Context(), sessionID(r))
fe.convertCurrency(r.Context(), p.GetPriceUsd(), currentCurrency(r))
//pb.NewRecommendationServiceClient(fe.recommendationSvcConn).ListRecommendations(ctx, &pb.ListRecommendationsRequest{UserId: userID, ProductIds: productIDs})
fe.getRecommendations(r.Context(), sessionID(r), []string{id}) 
fe.chooseAd(r.Context(), p.Categories, log) 
```

### 2.3 addToCartHandler("/cart", post)

service日志包括"session"、"product"（商品id）、"quantity"，参数完整

```javascript
fe.getProduct(r.Context(), productID) 
// pb.NewCartServiceClient(fe.cartSvcConn).AddItem(ctx, &pb.AddItemRequest{
//		UserId: userID,
//		Item: &pb.CartItem{
//			ProductId: productID,
//			Quantity:  quantity},})
fe.insertCart(r.Context(), sessionID(r), p.GetId(), int32(quantity)) 
w.Header().Set("location", "/cart") // viewCartHandler?
```

### 2.4 emptyCartHandler("/cart/empty", post)

理论上会产生log.Debug("emptying cart")日志，但是locust没有模拟该用户行为。

```javascript
// pb.NewCartServiceClient(fe.cartSvcConn).EmptyCart(ctx, &pb.EmptyCartRequest{UserId: userID})
fe.emptyCart(r.Context(), sessionID(r)) 
w.Header().Set("location", "/") // homeHandler?
```

### 2.5 viewCartHandler("/cart", get)

service日志包括"session"，参数完整。

```javascript
fe.getCurrencies(r.Context())
fe.getCart(r.Context(), sessionID(r))
fe.getRecommendations(r.Context(), sessionID(r), cartIDs(cart)) //cartIDs 返回cart中的商品id
// pb.NewShippingServiceClient(fe.shippingSvcConn).GetQuote(ctx,
//		&pb.GetQuoteRequest{
//			Address: nil,
//			Items:   items})
fe.getShippingQuote(r.Context(), cart, currentCurrency(r)) 
fe.getProduct(r.Context(), item.GetProductId()) // 多次调用
fe.convertCurrency(r.Context(), p.GetPriceUsd(), currentCurrency(r)) // 多次调用
```

### 2.6 placeOrderHandler("/cart/checkout", post)

service日志包括"session"，参数**不完整**。日志还应该包括PlaceOrderRequest参数作为表单数据。这部分数据写死在frontend的代码里，可以直接从代码中获得，但是不可以从日志中获得。

```json
// pb.NewCheckoutServiceClient(fe.checkoutSvcConn).
//		PlaceOrder(r.Context(), &pb.PlaceOrderRequest{
//			Email: email,
//			CreditCard: &pb.CreditCardInfo{
//				CreditCardNumber:          ccNumber,
//				CreditCardExpirationMonth: int32(ccMonth),
//				CreditCardExpirationYear:  int32(ccYear),
//				CreditCardCvv:             int32(ccCVV)},
//			UserId:       sessionID(r),
//			UserCurrency: currentCurrency(r),
//			Address: &pb.Address{
//				StreetAddress: streetAddress,
//				City:          city,
//				State:         state,
//				ZipCode:       int32(zipCode),
//				Country:       country},
//		})
// 理论上这里应该有fe.PlaceOrder()，但是前几行的NewCheckoutServiceClient没有封装为fe.PlaceOrder()的形式
fe.getRecommendations(r.Context(), sessionID(r), nil)
fe.getCurrencies(r.Context())
```

### 2.7 logoutHandler("/logout", get)

理论上会产生log.Debug("logging out")日志，但是locust没有模拟该用户行为。

```javascript
w.Header().Set("location", "/") // homeHandler? 
```

### 2.8 setCurrencyHandler("/setCurrency", post)

service日志包括"session"、"curr.new"、"curr.old"，参数完整。

```javascript
// "curr.new"被写入cookie，该过程不需要调用service的rpc接口。
// 该handler的最后一步是重定向，该过程将根据具体的handler调用相关接口
referer := r.Header.Get("referer")
if referer == "" {
  referer = "/"
}
w.Header().Set("Location", referer) // homeHandler or the last handler?
```

### 其他注意事项

* **frontend存在的顺序调用关系**（目前只发现这一个特殊的调用）：fe.getRecommendations()会在frontend中先调用ListRecommendations，再调用fe.getProduct(ctx, v)，所以在trace日志中,如果存在"Frontend/Recv."->"ListRecommendations"，将同时存在"Frontend/Recv."->"GetProduct"。参见源代码src/frontend/rpc.go以及"trace日志分析.md"中的placeOrderHandler部分。

* **service内部存在的相互调用关系：**例如，placeOrderHandler调用PlaceOrder()，PlaceOrder()在checkoutservice内部调用cartservice的EmptyCart()。参见源代码src/checkoutservice/main.go。

