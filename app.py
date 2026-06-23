"""
Cloud Native DevOps Practice - Flask REST API
任务管理 REST API，用于演示 DevOps CI/CD 流水线
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# 内存存储（演示用途，不使用数据库）
tasks = [
    {"id": 1, "title": "学习云原生技术", "description": "了解微服务、容器编排、服务网格、DevOps四大关键技术", "done": False},
    {"id": 2, "title": "搭建CI/CD流水线", "description": "使用GitHub Actions实现自动化测试与部署", "done": False},
    {"id": 3, "title": "撰写项目报告", "description": "总结云原生DevOps实践的经验与心得", "done": False},
]

next_id = 4


@app.route("/", methods=["GET"])
def index():
    """API首页，返回项目信息"""
    return jsonify({
        "project": "Cloud Native DevOps Practice",
        "version": "1.0.0",
        "description": "基于Flask的任务管理REST API，用于演示DevOps CI/CD流水线",
        "endpoints": {
            "GET /tasks": "获取所有任务",
            "GET /tasks/<id>": "获取指定任务",
            "POST /tasks": "创建新任务",
            "PUT /tasks/<id>": "更新任务",
            "DELETE /tasks/<id>": "删除任务",
        }
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """获取所有任务列表"""
    return jsonify({"tasks": tasks, "total": len(tasks)})


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """获取指定ID的任务"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found", "task_id": task_id}), 404
    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def create_task():
    """创建新任务"""
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    task = {
        "id": next_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "done": data.get("done", False),
    }
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """更新指定任务"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found", "task_id": task_id}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """删除指定任务"""
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found", "task_id": task_id}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted", "task_id": task_id}), 200


@app.route("/health", methods=["GET"])
def health_check():
    """健康检查接口，用于CI/CD监控"""
    return jsonify({"status": "healthy", "service": "task-api"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
