"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.wait_time = republish_wait_time
        Thread.__init__(self, **kwargs)

    def run(self):
        id_crt = self.marketplace.register_producer()

        while True:
            for poz in self.products:
                # poz = elementul curent in lista producatorului
                # de produse (no inspiration, sorry)
                (prod, cantitate_curr, timp_productie_curr) = poz
                # imi setez in variabile valorile necesare prelucrarilor
                time.sleep(cantitate_curr * timp_productie_curr)
                # astept ca elementul curent sa fie produs in cantitatea dorita
                index = 0
                while index < cantitate_curr:
                    # incep publicare si pun produs cu produs pana cand ajung
                    # la cantitatea dorita
                    if not self.marketplace.publish(id_crt, prod):
                        # daca nu reusesc -> queue plin deci astept
                        time.sleep(self.wait_time)
                        while not self.marketplace.publish(id_crt, prod):
                            # cat timp intampin probleme cu publicarea
                            # (nu am loc in coada) astept
                            time.sleep(self.wait_time)
                        index += 1  # cand reusesc sa il public , incrementez
                    else:  # indexul pt a ajunge la numarul
                        index += 1  # dorit de publicari (cantitate)
