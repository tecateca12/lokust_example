import pytest
import invokust
import json
import os
from locust import HttpUser, TaskSet, task, between, SequentialTaskSet
import random
import allure

DEFAULT_SETTINGS_LEGACY = {
    "classes": [],
    "host": 'http://www.iana.org',
    "num_users": 1,
    "spawn_rate": 1,
    "run_time": "10s"
}


def log_results(json_results):
    with open(os.path.join("results", "locust_log.json"), "w") as wh:
        json.dump(json_results, wh, indent=4)


@pytest.fixture(scope="module")
def qa_locust_legacy():
    """
        Opens the file provided and returns the binary contents read.
    """
    def _qa_locust_legacy(settings=None):
        locust_settings = DEFAULT_SETTINGS_LEGACY.copy()
        locust_settings.update(settings)
        load_test = invokust.LocustLoadTest(invokust.create_settings(**locust_settings))
        load_test.run()
        results = load_test.stats()
        log_results(results)
        return results

    return _qa_locust_legacy



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
        if len(USERS):
            self.current_user = USERS.pop(0)
            self.client.post("/login", json={
                "username": self.current_user["username"],
                "password": self.current_user["password"]
            }, name=f"login as {self.current_user['username']}")

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


class WebsiteUser(HttpUser):
    host = HOST
    tasks = [UserBehavior]
    wait_time = between(1, 5)


settings = {
    "classes": [WebsiteUser],
    "host": WebsiteUser.host,
    "num_users": 1,
    "spawn_rate": 1,
    "run_time": "5s"
}


class TestLoad:

    def test_load(self, qa_locust_legacy):
        """
        """
        qa_locust_legacy(settings)
        allure.attach.file(
            os.path.join("results", "locust_log.json"),
            name=f"locust_log.json",
            attachment_type=allure.attachment_type.JSON)
