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

In dieser Dokumentation werden verschiedene Szenarien für Lasttests beschrieben, die mit Locust simuliert werden können. Locust ist ein leistungsstarkes Tool für Lasttests, das es ermöglicht, das Verhalten von Benutzern unter verschiedenen Bedingungen zu simulieren. Im Folgenden werden vier spezifische Szenarien detailliert beschrieben.

## Szenario 1: Spitzenlast

**Zielsetzung:** Das Ziel dieses Szenarios ist es, zu verstehen, wie das System unter einer plötzlichen und extremen Last reagiert. Dies hilft, die Robustheit und Skalierbarkeit der Anwendung zu bewerten.

**Simulation mit Locust:**

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

## Szenario 2: Stetiges Wachstum
**Beschreibung:** 
In diesem Szenario wird die Last langsam über einen längeren Zeitraum hinweg erhöht. Dies simuliert ein realistisches Wachstum der Benutzerzahlen über die Zeit.

```sh
os.system("locust -f locustfile.py --users 1000 --spawn-rate 10 --run-time 1h")
```

Um ein stetiges Wachstum zu simulieren, können wir die spawn_rate auf einen niedrigeren Wert setzen und die --run-time Option verwenden, um die Dauer des Tests zu definieren.

## Szenario 3: Schrittweise Erhöhung

**Beschreibung:**
Die Last wird in vordefinierten Schritten erhöht und dann für eine bestimmte Zeit aufrechterhalten. Dies hilft zu verstehen, wie das System reagiert, wenn die Last stufenweise erhöht wird.

```sh
def setup_step_load_scenario():
    user_numbers = [100, 500, 1000, 1500]
    for users in user_numbers:
        os.system(f"locust -f locustfile.py --users {users} --spawn-rate 50 --run-time 10m")
        time.sleep(600)  # Warten Sie 10 Minuten zwischen den Schritten
```

## Szenario 4: Unvorhersehbare Lastspitzen

**Beschreibung:**
Dieses Szenario simuliert zufällige Lastspitzen, um die Reaktion der Anwendung auf unerwartete Ereignisse zu testen.

```sh
import random

def setup_unpredictable_peak_scenario():
    while True:
        users = random.randint(100, 2000)
        spawn_rate = random.randint(50, 500)
        os.system(f"locust -f locustfile.py --users {users} --spawn-rate {spawn_rate} --run-time 5m")
        time.sleep(random.randint(300, 1200))  # Warten Sie zufällig zwischen 5 und 20 Minuten
```