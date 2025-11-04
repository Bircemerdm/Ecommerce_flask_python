from flask import Flask, jsonify, Blueprint, request
from ecommerce.models import Category

apiCategories = Blueprint("apiCategories", __name__, url_prefix="/api/categories")


@apiCategories.route("/")
def getAllCategories():
    try:
        categories = Category.get_all_categories()
        all_category = []

        for category in categories:
            all_category.append({"id": category.id, "name": category.name})

        return jsonify({"success": True, "data": all_category})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


@apiCategories.route("add_category", methods=["GET", "POST"])
def addCategory():
    try:
        name = request.form.get("name")

        Category.add_category(name)

        return jsonify({"success": True, "message": "user added successfully"})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


@apiCategories.route("category/<int:id>", methods=["GET", "PUT", "DELETE"])
def getByIdCategory(id):

    try:
        category = Category.get_category_by_id(id)
        if category is None:
            return jsonify({"success": False, "message": "category is not find"})

        if request.method == "GET":

            if category is None:

                return jsonify({"success": False, "message": "category is not find"})
            else:
                categoryobj = {"id": category.id, "category name": category.name}
                return jsonify({"success": True, "data": categoryobj})

        elif request.method == "DELETE":

            if category is None:
                return jsonify({"success": False, "message": "category is not find"})
            else:
                Category.delete_category(id)
                return jsonify({"success": True, "message": "Category is delete"})

        elif request.method == "PUT":
            name = request.form.get("name")

            if name == None:
                name = category.name

            Category.update_category(id, name)
        return jsonify({"success": True, "message": "Category is update"})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})
