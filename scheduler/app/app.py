from flask import Flask, request, jsonify, json
import pika

app = Flask(__name__)

rabbitmq_host = "localhost"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue="task_queue")

tasks: dict = {}

@app.route("/tasks", methods=["POST"])
def create_task() -> json:
    task_id = len(tasks) + 1
    data = request.json
    task = {"task_id": task_id,
                      "status": "scheduled",
                      "data": data}
    tasks[task_id] = task
    
    channel.basic_publish(
        exchange='',
        routing_key="task_queue",
        body=str(task)
    )
    print(f"[x] Sent {task}")

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