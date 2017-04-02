from __future__ import division
from functools import partial

from desmod.component import Component
from desmod.dot import component_to_dot

# from .gtkw import write_gtkw_files
from grocery.customer import CustomerGen
from grocery.store import Store
#import Checkout


class Top(Component):
    """The top-level of the Grocery model.

    This top-level component ties together CustomerGenerator,
    Store, and Checkout components into a
    complete, simulatable model.

    """

    base_name = ''  # Suppress top-level name

    def __init__(self, *args, **kwargs):
        super(Top, self).__init__(*args, **kwargs)
        # self.info('\n' + str(self.env.geom))
        self.cgen = CustomerGen(self)
        self.store = Store(self)

    def connect_children(self):
        self.connect(self.store, 'cgen')

    @classmethod
    def pre_init(cls, env):
        # write_gtkw_files(env)
        pass

    def elab_hook(self):
        pass
        #colorscheme = self.env.config['sim.dot.colorscheme']
        #if self.env.config['sim.dot.enable']:
            #with open('component-full.dot', 'w') as dot_file:
                #dot_file.write(component_to_dot(self, colorscheme=colorscheme))
            #with open('component-hier.dot', 'w') as dot_file:
                #dot_file.write(component_to_dot(self,
                                                #show_connections=False,
                                                #show_processes=False,
                                                #colorscheme=colorscheme))
            #with open('component-conn.dot', 'w') as dot_file:
                #dot_file.write(component_to_dot(self,
                                                #show_hierarchy=False,
                                                #colorscheme=colorscheme))

    def post_sim_hook(self):
        """Called at simulation end

        """
        pass


    def get_result_hook(self, result):
        # geom = self.env.geom
        pass
