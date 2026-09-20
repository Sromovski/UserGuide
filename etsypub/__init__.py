"""Publish the Field Guide volumes to Etsy as digital instant-download listings.

Structure and safety rules are lifted from C:\\Projects\\TShirt1\\pod-pipeline, which
reaches Etsy through Printify. Printify has no concept of a digital download, so the
transport here is the Etsy Open API v3 directly — but the shape is deliberately the same:
SQLite state per (sku, channel), an idempotent publish that records the remote id before
anything else, reconciliation against what the channel actually holds, and paced batches.
"""
