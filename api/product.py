from flask import Flask, jsonify, Blueprint, request
from ecommerce.models import Product

apiProduct = Blueprint("apiProduct", __name__, url_prefix="/api/product")


@apiProduct.route("/")
def get_all_product():
    try:
        products = Product.get_all_products()
        productList = []

        for product in products:
            productList.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "oldPrice": product.oldPrice,
                    "description": product.description,
                    "category_id": product.category_id,
                }
            )

        return jsonify({"success": True, "data": productList})

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


@apiProduct.route("/addProduct", methods=["GET", "POST"])
def addProduct():
    try:
        name = request.form.get("name")
        price = request.form.get("price")
        oldPrice = request.form.get("oldPrice")
        description = request.form.get("description")
        category_id = request.form.get("category_id")

        if name == None:
            return {"success": False, "message": "name is required"}
        if price == None:
            price = oldPrice
        if oldPrice == None:
            return {"success": False, "message": "oldPrice is required"}
        if description == None:
            return {"success": False, "message": "description is required"}
        if category_id == None:
            return {"success": False, "message": "category_id is required"}

        Product.add_product(name, price, oldPrice, description, category_id)

        return jsonify({"success": True, "message": "Product added successfully"})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


@apiProduct.route("<int:id>", methods=["GET", "PUT", "DELETE"])
def product(id):
    try:
        product = Product.get_product_by_id(id)

        if product.id == None:
            return jsonify({"succes": False, "message": "Product is not find"})

        if request.method == "GET":
            productObj = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "oldPrice": product.oldPrice,
                "description": product.description,
                "category_id": product.category_id,
            }

            return jsonify({"succes": True, "data": productObj})

        if request.method == "DELETE":

            product.delete_product(id)
            return jsonify({"success": True, "message": "product Deleted"})

        if request.method == "PUT":
            name = request.form.get("name")
            price = request.form.get("price")
            oldPrice = request.form.get("oldPrice")
            description = request.form.get("description")
            category_id = request.form.get("category_id")

            if name == None:
                name = product.name
            if price == None:
                price = product.price
            if oldPrice == None:
                oldPrice = product.oldPrice
            if description == None:
                description = product.description
            if category_id == None:
                category_id = product.category_id

            product.update_product(id, name, price, oldPrice, description, category_id)

            return jsonify({"success": True, "message": "product updated"})

    except Exception as e:
        print("error", e)
        return jsonify({"success": False, "message": "there is an error"})
