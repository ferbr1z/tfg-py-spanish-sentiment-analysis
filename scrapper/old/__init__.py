from .compat import apply_twikit_patches

apply_twikit_patches()  # debe correr antes de instanciar cualquier twikit.Client

from .client import Scrapper

__all__ = ['Scrapper']
