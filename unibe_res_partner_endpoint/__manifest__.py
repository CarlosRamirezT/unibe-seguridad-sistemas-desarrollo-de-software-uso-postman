# -*- coding: utf-8 -*-
{
    "name": "unibe_res_partner_endpoint",
    "summary": "Module to extend res.partner model with additional endpoints",
    "description": """
This module extends the res.partner model in Odoo to provide additional endpoints for integration with external systems. It includes new views and templates to manage the extended functionalities.
    """,
    "author": "Carlos Ramirez",
    "website": "https://www.github.com/CarlosRamirezT",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["base", "contacts", "crm"],
    "data": [
        "data/endopoint_user.xml",
    ],
    "test": [
        "tests/test_res_partner_endpoints.py",
    ],
}
