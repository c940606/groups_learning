import unittest

from tests.HTMLTestRunner import HTMLTestRunner
from tests.test_solution import TestLeastOperators

if __name__ == '__main__':
    suite = unittest.TestSuite()

    tests = [TestLeastOperators("test_func")]  # 添加测试用例列表
    # 添加一组测试用例
    suite.addTests(tests)
    # 添加一个测试用例
    suite.addTest(TestLeastOperators("test_func"))

    # loadTestsFromName()，传入'模块名.TestCase名'
    # 传入单个
    suite.addTests(unittest.TestLoader().loadTestsFromName("test_solution.TestLeastOperators"))
    # 传入一个列表
    suite.addTests(unittest.TestLoader().loadTestsFromNames(["test_solution.TestLeastOperators"]))

    # loadTestsFromTestCase()，传入TestCase
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLeastOperators))
    #

    # suite中也可以套suite

    # 将测试结果输出到测试报告中
    # with open('UnittestTextReport.txt', 'w', encoding="utf-8") as f:
    #     runner = unittest.TextTestRunner(stream=f, verbosity=2)
    #     runner.run(suite)

    # 将测试结果输出到测试报告html中
    # with open('HTMLReport.html', 'w') as f:
    #     runner = HTMLTestRunner(stream=f,
    #                             title='MathFunc Test Report',
    #                             description='generated by HTMLTestRunner.',
    #                             verbosity=2
    #                             )
    #     runner.run(suite)



    # 直接将结果输出控制台
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)