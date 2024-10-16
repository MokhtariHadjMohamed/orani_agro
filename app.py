import os
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from User import User
from Product import Product
from Order import Order
from Category import Category
from SubCategory import SubCategory
from ProductOrder import ProductOrder
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

cred = credentials.Certificate("firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"storageBucket": "oraniagro.appspot.com"})

db = firestore.client()
app = Flask(__name__)


@app.route("/")
def index():
    dUser = db.collection("Users").stream()
    users = []
    for doc in dUser:
        users.append(User.from_dict(doc.to_dict()))

    dProduct = db.collection("Products").stream()
    products = []
    for doc in dProduct:
        products.append(Product.from_dict(doc.to_dict()))

    dOrder = db.collection("Orders").where(filter=FieldFilter(
        "orderSituation", "==", "في انتظار شحن")).stream()
    orders = []
    for doc in dOrder:
        orders.append(Order.from_dict(doc.to_dict()))

    docs = db.collection("Category").stream()
    category = {}
    for doc in docs:
        d = (Category.from_dict(doc.to_dict())).to_dict()
        category[d["idCategory"]] = d

    return render_template("index.html", users=users, products=products, orders=orders, category=category, zip=zip, len=len)

# main pages


@app.route("/users.html")
def users():
    docs = db.collection("Users").stream()
    users = []
    for doc in docs:
        users.append(User.from_dict(doc.to_dict()))
    return render_template("users.html", users=users, i=1)


@app.route("/products.html")
def products():
    docs = db.collection("Products").stream()
    products = []
    for doc in docs:
        products.append(Product.from_dict(doc.to_dict()))
    return render_template("products.html", products=products)


@app.route("/orders.html")
def orders():
    docs = db.collection("Orders").stream()
    dUser = db.collection("Users")
    orders = []
    users = []

    for doc in docs:
        orders.append(Order.from_dict(doc.to_dict()))

    for o in orders:
        docs_user = dUser.where(filter=FieldFilter(
            "idUser", "==", o.idClient)).stream()
        for doc_user in docs_user:
            users.append(User.from_dict(doc_user.to_dict()))
    return render_template("orders.html", orders=orders, users=users, zip=zip)


@app.route("/category.html")
def category():
    docs = db.collection("Category").stream()
    category = {}
    for doc in docs:
        d = (Category.from_dict(doc.to_dict())).to_dict()
        category[d["idCategory"]] = d

    dSubCategory = db.collection("SubCategory").stream()
    subCategory = []
    for doc in dSubCategory:
        subCategory.append(SubCategory.from_dict(doc.to_dict()))
    return render_template("category.html", category=category, subCategory=subCategory)

# Info pages
@app.route("/ordersInfo.html/<idOrder>")
def ordersInfo(idOrder):
    docs = db.collection("Orders").document(idOrder)
    order = Order.from_dict(docs.get().to_dict())

    dUser = db.collection("Users").document(order.idClient)
    user = User.from_dict(dUser.get().to_dict())

    dDeleveryBoy = db.collection("Users").where(
        filter=FieldFilter("type", "==", "deliveryBoy")).stream()
    deleveryBoy = []
    for doc in dDeleveryBoy:
        deleveryBoy.append(User.from_dict(doc.to_dict()))

    productsOrders = []
    total = 0
    for o in order.productOrders:
        productsOrders.append(ProductOrder.from_dict(o))
        total += ProductOrder.from_dict(o).productPrice

    return render_template("ordersInfo.html", order=order, user=user,
                            productsOrders=productsOrders, deleveryBoy=deleveryBoy, total=total)


@app.route('/usersInfo.html/<idUser>')
def userInfo(idUser):
    dUser = db.collection("Users").document(idUser)
    user = User.from_dict(dUser.get().to_dict())

    docs = db.collection("Category").stream()
    category = []
    for doc in docs:
        category.append(Category.from_dict(doc.to_dict()))

    return render_template("usersInfo.html", user=user, category=category)


@app.route("/productInfo.html/<idProduct>")
def productInfo(idProduct):
    dProduct = db.collection("Products").document(idProduct)
    product = Product.from_dict(dProduct.get().to_dict())

    docs = db.collection("SubCategory").stream()
    category = []
    for doc in docs:
        category.append(SubCategory.from_dict(doc.to_dict()))

    image = storage.bucket().blob(f'Image/{product.NameProduct}.png').generate_signed_url(
        timedelta(seconds=300), method='GET')

    return render_template("productInfo.html", product=product, image=image, category=category)


@app.route("/categoryInfo.html/<idCategory>")
def categoryInfo(idCategory):
    dCategory = db.collection("Category").document(idCategory)
    category = Category.from_dict(dCategory.get().to_dict())
    return render_template("categoryInfo.html", category=category)


@app.route("/subCategoryInfo.html/<idSubCategory>")
def subCategoryInfo(idSubCategory):
    dSubCategory = db.collection("SubCategory").document(idSubCategory)
    subCategory = SubCategory.from_dict(dSubCategory.get().to_dict())

    docs = db.collection("Category").stream()
    category = []
    for doc in docs:
        category.append(Category.from_dict(doc.to_dict()))

    return render_template("subCategoryInfo.html", subCategory=subCategory, category=category)

# add page


@app.route("/usersAdd.html")
def userAdd():
    docs = db.collection("Category").stream()
    category = []
    for doc in docs:
        category.append(Category.from_dict(doc.to_dict()))
    return render_template('usersAdd.html', category=category)


@app.route("/addCategory.html")
def addCategory():
    return render_template('addCategory.html')


@app.route("/addProduct.html")
def addProduct():
    docs = db.collection("SubCategory").stream()
    category = []
    for doc in docs:
        category.append(SubCategory.from_dict(doc.to_dict()))
    return render_template('addProduct.html', category=category)


@app.route("/addSubCategory.html")
def addSubCategory():
    docs = db.collection("Category").stream()
    category = []
    for doc in docs:
        category.append(Category.from_dict(doc.to_dict()))
    return render_template('addSubCategory.html', category=category)

#  function with out pages


@app.route("/delete/<document>/<idDoc>")
def delete(document, idDoc):
    if document == 'Users':
        auth.delete_user(idDoc)
    elif document == 'Products':
        dProduct = db.collection("Products").document(idDoc)
        product = Product.from_dict(dProduct.get().to_dict())
        # image delete
        bucket = storage.bucket()
        blob = bucket.blob(f'Image/{product.NameProduct}.png')
        blob.delete()
    elif document == "SubCategory":
        dSubCategory = db.collection("SubCategory").document(idDoc)
        subCategory = SubCategory.from_dict(dSubCategory.get().to_dict())
        # image delete
        bucket = storage.bucket()
        blob = bucket.blob(f'Image/{subCategory.Name}.png')
        blob.delete()
    db.collection(document).document(idDoc).delete()
    return redirect(url_for('index'))

# upload fuction


@app.route("/uploadUser", methods=['POST'])
def uploadUser():
    name = request.form.get("name")
    familyName = request.form.get("familyName")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = int(request.form.get("phone"))
    address = request.form.get("address")
    invetation = request.form.get("Category")
    typeUser = request.form.get("typeUser")
    user = auth.create_user(email=email, password=password)
    docs = db.collection("Users").document(user.uid)
    p = User(user.uid, name, familyName, address, phone, email,
             invetation, typeUser)
    docs.set(p.to_dict())
    return redirect(url_for('users'))


@app.route("/uploadProduct", methods=['POST'])
def uploadProduct():
    productName = request.form.get("productName")
    prixUnitaire = int(request.form.get("prixUnitaire"))
    prixCarton = int(request.form.get("prixCarton"))
    Quantite = int(request.form.get("Quantite"))
    category = request.form.get("category")
    docs = db.collection("Products").document()
    p = Product(category, productName, prixCarton,
                prixUnitaire, Quantite, docs.id)
    docs.set(p.to_dict())
    # image upload
    if 'images' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files["images"]
    UPLOAD_FOLDER = './static/productImage'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if file:
        filename = secure_filename(productName + '.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        bucket = storage.bucket()
        blob = bucket.blob(f'Image/{productName}.png')
        blob.upload_from_filename(
            f'{app.config["UPLOAD_FOLDER"]}/{productName}.png')
    os.remove(str(app.config['UPLOAD_FOLDER'] + '/' + productName + '.png'))
    return redirect(url_for('products'))


@app.route("/uploadCategory", methods=['POST'])
def uploadCategory():
    name = request.form.get("name")
    code = request.form.get("code")
    docs = db.collection("Category").document()
    p = Category(docs.id, name, code)
    docs.set(p.to_dict())
    return redirect(url_for('category'))


@app.route("/uploadSubCategory", methods=['POST'])
def uploadSubCategory():
    name = request.form.get("name")
    fatherCategory = request.form.get("fatherCategory")
    docs = db.collection("SubCategory").document()
    p = SubCategory(docs.id, name, fatherCategory)
    docs.set(p.to_dict())
    # image upload
    if 'images' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files["images"]
    UPLOAD_FOLDER = './static/productImage'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if file:
        filename = secure_filename(name + '.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        bucket = storage.bucket()
        blob = bucket.blob(f'Image/{name}.png')
        blob.upload_from_filename(f'{app.config["UPLOAD_FOLDER"]}/{name}.png')
    os.remove(str(app.config['UPLOAD_FOLDER'] + '/' + name + '.png'))
    return redirect(url_for('category'))

#  update functions


@app.route("/updateProduct/<idProduct>", methods=['POST'])
def updateProduct(idProduct):
    productName = request.form.get("productName")
    prixUnitaire = int(request.form.get("prixUnitaire"))
    prixCarton = int(request.form.get("prixCarton"))
    Quantite = int(request.form.get("Quantite"))
    category = request.form.get("category")
    docs = db.collection("Products").document(idProduct)
    p = Product(category, productName, prixCarton,
                prixUnitaire, Quantite, docs.id)
    docs.set(p.to_dict())
    # image upload
    if 'images' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files["images"]
    UPLOAD_FOLDER = './static/productImage'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if file:
        filename = secure_filename(productName + '.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        bucket = storage.bucket()
        blob = bucket.blob(f'Image/{productName}.png')
        blob.upload_from_filename(
            f'{app.config["UPLOAD_FOLDER"]}/{productName}.png')
    os.remove(str(app.config['UPLOAD_FOLDER'] + '/' + productName + '.png'))
    return redirect(url_for('products'))


@app.route("/updateCategory/<idCategory>", methods=['POST'])
def updateCategory(idCategory):
    name = request.form.get("name")
    code = request.form.get("code")
    docs = db.collection("Category").document(idCategory)
    p = Category(int(docs.id), name, code)
    docs.set(p.to_dict())
    return redirect(url_for('category'))


@app.route("/updateSubCategory/<idSubCategory>", methods=['POST'])
def updateSubCategory(idSubCategory):
    name = request.form.get("name")
    fatherCategory = request.form.get("fatherCategory")
    docs = db.collection("SubCategory").document(idSubCategory)
    p = SubCategory(docs.id, name, int(fatherCategory))
    docs.set(p.to_dict())
    # image upload
    if 'images' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files["images"]
    UPLOAD_FOLDER = './static/productImage'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if file:
        filename = secure_filename(name + '.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        bucket = storage.bucket()
        blob = bucket.blob(f'Image/{name}.png')
        blob.upload_from_filename(f'{app.config["UPLOAD_FOLDER"]}/{name}.png')
    os.remove(str(app.config['UPLOAD_FOLDER'] + '/' + name + '.png'))
    return redirect(url_for('category'))


@app.route("/updateUser/<idUser>", methods=['POST'])
def updateUser(idUser):
    name = request.form.get("name")
    familyName = request.form.get("familyName")
    email = request.form.get("email")
    phone = int(request.form.get("phone"))
    address = request.form.get("address")
    invetation = request.form.get("Category")
    docs = db.collection("Users").document(idUser)
    p = User(docs.id, name, familyName, address, phone, email,
             invetation, 'user')
    docs.set(p.to_dict())
    return redirect(url_for('users'))


@app.route("/updateOrder/<idOrder>", methods=['POST'])
def updateOrder(idOrder):
    deliveryBoyId = request.form.get("deliveryBoyId")
    orderSituation = request.form.get("orderSituation")

    docs = db.collection("Orders").document(idOrder)
    order = Order.from_dict(docs.get().to_dict())
    productsOrders = []

    for o in order.productOrders:
        productsOrders.append(ProductOrder.from_dict(o))

    for o in productsOrders:
        if (request.form.get(o.idOrder) != None):
            o.orderSituation = 'تم شحن'
        else:
            o.orderSituation = orderSituation

    productsOrdersObject = []
    for o in productsOrders:
        productsOrdersObject.append(o.to_dict())

    docs.update({
        "deliveryBoyId": deliveryBoyId,
        "orderSituation": orderSituation,
        "productOrders": productsOrdersObject
    })

    return redirect(url_for('orders'))

# search function


@app.route("/searchUser", methods=['POST'])
def searchUser():
    search = request.form.get("search")
    docs = db.collection("Users").where(
        filter=Or(filters=[FieldFilter("name", "==", search),
                           FieldFilter("familyName", "==", search),
                           FieldFilter("phone", "==", search),
                           FieldFilter("type", "==", search),
                           FieldFilter("email", "==", search),
                           FieldFilter("address", "==", search),
                           FieldFilter("invitation", "==", search)])
    ).stream()
    users = []
    for doc in docs:
        users.append(User.from_dict(doc.to_dict()))
    return render_template("users.html", users=users, i=1)


@app.route("/searchProduct", methods=['POST'])
def searchProduct():
    search = request.form.get("search")
    products = []
    # Category Search
    docs = db.collection("Category").where(
        filter=Or(filters=[FieldFilter("Name", "==", search),
                           FieldFilter("code", "==", search)])
    ).stream()

    for doc in docs:
        print(search)
        # sub search category
        dSubCategory = db.collection("SubCategory").where(
            filter=Or(filters=[FieldFilter("idCategory", "==", doc.to_dict()["idCategory"])])).stream()
        # product serach Subcategory
        for docSub in dSubCategory:
            dProduct = db.collection("Products").where(
                filter=Or(filters=[FieldFilter(
                    "IDCategorie", "==", docSub.to_dict()["idSubCategory"])])
            ).stream()
            # product add
            for dP in dProduct:
                products.append(Product.from_dict(dP.to_dict()))

    # SubCategory Search
    dSubCategory = db.collection("SubCategory").where(
        filter=Or(filters=[FieldFilter("Name", "==", search)])
    ).stream()
    for doc in dSubCategory:
        dProduct = db.collection("Products").where(
            filter=Or(filters=[FieldFilter("IDCategorie",
                      "==", doc.to_dict()["idSubCategory"])])
        ).stream()
        # product add
        for dP in dProduct:
            products.append(Product.from_dict(dP.to_dict()))
    # Product Search
    docs = db.collection("Products").where(
        filter=Or(filters=[FieldFilter("NameProduct", "==", search)])
    ).stream()
    for doc in docs:
        products.append(Product.from_dict(doc.to_dict()))
    return render_template("products.html", products=products)


@app.route("/searchOrder", methods=['POST'])
def searchOrder():
    search = request.form.get("search")
    docs = db.collection("Orders").where(
        filter=FieldFilter("orderSituation", "==", search)).stream()
    dUser = db.collection("Users")
    orders = []
    users = []

    for doc in docs:
        orders.append(Order.from_dict(doc.to_dict()))

    for o in orders:
        docs_user = dUser.where(filter=FieldFilter(
            "idUser", "==", o.idClient)).stream()
        for doc_user in docs_user:
            users.append(User.from_dict(doc_user.to_dict()))
    return render_template("orders.html", orders=orders, users=users, zip=zip)


@app.route("/searchCategory", methods=['POST'])
def searchCategory():
    search = request.form.get("search")
    category = {}
    subCategory = []

    docs = db.collection("Category").where(
        filter=Or(filters=[FieldFilter("Name", "==", search),
                           FieldFilter("code", "==", search)])
    ).stream()

    for doc in docs:
        d = (Category.from_dict(doc.to_dict())).to_dict()
        category[d["idCategory"]] = d
        # sub add
        dSubCategory = db.collection("SubCategory").where(
            filter=Or(filters=[FieldFilter(
                "idCategory", "==", d["idCategory"])])
        ).stream()
        for docSub in dSubCategory:
            subCategory.append(SubCategory.from_dict(docSub.to_dict()))

    dSubCategory = db.collection("SubCategory").where(
        filter=Or(filters=[FieldFilter("Name", "==", search)])
    ).stream()

    for doc in dSubCategory:
        subCategory.append(SubCategory.from_dict(doc.to_dict()))
        # category add
        dCategory = db.collection("Category").where(
            filter=Or(filters=[FieldFilter("idCategory", "==", doc.to_dict()['idCategory']),])).stream()
        for docCategory in dCategory:
            d = (Category.from_dict(docCategory.to_dict())).to_dict()
            category[d["idCategory"]] = d

    return render_template("category.html", category=category, subCategory=subCategory)

# error page


@app.errorhandler(404)
def not_found(e):
    return render_template("error-404.html")


if __name__ == "__main__":
    app.run()
