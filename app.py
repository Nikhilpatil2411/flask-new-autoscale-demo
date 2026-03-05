from flask import Flask, render_template, request
import requests
import socket

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    try:
        instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id",timeout=2).text
        instance_type = requests.get("http://169.254.169.254/latest/meta-data/instance-type",timeout=2).text
    except:
        instance_id = "i-demo123"
        instance_type = "t2.micro"

    hostname = socket.gethostname()

    users = ""
    status = ""

    if request.method == "POST":
        users = request.form["users"]

        if int(users) > 2000:
            status = "Scaling Up → Shift to t3.micro"
        else:
            status = "Normal Traffic"

    return render_template("index.html",
                           instance_id=instance_id,
                           instance_type=instance_type,
                           hostname=hostname,
                           users=users,
                           status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)