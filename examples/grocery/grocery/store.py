from __future__ import division
from collections import deque

from desmod.component import Component
from desmod.queue import Queue
import simpy
from itertools import chain, count



class Store(Component):
    """Host I/O traffic model.

    The host issues LBA (sector) oriented read and write traffic to the FE. The
    host maintains a configurable queue depth which defines how many IO
    commands may be in-flight in parallel.

    """

    base_name = 'store'

    def __init__(self, *args, **kwargs):
        super(Store, self).__init__(*args, **kwargs)

        self.add_process(self._process_customers)

        self.add_connections('cgen')



    def _process_customers(self):
        entrance_queue = self.cgen.submit_queue
        exit_queue = self.cgen.return_queue
        rand = self.env.rand
        prev_cmd_submit = self.env.now

        while True:
            customer = yield entrance_queue.get()
            print('Got customer {0.cid} with items={0.num_items}'.format(customer))
            delay = rand.expovariate(10)
            yield self.env.timeout(delay)

            # Update the previous customer submission time
            prev_cmd_submit = self.env.now

            yield exit_queue.put(customer)


    def post_sim_hook(self):
        pass

    def get_result_hook(self, result):
        pass

