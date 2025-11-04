from flask import Flask, jsonify
from flask_cors import CORS
from api.users import apiUser
from api.product import apiProduct
from api.admin import apiAdmin
from api.categories import apiCategories


from ecommerce import createApp
from ecommerce.initialize_db import createDB

# api dosyanının altındaki userstan apiUserı çağır
# app = Flask(__name__) # Burada Flask sınıfından bir uygulama nesnesi (app) oluşturduk.üm yönlendirmeleri (@app.route()), ayarları ve sunucuyu bu nesne üzerinden yönetiyorsun.


# app ve db yaratma ----------------------------------
app = createApp()
CORS(app)
# CORS (Cross-Origin Resource Sharing) = “Farklı alan adlarından gelen isteklere izin vermek” anlamına gelir.“Bu Flask uygulamasına (app) başka alan adlarından (örneğin React uygulamasından) gelen istekleri kabul et.”
createDB()

# kayıt alanı (app üzerine kaydetmediğim hiç bir sayfa app üzerinde görünmez tarayıcıda ulaşamayız)

app.register_blueprint(apiUser)
app.register_blueprint(apiProduct)
app.register_blueprint(apiAdmin)
app.register_blueprint(apiCategories)


@app.route("/")
def hello_world():
    return jsonify({"success": True, "message": "Main Page"})


# @app.route("/shares")
# def shares():
#     return "shares page"

if __name__ == "__main__":
    app.run(debug=True)

    # Python dosyası doğrudan çalıştırıldığında (python app.py), app.run() komutu çağrılır.
