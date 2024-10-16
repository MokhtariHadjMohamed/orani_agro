let orderSituation = document.querySelector('#orderSituation');
let itemProductsOrders = document.querySelectorAll('.itemProductsOrders');
orderSituation.addEventListener("change", () => {
    console.log(orderSituation.value);
    if(orderSituation.value != "في انتظار الشحن")
        itemProductsOrders.forEach(element => {
            element.checked = true
        });
    else
        itemProductsOrders.forEach(element => {
            element.checked = false
        });
})
    

