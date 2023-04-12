from earthquake import Earthquake
from flask import Flask, render_template, make_response, flash, request
from datetime import timedelta
from models import db, Subscribe
import secrets
from mail_sender import MailSender
import os
from dotenv import load_dotenv

load_dotenv()
SMTPAPIKEY = os.getenv("SMTPAPIKEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)


eq = Earthquake()

@app.context_processor
def total_subscribers():
    ln = len(Subscribe.query.filter_by().all())
    return {"total_subscribers":ln}

@app.context_processor
def total_count():
    sm = 0
    for subscribe in Subscribe.query.filter_by().all():
        sm += int(subscribe.count)
    return {"total_count":sm}

@app.route('/', methods=["GET", "POST"])
def index():
    ln = len(Subscribe.query.filter_by().all())
    print(ln)
    if request.method == "POST":
        email = request.form.get("email")
        if Subscribe.query.filter_by(email=email).first():
            flash("Bu mail ile bir abonelik zaten mevcut !")
        else:
            while True:
                api_key = secrets.token_hex(16)
                if not Subscribe.query.filter_by(APIKey=api_key).first():
                    new_subscriber = Subscribe(email=email, APIKey=api_key)
                    db.session.add(new_subscriber)
                    db.session.commit()
                    break
            """sender=MailSender(sender_mail=SENDER_EMAIL, token=SMTPAPIKEY)
            sender.send_message(api_key=api_key, receiver=email)"""

    return render_template("index.html")
    

@app.route('/earthquakes')
def get_earthquakes():
    min = request.args.get("min")
    max = request.args.get("max")
    if min and max:
        if request.args.get("order_by"):
            return order(ls=eq.filter_by_intensity(min=float(min), max=float(max)))
        return eq.filter_by_intensity(min=float(min), max=float(max))
    if max:
        if request.args.get("order_by"):
            return order(ls=eq.filter_by_intensity(max=float(max)))
        return eq.filter_by_intensity(max=float(max))
    if min:
        if request.args.get("order_by"):
            return order(ls=eq.filter_by_intensity(min=float(min)))
        return eq.filter_by_intensity(min=float(min))
    
    if request.args.get("order_by"):
                return order(ls=eq.earthquakes())
    return make_response(eq.earthquakes()), 200


@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    return make_response(eq.earthquakes()[id-1])


@app.route("/earthquakes/<city>")
def get_city(city):
    eq = Earthquake()
  
    if eq.city_response(city):
        ls = eq.city_response(city)
        if request.args.get("distance"):
            distance = int(request.args.get("distance"))
            if request.args.get("order_by"):
                return order(ls=ls, city=city, distance=distance)
            
            min = request.args.get("min")
            max = request.args.get("max")
            if min and max:
                    if request.args.get("order_by"):
                        return order(ls=eq.filter_by_intensity(min=float(min), max=float(max)), city=city, distance=distance)
                    return eq.filter_by_intensity(min=float(min), max=float(max))
            if max:
                if request.args.get("order_by"):
                    return order(ls=eq.filter_by_intensity(max=float(max)), city=city, distance=distance)
                return eq.filter_by_intensity(max=float(max))
            if min:
                if request.args.get("order_by"):
                    return order(ls=eq.filter_by_intensity(min=float(min)), city=city, distance=distance)
                return eq.filter_by_intensity(min=float(min))

        if request.args.get("order_by"):
                return order(ls=ls, city=city)       

        return make_response(eq.city_response(city=city))
        
    


def order(ls, city=None, distance=None):
    _order = request.args.get("order")
    if _order == None:
         _order = "ascending"
    if request.args.get("order_by") == "intensity": 
        return eq.order_by_intensity(ls=ls, order=_order)
    if request.args.get("order_by") == "depth":
        return eq.order_by_depth(ls=ls, order=_order)
    if distance and city:
        if request.args.get("order_by") == "distance":
            return eq.order_by_distance(city=city, distance_control=distance, order=_order)
    
    


if __name__ == '__main__':
    app.run()
 
    
