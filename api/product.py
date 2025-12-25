from flask import Flask, jsonify, Blueprint, request
from ecommerce.models import Product
from utils.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt

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
@admin_required
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


@apiProduct.route("<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def DeleteUpdateproduct(id):
    try:
        product = Product.get_product_by_id(id)

        claims = get_jwt()
        role = claims.get("role")

        if product.id == None:
            return jsonify({"succes": False, "message": "Product is not find"})

        if role != "admin":
            return jsonify({"success": False, "message": "Admin access required"})

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


@apiProduct.route("/<int:id>", methods=["GET"])
def getProductById(id):
    try:
        product = Product.get_product_by_id(id)
        if not product:
            return jsonify({"success": False, "message": "Product not found"}), 404

        return jsonify(
            {
                "success": True,
                "data": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "oldPrice": product.oldPrice,
                    "description": product.description,
                    "category_id": product.category_id,
                },
            }
        )

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"}), 500


@apiProduct.route("/get", methods=["GET"])
def get_paginate():
    try:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 1, type=int)

        result = Product.paginate(page, limit)

        products = []
        for product in result["items"]:
            products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "oldPrice": product.oldPrice,
                    "description": product.description,
                    "category_id": product.category_id,
                }
            )
        return jsonify(
            {
                "success": True,
                "data": products,
                "pagination": {
                    "page": result["page"],
                    "limit": result["limit"],
                    "total": result["total"],
                    "total_pages": result["total_pages"],
                },
            }
        )

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})
