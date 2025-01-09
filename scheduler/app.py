from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import pika # type: ignore

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:password@mysql:3306/task_scheduler"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

rabbitmq_host = "rabbitmq"
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="scheduled")

with app.app_context():
    db.create_all()


@app.route("/tasks", methods=["POST"])
def create_task() -> json:
    data = request.json
    task_name = data.get("task_name")
    task = Task(task_name=task_name)
    db.session.add(task)
    db.session.commit()
    
    channel.basic_publish(
        exchange='',
        routing_key="task_queue",
        body=str({"task_id": task.id, "task_name": task.task_name})
    )
    print(f"[x] Sent {task}")

    return jsonify({
        "message": "Task created",
        "task_id": task.id
    }), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_status(task_id: int) -> json:
    task = Task.query.get(task_id)
    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404
    return jsonify({"id": task.id, "task_name": task.task_name, "status": task.status})


if __name__ == '__main__':
    app.run(debug=True)