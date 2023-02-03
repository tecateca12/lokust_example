# lokust_example

## Setup
### Create venv
`python3 -m venv .env`

### Activate env
`source .env/bin/activate `

### Install requirements
`pip install -r requirements.txt`

## Usage

### WebUi

* `locust -f ${locustfile}.py`
* Go to  http://0.0.0.0:8089

### Headless 

* ` locust -f ${locustfile}.py --csv={path/filename} -u {int:amount of users} -r {int: rampage} --run-time {execution time, examples 10s;20m 1h30m} --headless  --html={path/filename}
`
### Pytest

* `pytest ${pytestfile}.py --alluredir=results`
* `allure serve results`