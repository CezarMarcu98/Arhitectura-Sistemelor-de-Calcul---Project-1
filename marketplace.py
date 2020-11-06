"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.id_prod = -1
        self.id_cons = -1
        self.queue_size = queue_size_per_producer
        self.mutex = Lock()
        self.producer_list = []  # lista din magazin a producatorului
        self.cart_list = []  # lista din magazin de cosuri
        self.restituire_la_prod = []  # lista auxiliara in care retin
        # detalii despre produsele cumparate

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.mutex.acquire()
        self.id_prod = self.id_prod + 1
        # initializez un nou spatiu de stocare pt noul producator
        self.producer_list.append([])
        aux = self.id_prod
        self.mutex.release()
        return aux

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # daca am spatiu in coada atasez produsul in lista de produse a vanzatorului
        self.mutex.acquire()
        if len(self.producer_list[producer_id]) <= self.queue_size:
            self.producer_list[producer_id].append(product)
            self.mutex.release()
            return True
        self.mutex.release()
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.mutex.acquire()
        cart = []
        # pun la dispozitie un nou spatiu in care se retin produse
        # pentru cumparator / client
        self.cart_list.append(cart)
        self.id_cons += 1
        aux = self.id_cons
        self.mutex.release()
        return aux

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.mutex.acquire()
        for one_prod in self.producer_list:
            # caut la fiecare producator sa vad daca au pe stoc produsul dorit
            for produs in one_prod:
                # caut prin toate produsele producatorilor
                if product == produs:
                    # daca am gasit il adaug in cos
                    self.cart_list[cart_id].append(produs)
                    self.restituire_la_prod.append(
                        [self.producer_list.index(one_prod), produs, cart_id])
                    # trebuie sa retin cosul in care pun , de la ce producator am luat
                    # si ce am luat pentru a sti , in cazul in care vreau sa-l returnez
                    # unde sa-l pun la loc
                    one_prod.remove(produs)
                    # scot din lista disponibila a producatorului obiectul luata
                    self.mutex.release()
                    return True
        self.mutex.release()
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.mutex.acquire()
        for produs in self.cart_list[cart_id]:
            # caut in cosul de cumparaturi produsul ce trebuie eliminat
            if produs == product:
                # odata gasit , il scot din cos si il pun de unde
                # l-am luat
                self.cart_list[cart_id].remove(produs)
                for k in self.restituire_la_prod:
                    # verific produsul si cosul in care a fost pus
                    # pentru a stii daca scot de unde trebuie
                    if k[1] == produs and k[2] == cart_id:
                        self.producer_list[k[0]].append(k[1])
                        break
                break
        self.mutex.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.cart_list[cart_id]
