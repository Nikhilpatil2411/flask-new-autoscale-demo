from flask import Flask, render_template, request
import requests
import socket

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id").text
    instance_type = requests.get("http://169.254.169.254/latest/meta-data/instance-type").text
    hostname = socket.gethostname()

    users = 0
    status = "Normal Traffic"

    if request.method == "POST":
        users = int(request.form["users"])

        if users > 2000:
            status = "Scaling Up → Shift to t3.micro"
        else:
            status = "Normal Traffic → Running on t2.micro"

    return render_template("index.html",
                           instance_id=instance_id,
                           instance_type=instance_type,
                           hostname=hostname,
                           users=users,
                           status=status)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)