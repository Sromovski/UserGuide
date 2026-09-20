"""Publish the Field Guide products to Gumroad.

Unlike Etsy, Gumroad needs no OAuth consent — a single access token in .env does it.
And unlike every public doc claims, product creation over the API works; see client.py.
"""
from .client import Gumroad, GumroadError

__all__ = ['Gumroad', 'GumroadError']
