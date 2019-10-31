import unittest
import invoiced
import responses


class TestCoupon(unittest.TestCase):

    def setUp(self):
        self.client = invoiced.Client('api_key')

    def test_endpoint(self):
        coupon = invoiced.Coupon(self.client, 123)
        self.assertEqual('/coupons/123', coupon.endpoint())

    @responses.activate
    def test_create(self):
        responses.add('POST', 'https://api.invoiced.com/coupons',
                      status=201,
                      json={"id": 123, "name": "Alpha"})

        coupon = invoiced.Coupon(self.client)
        coupon = coupon.create(name="Alpha")

        self.assertIsInstance(coupon, invoiced.Coupon)
        self.assertEqual(coupon.id, 123)
        self.assertEqual(coupon.name, "Alpha")

    @responses.activate
    def test_retrieve(self):
        responses.add('GET', 'https://api.invoiced.com/coupons/123',
                      status=200,
                      json={"id": "123", "name": "Alpha"})

        coupon = invoiced.Coupon(self.client)
        coupon = coupon.retrieve(123)

        self.assertIsInstance(coupon, invoiced.Coupon)
        self.assertEqual(coupon.id, '123')
        self.assertEqual(coupon.name, "Alpha")

    def test_update_no_params(self):
        coupon = invoiced.Coupon(self.client, 123)
        self.assertFalse(coupon.save())

    @responses.activate
    def test_update(self):
        responses.add('PATCH', 'https://api.invoiced.com/coupons/123',
                      status=200,
                      json={"id": 123, "name": 600})

        coupon = invoiced.Coupon(self.client, 123)
        coupon.name = 600
        self.assertTrue(coupon.save())

        self.assertTrue(coupon.name)

    @responses.activate
    def test_list(self):
        responses.add('GET', 'https://api.invoiced.com/coupons',
                      status=200,
                      json=[{"id": 123, "name": "Alpha"}],
                      adding_headers={
                        'x-total-count': '10',
                        'link': '<https://api.invoiced.com/coupons?per_page=25&page=1>; rel="self", <https://api.invoiced.com/coupons?per_page=25&page=1>; rel="first", <https://api.invoiced.com/coupons?per_page=25&page=1>; rel="last"'})  # noqa

        coupon = invoiced.Coupon(self.client)
        coupons, metadata = coupon.list()

        self.assertIsInstance(coupons, list)
        self.assertEqual(len(coupons), 1)
        self.assertEqual(coupons[0].id, 123)

        self.assertIsInstance(metadata, invoiced.List)
        self.assertEqual(metadata.total_count, 10)

    @responses.activate
    def test_delete(self):
        responses.add('DELETE', 'https://api.invoiced.com/coupons/123',
                      status=204)

        coupon = invoiced.Coupon(self.client, 123)
        self.assertTrue(coupon.delete())
