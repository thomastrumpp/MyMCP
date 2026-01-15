from locust import HttpUser, task, between

class McpServerUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def connect_sse(self):
        # Simulate an SSE client connecting to the endpoint
        with self.client.get("/sse", stream=True, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to connect: {response.status_code}")
            # We don't keep the connection open forever in this load test, 
            # we just test the handshake capacity.
