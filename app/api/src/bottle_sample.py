#from bottle import Bottle, route, redirect, run, template
#from bottle.ext import sqlite
import os
import subprocess


import bottle
from bottle.ext import sqlite

# import os

# @route('/hello/<name>')
# def index(name):
#     return template('<b>Hello {{name}}</b>!', name=name)

# @route("/uptime")
# def uptime():
#     # sending the uptime command as an argument to popen()
#     # and saving the returned result (after truncating the trailing \n)
#     ut = os.popen('uptime -p').read()[:-1]

#     return template('<b>Uptime: {{ut}}</b>', ut=ut)

# run(host="0.0.0.0", port=8080)



app = bottle.Bottle()
plugin = sqlite.Plugin(dbfile='/mnt/data/my_scripts/app/api/src/app.db')
app.install(plugin)


def brixUptime(timeout):
    out = subprocess.check_output(["/mnt/data/my_scripts/openssh_ssh_brix.sh", "uptime"], timeout=timeout)
    return out

def check_live(hostname):
    response = os.system("ping -c 1 -W 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Brix2807 is active, uptime: {}".format(brixUptime()) 
    else:
        pingstatus = "Brix2807 is inactive"

    return pingstatus

@app.route('/device/:id')
def show(id, db):
    #import pdb; pdb.set_trace()
    row = db.execute('SELECT id, name, status, ip, datetime(last_updated, "localtime") as last_updated from devices where id=?', id).fetchone()
    if row:
        #return bottle.template('<b>name: {{name}}, status: {{status}}, last_updated: {{last_updated}}</b> ', name=row["name"], status=row["status"], last_updated=row["last_updated"])

        host = row["ip"]
        uptime = None
        ping_response = os.system("ping -c 1 -W 1 " + host)
        # status 0=shutdown, 1=on, 2=sleep
        if row["status"] == 1:
            # ping_response = 0 , means alive
            if ping_response == 0:
                uptime = brixUptime(3)
        return bottle.template("device.tpl", id=row["id"], name=row["name"], status=row["status"], last_updated=row["last_updated"], uptime=uptime, ping_response=ping_response)

    return HTTPError(404, "Page not found")


@app.route('/brix2807/suspend')
def suspend_brix2807(db):
    # call a ssh shutdown command to target machine
    subprocess.call(["/mnt/data/my_scripts/openssh_ssh_brix.sh", "systemctl suspend"])
    db.execute('update devices set status=2, last_updated=datetime("now") where id=1')
    #return template('<b>suspending device: {{name}}</b>', name="brix2807")
    bottle.redirect("/device/1")


@app.route('/brix2807/shutdown')
def shutdown_brix2807(db):
    # call a ssh shutdown command to target machine
    subprocess.call(["/mnt/data/my_scripts/openssh_ssh_brix.sh", "systemctl poweroff"])
    db.execute('update devices set status=0, last_updated=datetime("now") where id=1')
    #return template('<b>suspending device: {{name}}</b>', name="brix2807")
    bottle.redirect("/device/1")


@app.route('/brix2807/wake')
def wake(db):
    #subprocess.call(["/mnt/data/my_scripts/wake_brix2807.sh"])
    os.system("/mnt/data/my_scripts/wake_brix2807.sh")
    db.execute('update devices set status=1, last_updated=datetime("now") where id=1')
    bottle.redirect("/device/1")


abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
bottle.TEMPLATE_PATH.insert(0, abs_views_path )


app.run(host="0.0.0.0", port=8080)