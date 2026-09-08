from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Git & GitHub", "done": True},
    {"id": 2, "title": "Learn Docker", "done": True},
    {"id": 3, "title": "Learn Jenkins CI/CD", "done": False},
]

@app.route("/")
def home():
    return jsonify({
        "message": "🚀 TaskFlow API is running!",
        "version": "1.0.0",
        "endpoints": ["/tasks", "/health"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks, "count": len(tasks)})

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
