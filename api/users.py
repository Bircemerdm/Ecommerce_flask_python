from flask import Flask, jsonify, Blueprint, request
from ecommerce.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

# yeni bir routera ihtiyacımız var app.router ı kullanamayız çünkü app dosyasında flask frameworkünü ayağa kaldırıp app ismini verdik burda başka bir isimlendirme yapmamız gerek

apiUser = Blueprint("apiUser", __name__, url_prefix="/api/users")


@apiUser.route("/")
def users():
    try:

        allUsers = User.get_all_users()
        users = []

        for user in allUsers:
            users.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                    "activated": user.activated,
                }
            )
        return jsonify({"success": True, "data": users, "count": len(users)})

    except Exception as e:
        print("Error in users: ", e)
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
def user(id):
    try:
        user = User.get_user_by_id(id)
        if user is None:
            return jsonify({"sucess": False, "message": "is not found user"})

        if request.method == "GET":
            if user.id:

                userObject = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "password": user.password,
                }
                return jsonify({"success": True, "data": userObject})

            else:

                return jsonify({"success": False, "message": "User is not found"})

            # --------------------------------------------------------------------

        elif request.method == "DELETE":

            if user.id:
                user.delete_user(id)
                return jsonify({"success": True, "message": "user Deleted"})
            else:
                return jsonify({"success": False, "message": "user not found"})
        # --------------------------------------------------------------------
        elif request.method == "PUT":

            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            if username == None:
                username = user.username
            if email == None:
                email = user.email
            if password == None:
                password = user.password

            hashed_password = generate_password_hash(password)

            User.update_user(id, username, email, hashed_password)

            return jsonify({"success": True, "message": " user Uptade "})

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


# Register işlemi
@apiUser.route("/addUser", methods=["GET", "POST"])
def user_add():
    try:
        # formdan gelen verileri aldık ve veritabanına yolladık
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if username == None or email == None or password == None:
            return jsonify({"success": False, "message": "missing fields"})

        hashed_password = generate_password_hash(password)
        User.add_user(username, email, hashed_password)
        return jsonify({"success": True, "message": "kullanıcı başarıyla eklendi"})
    except Exception as e:
        print("Error in users :", e)
        return jsonify({"success": False, "message": "there is an error"})


# Eğer herhangi bir adımda (örneğin veritabanı bağlantısında) hata olursa, uygulama çökmesin diye try-except kullanılıyor.


@apiUser.route("/activate", methods=["POST"])
def activated():
    try:
        id = request.form.get("id")
        user = User.get_user_by_id(id)
        if user is None:
            return jsonify({"success": False, "message": "user is not found"})

        if user.activated == "True":
            return "User already activated"

        else:
            User.activate_user(id)
            return "Done"
    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/deactivate", methods=["POST"])
def deactivated():
    try:
        id = request.form.get("id")
        user = User.get_user_by_id(id)
        if user is None:
            return jsonify({"success": False, "message": "user is not found"})

        if user.activated == "False":
            return "User already deactivated"

        else:
            User.deactivate_user(id)
            return "Done deactive"

    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/deactivateusers", methods=["GET"])
def deactivatedUser():
    try:
        users = User.get_all_users()
        userobj = []

        for user in users:
            if user.activated == False:
                userobj.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "password": user.password,
                        "activated": user.activated,
                    }
                )
        if len(userobj) > 0:
            return jsonify({"success": True, "data": userobj, "count": len(userobj)})
        else:
            return jsonify({"success": False, "message": "no deactivated users"})

    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/activateusers", methods=["GET"])
def activatedUser():
    try:
        users = User.get_all_users()
        userobj = []

        for user in users:
            if user.activated == True:
                userobj.append(
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "password": user.password,
                        "activated": user.activated,
                    }
                )
        if len(userobj) > 0:
            return jsonify({"success": True, "data": userobj, "count": len(userobj)})
        else:
            return jsonify({"success": False, "message": "no activated users"})

    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/login", methods=["POST"])
def UserLogin():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return jsonify(
                {
                    "success": False,
                    "message": "Email and Password fiels can't be empty",
                },
                400,
            )

        user = User.get_by_user_email(email)

        if not user and not check_password_hash(user.password, password):
            return jsonify(
                {"sucess": False, "message": "Email or password is incorrect"}
            )

        access_token = create_access_token(
            identity=str(user.id), additional_claims={"role": "user"}
        )

        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify(
            {
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "userId": user.id,
                "userEmail": user.email,
                "message": "login successful",
            }
        )

    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/register", methods=["POST"])
def UserRegister():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        old_email = User.get_by_user_email(email)

        if not username or not email or not password:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "username, email or password can not be empty",
                    }
                ),
                400,
            )

        hashed_password = generate_password_hash(password)

        if old_email:
            return (
                jsonify({"success": False, "message": "This user already exists"}),
                409,
            )

        User.add_user(username, email, hashed_password)
        return jsonify({"success": True, "message": "User added successfully "}), 201
    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


@apiUser.route("/profile", methods=["GET"])
@jwt_required()  # Bu fonksiyon çalışmadan önce geçerli bir JWT var mı kontrol et
def myProfile():
    try:
        user_id = get_jwt_identity()

        user = User.get_user_by_id(user_id)

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        return jsonify(
            {
                "success": True,
                "data": {"id": user.id, "username": user.username, "email": user.email},
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": "there is an error"})


# @apiUser.route("/")
# def Users():
#     allUsers=[{"id":1,"name":"ali", "surname":"cark" ,"age":22},
#               {"id":2,"name":"veli", "surname":"vali", "age":25},
#               {"id":3,"name":"ahmet", "surname":"aga" ,"age":23}]
#     return jsonify({"success":True, "data": allUsers})
# @apiUser.route("/<int:id>")
# def User(id):
#     user={"id":1,"name":"ali", "surname":"cark" ,"age":22}
#     return jsonify({"success":True, "data": user})

# @apiUser.route("/addUser", methods=["GET", "POST"])
# def addUser():

#     print("dneeme")
#     # print("🚀 method:", request.method)
#     print("📦 args:", request.args.get("username"), request.args.get("email"),request.args.get("password"))         # URL üzerinden gelen parametreler
#     print("data", request.data)
#     # print("📝 form:", request.form)         # form-data veya x-www-form-urlencoded
#     # print("📂 json:", request.get_json())   # JSON body


#     return jsonify({"success": True, "message": "User Added"})
