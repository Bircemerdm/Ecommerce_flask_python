from flask import jsonify, Blueprint, request
from ecommerce.models import Admin
from werkzeug.security import generate_password_hash

apiAdmin = Blueprint("apiAdmin", __name__, url_prefix="/api/admin")


@apiAdmin.route("/")
def Users():
    try:
        admins = Admin.get_admins()
        adminlist = []
        for admin in admins:
            adminlist.append(
                {
                    "id": admin.id,
                    "name": admin.name,
                    "email": admin.email,
                    "password": admin.password,
                    "mod": admin.mod,
                }
            )
        return jsonify({"success": True, "data": adminlist, "count": len(adminlist)})
    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


@apiAdmin.route("/addAdmin", methods=["GET", "POST"])
def addAdmin():
    try:

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name == None or email == None or password == None:
            return jsonify({"success": False, "message": "missing fields"})

        hashed_password = generate_password_hash(password)

        Admin.add_admin(name, email, hashed_password)

        return {"success": True, "message": " success add Admin"}
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


@apiAdmin.route("/<int:id>", methods=["GET", "PUT", "DELETE"])
def admin(id):
    try:
        admin = Admin.get_admin_by_id(id)

        if admin is None:
            return jsonify({"sucess": False, "message": "is not found admin"})

        if request.method == "GET":
            if admin.id:
                adminobj = {
                    "id": admin.id,
                    "name": admin.name,
                    "email": admin.email,
                    "password": admin.password,
                    "mod": admin.mod,
                }

                return jsonify({"sucess": True, "data": adminobj})

        elif request.method == "DELETE":
            if admin.id:

                admin.delete_admin(id)

                return jsonify(
                    {"sucess": True, "message": "Kullanıcı başarıyla silindi"}
                )
            else:
                return jsonify({"sucess": True, "message": "is not found admin"})

        elif request.method == "PUT":

            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            if name == None:
                name = admin.name
            if email == None:
                email = admin.email
            if password == None:
                password = admin.password

            hashed_password = generate_password_hash(password)

            Admin.update_admin(id, name, email, hashed_password)

            return jsonify(
                {"sucess": True, "message": "Kullanıcı başarıyla güncellendi"}
            )

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})
