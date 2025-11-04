# create db mizi temsil eden yer database imizin oluşturulacağı yer
from ecommerce.models import db
from ecommerce import createApp


def createDB():
    app = createApp()
    with app.app_context():  # ✔️ Doğru kullanım
        db.create_all()

    # db yi yaratırken create_all fonksiyonu kullanacağız ben neye göre yaratacağım bu db yi? initialize de createappi belirtmiştik sana createapp zaten bizi app i döndürüyor
