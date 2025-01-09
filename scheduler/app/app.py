from flask import Flask, request, jsonify, json

app = Flask(__name__)

tasks: dict = {}

@app.route("/tasks", methods=["POST"])
def create_task() -> json:
    task_id = len(tasks) + 1
    data = request.json
    tasks[task_id] = {"task_id": task_id,
                      "status": "scheduled",
                      "data": data}
    return jsonify({
        "message": "Task created",
        "task_id": task_id
    }), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_status(task_id: int):
    task = tasks.get(task_id)
    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True)