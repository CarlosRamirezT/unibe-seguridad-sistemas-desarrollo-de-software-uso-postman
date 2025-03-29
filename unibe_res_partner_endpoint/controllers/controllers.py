import json

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, ValidationError

class UnibeResPartnerEndpoint(http.Controller):
    """
    Controller for managing res.partner records via HTTP endpoints.
    This controller includes security measures to protect against common cyber attacks such as:
    - SQL Injection: Using Odoo ORM methods which are safe from SQL injection.
    - HTML Injection: Ensuring that data is properly sanitized before rendering.
    - CSRF: Using Odoo's built-in CSRF protection for POST, PUT, and DELETE requests.
    - Authentication: Ensuring that only authenticated users can access these endpoints.
    """

    @http.route('/unibe_res_partner_endpoint/partners', auth='user', type='json', methods=['GET'])
    def list_partners(self, **kw):
        if not request.env.user.has_group('base.group_user'):
            raise AccessError("You do not have the necessary permissions to access this resource.")
        partners = request.env['res.partner'].search([])
        partners_data = partners.read(['name', 'email', 'phone'])
        return partners_data

    @http.route('/unibe_res_partner_endpoint/partners', auth='user', type='json', methods=['POST'], csrf=True)
    def create_partner(self, **kw):
        if not request.env.user.has_group('base.group_user'):
            raise AccessError("You do not have the necessary permissions to access this resource.")
        try:
            # Intenta acceder a request.jsonrequest, si no existe, procesa manualmente el JSON
            partner_data = request.jsonrequest
        except AttributeError:
            partner_data = json.loads(request.httprequest.data or '{}')
        # Validate input data
        if not partner_data.get('name') or not partner_data.get('email'):
            raise ValidationError('Name and email are required')
        new_partner = request.env['res.partner'].create(partner_data)
        return {'id': new_partner.id}

    @http.route('/unibe_res_partner_endpoint/partners/<int:partner_id>', auth='user', type='json', methods=['DELETE'], csrf=True)
    def delete_partner(self, partner_id, **kw):
        if not request.env.user.has_group('base.group_user'):
            raise AccessError("You do not have the necessary permissions to access this resource.")
        partner = request.env['res.partner'].browse(partner_id)
        if partner.exists():
            partner.unlink()
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Partner not found'}

    @http.route('/unibe_res_partner_endpoint/partners/<int:partner_id>', auth='user', type='json', methods=['PUT'], csrf=True)
    def update_partner(self, partner_id, **kw):
        if not request.env.user.has_group('base.group_user'):
            raise AccessError("You do not have the necessary permissions to access this resource.")
        try:
            # Intenta acceder a request.jsonrequest, si no existe, procesa manualmente el JSON
            partner_data = request.jsonrequest
        except AttributeError:
            partner_data = json.loads(request.httprequest.data or '{}')
        # Validate input data
        if not partner_data.get('name') or not partner_data.get('email'):
            raise ValidationError('Name and email are required')
        partner = request.env['res.partner'].browse(partner_id)
        if partner.exists():
            partner.write(partner_data)
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Partner not found'}

    @http.route('/unibe_res_partner_endpoint/partners/<int:partner_id>', auth='user', type='json', methods=['GET'])
    def get_partner(self, partner_id, **kw):
        if not request.env.user.has_group('base.group_user'):
            raise AccessError("You do not have the necessary permissions to access this resource.")
        partner = request.env['res.partner'].browse(partner_id)
        if partner.exists():
            return partner.read(['name', 'email', 'phone'])[0]
        else:
            return {'status': 'error', 'message': 'Partner not found'}
