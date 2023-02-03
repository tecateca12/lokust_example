from locust import HttpUser, TaskSet, task, between
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

class UserBehavior(TaskSet):

    @task
    def go_to_home(self):
        url = AVAILABLE_CONTENT["home"]
        self.client.request("GET", url, name=f'request to home')

    @task
    def go_to_products(self):
        url = AVAILABLE_CONTENT["products"]
        self.client.get(url, name=f'request to products')

    @task
    def go_to_product_page(self):
        url = random.choice(AVAILABLE_CONTENT["product_details"])
        self.client.get(url, name=f"request to {url}")


class WebsiteUser(HttpUser):
    host = HOST
    tasks = [UserBehavior]
    wait_time = between(1, 5)
