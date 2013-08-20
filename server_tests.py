import os
import server
import unittest
import tempfile

class server_test_case(unittest.testCase):
    def setup(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        server.init_db()
    def tear_down(self):

