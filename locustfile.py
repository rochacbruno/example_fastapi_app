from locust import HttpUser, between, task


class MetricsUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def metrics(self):
        self.client.get("/metrics")
