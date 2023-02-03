from locust import HttpUser, TaskSet, task, between, SequentialTaskSet
import random

# USER DEFINED VARIABLES
HOST = "https://automationexercise.com"  # Hostname
# Hostname cna be overriden by passing the
# This list needs to be filled out based on the populated environment
AVAILABLE_CONTENT = {
    'home': "/",
    "products": "/products",
    'product_details': [
        '/product_details/1',
        '/product_detailss/2',
        '/product_details/2',
    ]

}


USERS = [
    {
        "username": "algo@algo.com",
        "password": "12345678"
     }
]


class UserBehavior(TaskSet):
#class UserBehavior(SequentialTaskSet):
    current_user = None

    def on_start(self):
        login_success = self.login()
        while not login_success:
            # Si el inicio de sesión falla, volvemos a intentar
            login_success = self.login()

    def login(self):
        if len(USERS):
            self.current_user = USERS.pop(0)
            with self.client.post("/login", json={
                "username": self.current_user["username"],
                "password": self.current_user["password"]
            }, name=f"login as {self.current_user['username']}", catch_response=True) as response:
                if response.status_code == 200:
                    print("Login successful")
                    return True
                else:
                    USERS.append(self.current_user)
                    response.failure("failed login")
                    return False
        else:
            return False

    @task(1)
    def go_to_home(self):
        url = AVAILABLE_CONTENT["home"]
        self.client.request("GET", url, name=f'request to home')

    @task(4)
    def go_to_products(self):
        url = AVAILABLE_CONTENT["products"]
        self.client.get(url, name=f'request to products')

    @task(1)
    def go_to_product_page(self):
        url = random.choice(AVAILABLE_CONTENT["product_details"])
        self.client.get(url, name=f"request to {url}")

    def on_stop(self):
        with self.client.get("/logout",
                             name=f"logout as {self.current_user['username']}",
                             catch_response=True) as response:
            USERS.append(self.current_user)
            response.success()


class WebsiteUser(HttpUser):
    host = HOST
    tasks = [UserBehavior]
    wait_time = between(1, 5)
