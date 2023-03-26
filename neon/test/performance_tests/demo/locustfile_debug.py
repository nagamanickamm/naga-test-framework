from locust import HttpUser, task, run_single_user

class QuickstartUser(HttpUser):
    host = "http://localhost"

    @task
    def hello_world(self):
        with self.client.get("/hello", catch_response=True) as resp:
            pass

if __name__ == "__main__":
    run_single_user(QuickstartUser)