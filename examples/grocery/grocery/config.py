"""Comprehensive default configuration."""

from  desmod.config import NamedManager

named = NamedManager()

def _setup_named(named):
    named.name('default', [], {
        'store.max_customers': 100,
        'store.customers_per_hour': 120,
        'sim.duration': '100 s',
    })

_setup_named(named)
