from __future__ import division
from collections import deque

from desmod.component import Component
from desmod.queue import Queue
import simpy
from itertools import chain, count


cid_counter = count(start=0)

class Customer(object):

    __slots__ = ('num_items', 'cid')

    def __init__(self):
        self.reset()

    def setup(self, num_items):
        self.num_items = num_items
        self.cid = next(cid_counter)

    def reset(self):
        self.num_items = None
        self.cid = None

    def __str__(self):
        if self.cid is None:
            return ('Customer(cid=None'.format(self))

        return ('Customer(cid={0.cid:06x}'.format(self))


class CustomerGen(Component):
    """Host I/O traffic model.

    The host issues LBA (sector) oriented read and write traffic to the FE. The
    host maintains a configurable queue depth which defines how many IO
    commands may be in-flight in parallel.

    """

    base_name = 'cgen'

    def __init__(self, *args, **kwargs):
        super(CustomerGen, self).__init__(*args, **kwargs)

        max_customers = 50
        self.customers_per_hour =  120


        self.idle_queue = Queue(self.env, capacity=max_customers,
                              items=(Customer()
                                     for _ in range(max_customers)))
        self.return_queue = Queue(self.env, capacity=max_customers)

        self.submit_queue = Queue(self.env, capacity=max_customers)


        #self.auto_probe('queue_depth_{}'.format(stream_id),
                        #self.submit_queue, trace_remaining=True,
                        #vcd={})

        self.add_process(self._submit_loop)

        self.add_processes(self._complete_loop)



    def _submit_loop(self):
        idle_queue = self.idle_queue
        cust_per_sec = self.customers_per_hour / 3600.0

        rand = self.env.rand
        prev_cmd_submit = self.env.now

        while True:
            customer = yield idle_queue.get()
            num_items = 2
            delay = rand.expovariate(cust_per_sec)
            yield self.env.timeout(delay)

            # Update the previous customer submission time
            prev_cmd_submit = self.env.now

            customer.setup(num_items)

            yield self.submit_queue.put(customer)


    def _complete_loop(self):
        while True:
            customer = yield self.return_queue.get()

            customer.reset()

            # The following shouldn't ever wait as then one stream
            # can block another one from progress
            yield self.idle_queue.put(customer)


    def post_sim_hook(self):
        pass

    def get_result_hook(self, result):
        pass

