## The goal of this scenario is to create an even and predictable load on all services. 
## This can be helpful to understand the baseline performance of your application.

import random
from locust import HttpUser, TaskSet, between, task, events
import time
import random

class MyCustomError(Exception):
    """Das ist Eine benutzerdefinierte Ausnahmeklasse."""
    pass

products = [
    '0PUK6V6EV0',
    '1YMWWN1N4O',
    '2ZYFJ3GM2N',
    '66VCHSJNUP',
    '6E92ZMYYFZ',
    '9SIQT8TOJO',
    'L9ECAV7KIM',
    'LS4PSXUNUM',
    'OLJCESPC7Z',
]

def simulate_network_delay(): 
    time.sleep(random.uniform(0.5, 2))  

def maybe_raise_exception(response=None):
    if random.randint(1, 80) == 1:
        simulate_network_delay()
        if response:
            response.failure("Ungültige Angaben des Nutzers haben zu einer Fehlermeldung geführt.")
        raise MyCustomError("Das ist eine Testexception um reale Applikation besser nachzubilden.")

def index(l):
    with l.client.get("/", catch_response=True) as response:
        try:
            maybe_raise_exception(response)
        except MyCustomError:
            pass

def setCurrency(l):
    currencies = ['EUR', 'USD', 'JPY', 'CAD']
    with l.client.post("/setCurrency", {'currency_code': random.choice(currencies)}, catch_response=True) as response:
        try:
            maybe_raise_exception(response)
        except MyCustomError:
            pass

def browseProduct(l):
    product = random.choice(products)
    with l.client.get("/product/" + product, catch_response=True) as response:
        try:
            maybe_raise_exception(response)
            if product == "ERROR" or response.status_code == 404:
                response.failure("Ungültiges Produkt wurde angefragt")
            else:
                response.success()
        except MyCustomError:
            pass

def viewCart(l):
    with l.client.get("/cart", catch_response=True) as response:
        try:
            maybe_raise_exception(response)
        except MyCustomError:
            pass

def addToCart(l):
    product = random.choice(products)
    with l.client.get("/product/" + product, catch_response=True) as response_get:
        try:
            maybe_raise_exception(response_get)
            if product == "ERROR" or response_get.status_code == 404:
                response_get.failure("Ungültiges Produkt wurde angefragt")
            else:
                with l.client.post("/cart", {'product_id': product, 'quantity': random.choice([1,2,3,4,5,10])}, catch_response=True) as response_post:
                    try:
                        maybe_raise_exception(response_post)
                        if response_post.status_code != 200:
                            response_post.failure("Produkt konnte nicht zum Warenkorb hinzugefügt werden")
                        else:
                            response_post.success()
                    except MyCustomError:
                        pass
        except MyCustomError:
            pass

def checkout(l):
    with l.client.post("/cart/checkout", {
        'email': 'someone@example.com',
        'street_address': '1600 Amphitheatre Parkway',
        'zip_code': '94043',
        'city': 'Mountain View',
        'state': 'CA',
        'country': 'United States',
        'credit_card_number': '4432-8015-6152-0454',
        'credit_card_expiration_month': '1',
        'credit_card_expiration_year': '2039',
        'credit_card_cvv': '672',
    }, catch_response=True) as response:
        try:
            maybe_raise_exception(response)
            # Hier könnten Sie zusätzliche Überprüfungen basierend auf der Antwort durchführen
        except MyCustomError:
            pass


## when you set conc users to 100 -> 100 dieser User klassen werden definiert
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


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 10)
