# Generating Load for locust

## Define user that gets simulated on the system

### HttpUser class is a central part of Locust that allows you to define a type of user that sends HTTP requests to your web server.

```sh
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
```

### A taskset is a collection of tasks that a user can perform. 

In an example script, UserBehavior is a subclass of TaskSet in which various user tasks are defined as methods. With the @task decorator, you can specify the weight of each task, which determines its execution frequency in relation to other tasks. The number inside the brackets sets the ratio of every task. The example that can be found here correspons to these ratios:

    index: 1/19,
    setCurrency: 2/19,
    browseProduct: 10/19,
    addToCart: 2/19,
    viewCart: 3/19,
    checkout: 1/19

So obviously like in real world applications users would mostly visit the website and sometimes perform actions such as putting products into the cart or paying.

```sh
class UserBehavior(TaskSet):

    @task(1)
    def task1(self):
        index(self)

    @task(2)
    def task2(self):
        setCurrency(self)

    @task(10)
    def task3(self):
        browseProduct(self)

    @task(2)
    def task4(self):
        viewCart(self)

    @task(3)
    def task5(self):
        addToCart(self)

    @task(1)
    def task6(self):
        checkout(self)

    @task(1)
    def taskThatMayFail(self):
        raise MyCustomError("Etwas ist schiefgegangen")

```

### between: A function that generates a random waiting time between tasks for each user. 
This helps to simulate user behavior more realistically, as in the real world users do not send requests continuously

```sh
wait_time = between(1, 10)
```

### Perform requests

Locust has built in function to perform get and post requests. 

```sh
response = Taskset.client.get("/product/" + product, catch_response=True)
```

```sh
response = Taskset.client.post("/product/" + product, catch_response=True)
```

# Scenarios

This documentation describes various scenarios for load tests that can be simulated with Locust. Locust is a powerful load testing tool that makes it possible to simulate the behavior of users under different conditions. Four specific scenarios are described in detail below.

## Szenario 1: Peak Load

**Goal:** The aim of this scenario is to understand how the system reacts under a sudden and extreme load. This helps to evaluate the robustness and scalability of the application.

**Simulation with Locust:**

```sh
class PeakLoadUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [UserBehavior]

    @task
    def my_task(self):
        self.client.get("/")
```

you can also add and play around with these variables in the dockerfile or inside the locust web-ui

```sh
def setup_peak_load_scenario():
    # Starten Sie Locust mit einer hohen spawn_rate, z.B. 1000 Benutzer pro Sekunde
    os.system("locust -f locustfile.py --users 5000 --spawn-rate 1000")
```

## Szenario 2: Steady Increase
**Description:** 
In this scenario, the load is slowly increased over a longer period of time. This simulates realistic growth in user numbers over time.

```sh
os.system("locust -f locustfile.py --users 1000 --spawn-rate 10 --run-time 1h")
```

To simulate continuous growth, we can set the spawn_rate to a lower value and use the --run-time option to define the duration of the test.

## Szenario 3: Continous Increase

**Description:**
The load is increased in predefined steps and then maintained for a certain time. This helps to understand how the system reacts when the load is increased in steps.

```sh
def setup_step_load_scenario():
    user_numbers = [100, 500, 1000, 1500]
    for users in user_numbers:
        os.system(f"locust -f locustfile.py --users {users} --spawn-rate 50 --run-time 10m")
        time.sleep(600)  # Warten Sie 10 Minuten zwischen den Schritten
```

## Szenario 4:  Unpredictable load peaks



**Description:**
This scenario simulates random load peaks to test the application's reaction to unexpected events.

```sh
import random

def setup_unpredictable_peak_scenario():
    while True:
        users = random.randint(100, 2000)
        spawn_rate = random.randint(50, 500)
        os.system(f"locust -f locustfile.py --users {users} --spawn-rate {spawn_rate} --run-time 5m")
        time.sleep(random.randint(300, 1200))  # Warten Sie zufällig zwischen 5 und 20 Minuten
```
