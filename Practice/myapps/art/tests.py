from django.test import TestCase
import log_
import logging

# Create your tests here.
class TestLogger(TestCase):
    def testLog(self):
        self.assertEqual('1', '1')
        logging.info('测试 1=1 成功!', extra={'username': 'kyra'})

    def testErrorLog(self):
        try:
            self.assertEqual('1', '2')
            logging.info('测试 1=2 成功!', extra={'username': 'kyra'})
        except:
            logging.error('测试 1=2 失败!', extra={'username': 'kyra'})


    def testDjangoLog(self):
        self.assertIn(1, [1,2,3])
        logging.getLogger('mdjango').info('1在[1,2,3]中,测试成功')