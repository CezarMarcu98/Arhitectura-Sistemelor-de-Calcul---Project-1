"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type_com carts: List
        :param carts: a list of add and remove operations

        :type_com marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type_com retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type_com kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.wait_time = retry_wait_time
        Thread.__init__(self, **kwargs)
        self.name = kwargs["name"]

    def run(self):
        id_cart = self.marketplace.new_cart()

        for cart in self.carts:
            for comenzi in cart:
                type_com = comenzi['type']
                cantitate = comenzi['quantity']
                prod_id = comenzi['product']
                # stochez variabilele de care am nevoie pentru prelucrare
                if type_com == 'add':
                    i = 0
                    while i < cantitate:
                        # apelez add to cart pentru a lua produs cu produs
                        # din marketplace
                        if not self.marketplace.add_to_cart(id_cart, prod_id):
                            # daca metoda intoarce false fac clientul sa astepte
                            time.sleep(self.wait_time)
                            while not self.marketplace.add_to_cart(id_cart, prod_id):
                                # cat timp inca nu reusesc sa adaug in cos, astept
                                time.sleep(self.wait_time)
                            i += 1
                        else:
                            i += 1
                elif type_com == 'remove':
                    i = 0
                    while i < cantitate:
                        # apelez remove from cart de suficiente ori incat sa
                        # se respecte cantitatea dorita de a fi eliminata
                        self.marketplace.remove_from_cart(id_cart, prod_id)
                        i = i + 1

        produse_cump = self.marketplace.place_order(id_cart)
        # intorc cosul de cumparaturi la finalul tuturor prelucrarilor
        # si afisez
        for cumparat in produse_cump:
            print("{} bought {}".format(self.name, cumparat))
