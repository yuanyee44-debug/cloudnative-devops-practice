"""
Unit tests for Flask Task Management API
"""
import pytest
from app import app, tasks as initial_tasks, next_id as initial_next_id


@pytest.fixture
def client():
    """创建Flask测试客户端"""
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_tasks():
    """每个测试前重置任务数据，确保测试独立性"""
    import app as app_module
    app_module.tasks = [
        {"id": 1, "title": "学习云原生技术", "description": "了解微服务、容器编排、服务网格、DevOps四大关键技术", "done": False},
        {"id": 2, "title": "搭建CI/CD流水线", "description": "使用GitHub Actions实现自动化测试与部署", "done": False},
        {"id": 3, "title": "撰写项目报告", "description": "总结云原生DevOps实践的经验与心得", "done": False},
    ]
    app_module.next_id = 4


class TestIndex:
    """测试API首页"""

    def test_index_returns_project_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json
        assert "project" in data
        assert data["project"] == "Cloud Native DevOps Practice"
        assert "version" in data
        assert "endpoints" in data


class TestGetTasks:
    """测试获取任务列表"""

    def test_get_all_tasks(self, client, reset_tasks):
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json
        assert "tasks" in data
        assert "total" in data
        assert data["total"] >= 3

    def test_get_single_task(self, client, reset_tasks):
        response = client.get("/tasks/1")
        assert response.status_code == 200
        data = response.json
        assert data["id"] == 1
        assert data["title"] == "学习云原生技术"

    def test_get_task_not_found(self, client, reset_tasks):
        response = client.get("/tasks/999")
        assert response.status_code == 404
        data = response.json
        assert "error" in data


class TestCreateTask:
    """测试创建任务"""

    def test_create_task_success(self, client, reset_tasks):
        response = client.post("/tasks", json={"title": "部署应用到生产环境"})
        assert response.status_code == 201
        data = response.json
        assert data["title"] == "部署应用到生产环境"
        assert "id" in data

    def test_create_task_with_description(self, client, reset_tasks):
        response = client.post("/tasks", json={
            "title": "配置监控告警",
            "description": "使用Prometheus+Grafana实现服务监控"
        })
        assert response.status_code == 201
        data = response.json
        assert data["description"] == "使用Prometheus+Grafana实现服务监控"

    def test_create_task_missing_title(self, client, reset_tasks):
        response = client.post("/tasks", json={})
        assert response.status_code == 400
        data = response.json
        assert "error" in data

    def test_create_task_no_body(self, client, reset_tasks):
        response = client.post("/tasks", content_type="application/json")
        assert response.status_code == 400


class TestUpdateTask:
    """测试更新任务"""

    def test_update_task_mark_done(self, client, reset_tasks):
        response = client.put("/tasks/1", json={"done": True})
        assert response.status_code == 200
        data = response.json
        assert data["done"] is True

    def test_update_task_change_title(self, client, reset_tasks):
        response = client.put("/tasks/1", json={"title": "深入学习Kubernetes"})
        assert response.status_code == 200
        data = response.json
        assert data["title"] == "深入学习Kubernetes"

    def test_update_task_not_found(self, client, reset_tasks):
        response = client.put("/tasks/999", json={"done": True})
        assert response.status_code == 404

    def test_update_task_no_body(self, client, reset_tasks):
        response = client.put("/tasks/1", content_type="application/json")
        assert response.status_code == 400


class TestDeleteTask:
    """测试删除任务"""

    def test_delete_task_success(self, client, reset_tasks):
        response = client.delete("/tasks/1")
        assert response.status_code == 200
        data = response.json
        assert "message" in data

    def test_delete_task_verify_removed(self, client, reset_tasks):
        client.delete("/tasks/1")
        response = client.get("/tasks/1")
        assert response.status_code == 404

    def test_delete_task_not_found(self, client, reset_tasks):
        response = client.delete("/tasks/999")
        assert response.status_code == 404


class TestHealthCheck:
    """测试健康检查接口"""

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json
        assert data["status"] == "healthy"
        assert data["service"] == "task-api"
