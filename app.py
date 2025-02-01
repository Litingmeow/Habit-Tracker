from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret"

# Global storage for user habits and coins
users = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        session["user"] = "default"
    
    user = session["user"]
    
    if user not in users:
        users[user] = {"tasks": [], "coins": 0}

    if request.method == "POST":
        task = request.form["task"]
        time_planned = request.form["time"]
        
        if time_planned.isdigit():
            time_planned = int(time_planned)
            users[user]["tasks"].append({"name": task, "time_planned": time_planned, "time_spent": 0, "status": "pending"})
        
    return render_template("index.html", tasks=users[user]["tasks"], coins=users[user]["coins"])

@app.route("/log_time", methods=["POST"])
def log_time():
    user = session["user"]
    
    task_id = int(request.form["task_id"])
    time_spent = request.form["time_spent"]

    if time_spent.isdigit():
        time_spent = int(time_spent)
        task = users[user]["tasks"][task_id]
        task["time_spent"] = time_spent
        
        if time_spent >= task["time_planned"]:
            task["status"] = "completed"
            users[user]["coins"] += 1  # Reward user with a coin
        else:
            task["status"] = "incomplete"
    
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()  # Clear all session data
    users.clear()  # Clear stored user habit data
    return redirect(url_for("index"))  # Redirect back to home

if __name__ == "__main__":
    app.run(debug=True)
