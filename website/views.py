from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import EventLog
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required

def home():
    uv = ""
    air = ""
    if request.method == 'POST':
        if request.form.get('stat') == 'Started':
            if request.form.get('uv_s') != 'on':
                uv = 'off'
            else:
                uv = request.form.get('uv_s')
            if request.form.get('air_s') != 'on':
                air = 'off'
            else:
                air = request.form.get('air_s')
        else:
            if request.form.get('uv_s') != 'on':
                uv = 'off'
            else:
                uv = "Terminated"
            if request.form.get('air_s') != 'on':
                air = 'off'
            else:
                air = "Terminated"
        
        room = request.form.get('room_num')
        time = request.form.get('time_now')
        stat = request.form.get('stat')
        date = request.form.get('date_now')
        interval = request.form.get('interval')

        if (room == "" or time == "" or date == "" or stat == "" or (uv == "off" and air == "off")) and (stat == "Started" or stat == ""):
            return render_template("index.html", user=current_user)
        
        new_rec = EventLog(user_id=current_user.id, uv=uv, air=air, room=room,
                                time=time, interval=interval, stat=stat, date=date)
        db.session.add(new_rec)
        db.session.commit()
    return render_template("index.html", user=current_user)