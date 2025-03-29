from odoo.tests.common import HttpCase, tagged
import logging

_logger = logging.getLogger(__name__)

@tagged('post_install', 'at_install', 'unibe')
class TestResPartnerEndpoints(HttpCase):

    def setUp(self):
        super(TestResPartnerEndpoints, self).setUp()
        self.partner_model = self.env['res.partner']
        self.test_partner = self.partner_model.create({
            'name': 'Test Partner',
            'email': 'test@example.com',
        })
        _logger.info('Setup complete with test partner created: %s', self.test_partner)

    def test_endpoint_get_partner(self):
        _logger.info('Testing GET partner endpoint')
        response = self.url_open('/api/partner/%s' % self.test_partner.id)
        _logger.info('Response status code: %s', response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Partner', response.text)
        _logger.info('GET partner endpoint test passed')

    def test_endpoint_create_partner(self):
        _logger.info('Testing CREATE partner endpoint')
        response = self.url_open('/api/partner', data={
            'name': 'New Partner',
            'email': 'new@example.com',
        }, method='POST')
        _logger.info('Response status code: %s', response.status_code)
        self.assertEqual(response.status_code, 200)
        new_partner = self.partner_model.search([('email', '=', 'new@example.com')])
        self.assertTrue(new_partner)
        _logger.info('CREATE partner endpoint test passed')

    def test_sql_injection(self):
        _logger.info('Testing SQL injection protection')
        response = self.url_open('/api/partner?name=" OR 1=1 --')
        _logger.info('Response status code: %s', response.status_code)
        self.assertNotEqual(response.status_code, 200)
        _logger.info('SQL injection protection test passed')

    def test_xss_attack(self):
        _logger.info('Testing XSS attack protection')
        response = self.url_open('/api/partner', data={
            'name': '<script>alert("XSS")</script>',
            'email': 'xss@example.com',
        }, method='POST')
        _logger.info('Response text: %s', response.text)
        self.assertNotIn('<script>', response.text)
        _logger.info('XSS attack protection test passed')

    def test_csrf_protection(self):
        _logger.info('Testing CSRF protection')
        response = self.url_open('/api/partner', data={
            'name': 'CSRF Test',
            'email': 'csrf@example.com',
        }, method='POST', headers={'X-CSRFToken': 'invalid_token'})
        _logger.info('Response status code: %s', response.status_code)
        self.assertEqual(response.status_code, 403)
        _logger.info('CSRF protection test passed')
