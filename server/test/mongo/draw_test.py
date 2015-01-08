from django.test import TestCase
from server.bom.random_number import *
from server.mongodb.driver import *
import django


class SanityMongo(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        django.setup()
        self._driver = MongoDriver.instance()

    def persist_draw_test(self):
        """MongoDB: Persist and retrieve RandomNumberDraw"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        raw = self._driver._draws.find_one({"_id":res_id})
        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in raw.keys())
            self.assertTrue(v == raw[k])
        self._driver._draws.remove({"_id":res_id})

    def raw_retrieve_test(self):
        """MongoDB: Persist and retrieve RandomNumberDraw"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        draw = RandomNumberDraw(**self._driver._draws.find_one({"_id":res_id}))

        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in draw.__dict__.keys())
            self.assertTrue(v == draw.__dict__[k])
        self._driver._draws.remove({"_id":res_id})

    def retrieve_draw_test(self):
        """MongoDB: Retrieves an item using mongodb driver"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        res_id = self._driver.save_draw(tested_item)
        retrieved = self._driver.retrieve_draw(RandomNumberDraw,res_id)

        self.assertIsInstance(retrieved,RandomNumberDraw)
        for k,v in tested_item.__dict__.items():
            self.assertTrue(k in retrieved.__dict__.keys())
            self.assertTrue(v == retrieved.__dict__[k])
        self._driver._draws.remove({"_id":res_id})