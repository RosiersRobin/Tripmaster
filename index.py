from flask import Flask, redirect, url_for, render_template, request
from model.Formulas import Formulas
from model.DB import DB
import netifaces as ni
import os
import datetime

app = Flask(__name__)

# db = DB()


# this is to make a global usable variable.
# To add a new variable, just add a def method and return the method.
@app.context_processor
def utility_processor():
    def trip_state():
        return DB().get_trip_state()
    return dict(trip_state=trip_state)


# Disable all cache settings
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# This route redirects to the index page, since I don't have any reason to use the '/' here.
@app.route('/')
def redir():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/tripmaster')
def tripmaster():
    # Prefered average speed
    pref_avg_speed = DB().get_pref_avg_speed()
    # Ideal start time
    ideal_start_time = DB().get_ideal_start_time()

    return render_template('tripmaster.html', pref_avg_speed=pref_avg_speed, ideal_start_time=ideal_start_time)


@app.route('/drawmode')
def drawmode():
    return render_template('drawmode.html')


@app.route('/settings')
def settings():
    try:
        # First of all, we need to determine the used interface (wifi of ethernet)
        def_gw_device = ni.gateways()['default'][ni.AF_INET][1]
        # Get the IP
        ip = ni.ifaddresses(def_gw_device)[2][0]['addr']
    except KeyError:
        ip = "None"
    # Get the GPS status
    status = DB().get_fix()
    # Get the current setted screen brightness
    brightness = DB().get_screen_brightness()

    return render_template('settings.html', ip=ip, status=status, brightness=brightness)


###########################################################
# JAVASCRIPT ROUTES TO MAKE THINGS DYNAMIC
###########################################################
# In here, we have some javascript routes to be used with
# AJAX. Then only can be accessed by ajax ,since the urls
# are weird from construction.
###########################################################
@app.route('/ajax/get-current-speed')
def ajax_cur_speed():
    speed = DB().get_cur_speed()
    if speed > 1:
        return str(speed)
    else:
        return str(0)


@app.route('/ajax/get-total-distance')
def ajax_total_distance():
    # So, we need to get the total distance in KM,
    # As we speak, we have the distance in meters, but
    # we display it as KM, SOOOOOOOOOOOOO
    # we need to divide it by 1000 -> get km.
    m = DB().get_total_distance()
    distance = (m/1000)
    return str(round(distance, 3))


@app.route('/ajax/get-average-speed')
def ajax_avg_speed():
    if DB().get_trip_state() == 1:
        avg_speed = Formulas.avg_speed()
    else:
        avg_speed = 0.0
    # avg_speed = Formulas.avg_speed()
    return str(avg_speed)


@app.route('/ajax/get-trip-state')
def ajax_get_trip_state():
    return str(DB().get_trip_state())


@app.route('/ajax/get-toggle-trip-distance/<trip>')
def ajax_get_toggle_trip_distance(trip):
    return str(round((DB().get_toggle_trip_distance(trip)/1000), 2))


@app.route('/ajax/reset-toggle-trip', methods=["POST"])
def ajax_reset_toggle_trip():
    trip = request.form.get("trip")
    return str(DB().reset_toggle_trip(trip))


@app.route('/ajax/get-total-drove-wrong-distance')
def ajax_get_total_drove_wrong_distance():
    return str(round((DB().get_total_distance_wrong()/1000), 2))


@app.route('/ajax/get-trip-ideal-stop-time')
def ajax_get_trip_ideal_stop_time():
    total_dist = DB().get_total_distance() - DB().get_total_distance_wrong()
    total_dist_m = total_dist/1000
    time = 60
    avg = DB().get_pref_avg_speed()
    minutes_to_add = (total_dist_m * time) / avg
    start_time = datetime.datetime.strptime(str(DB().get_ideal_start_time()), '%H:%M:%S')
    ideal_stop_time = start_time + datetime.timedelta(minutes=minutes_to_add)
    return str(ideal_stop_time.strftime("%H:%M:%S"))


# THIS CONTAINS THE SECTION WITH ALL THE ROUTES TO DO A POST
@app.route('/ajax/shutdown-system-safe', methods=['POST'])
def ajax_shutdown_system():
    os.system('sudo shutdown now')
    return 'Powered off.'


@app.route('/ajax/reboot-system-safe', methods=['POST'])
def ajax_reboot_system():
    os.system('sudo reboot now')
    return 'Going down for a reboot!'


@app.route('/ajax/update-trip-state', methods=['POST'])
def ajax_update_trip_state():
    state = DB().get_trip_state()
    if state == 0:
        # Update to the 1 state
        DB().update_trip_state(1)
    else:
        # Update to the 0 state
        DB().update_trip_state(0)
    return str(state)


@app.route('/ajax/update-wrong-traject-state', methods=['POST'])
def ajax_update_wrong_traject_state():
    state = DB().get_wrong_traject_state()
    if state == 0:
        # Update to the 1 state
        DB().update_wrong_traject_state(1)
    else:
        # Update to the 0 state
        DB().update_wrong_traject_state(0)
    return str(state)


@app.route('/ajax/update-trip-pref-avg-speed', methods=['POST'])
def ajax_update_trip_pref_avg_speed():
    # Do the action
    # First get the data
    new_avg_speed = request.form.get('pref_speed')
    DB().update_pref_avg_speed(new_avg_speed)
    return "OK"


@app.route('/ajax/update-trip-ideal-start-time', methods=['POST'])
def ajax_update_trip_ideal_start_time():
    # Do the action
    # First get the data
    new_start_time = request.form.get('ideal_time')
    DB().update_ideal_start_time(new_start_time)
    return "OK"


@app.route('/ajax/update-pref-brightness', methods=['POST'])
def ajax_update_pref_brightness():
    # Do the action
    # First get the data
    new_brightness = request.form.get('brightness')
    DB().update_screen_brightness(new_brightness)
    return "OK"


@app.route('/ajax/reset-database', methods=['POST'])
def ajax_reset_database():
    DB().reset_database()
    return "OK"


@app.route('/ajax/update-toggle-trip-state', methods=['POST'])
def ajax_update_toggle_trip_state():
    trip = request.form.get("trip")
    state = request.form.get("state")
    DB().toggle_trip_state(trip, state)
    return "OK"


if __name__ == '__main__':
    # app.run()
    # app.run(debug=True, host='172.23.48.23', port=80)
    app.run(debug=True, host='0.0.0.0', port=5000)
