import unittest

from ddt import ddt, data, unpack,file_data

from least_operators import Solution


# 一个class继承了unittest.TestCase，便是一个测试用例
@ddt
class TestLeastOperators(unittest.TestCase):

    # TestCase基类方法,所有case执行之前自动执行
    @classmethod
    def setUpClass(cls) -> None:  # 1
        print("这里是所有测试用例前的准备工作")

    # TestCase基类方法,所有case执行之后自动执行
    @classmethod
    def tearDownClass(cls) -> None:  # 2
        print("这里是所有测试用例后的清理工作")

    # TestCase基类方法,每次执行case前自动执行
    def setUp(self) -> None:  # 3
        print("这里是一个测试用例前的准备工作")
        self.a = Solution()  # 创建对象

    # TestCase基类方法,每次执行case后自动执行
    def tearDown(self) -> None:  # 4
        print("这里是一个测试用例后的准备工作")
        del self.a

    @data((2, 10))
    @unpack
    @unittest.skip("想临时跳过这个测试用例")  # 5
    def test_illgal_character(self, i, v):
        """
        1. 可能会出现非 + - * / 数字的字符
        2. 可能出现 +2+2 , -2+2, 2+2-, 2+2+, 2+2*, 2+2/ 类似这样不合法的字符串
        """
        print("测试非法字符")
        self.skipTest("跳过这个测试用例")  # 6
        s = self.a.leastOpsExpressTarget(i, v)
        opt = {"+", "-", "*", "/"}

        def helper(s):
            # 1. 为空
            if not s: return False
            # 首尾位置出现不合法字符
            if s[0] in opt or s[-1] in opt: return False
            # 遍历字符是否出现不合法字符
            for a in s:
                if not (a.isdigit() or a in opt):
                    return False
            return True

        self.assertTrue(helper(s), msg="给到结果的字符串不合法")

    # @data((2, 10), (3, 10))
    # @unpack
    @file_data("test_data.json")
    def test_expected_results(self, i, v):
        print("测试预期结果")
        result = eval(self.a.leastOpsExpressTarget(i, v))
        self.assertEqual(result, v, msg="预期结果错误")

    def test_func(self):
        print("测试函数")

#
if __name__ == '__main__':
    unittest.main(verbosity=2)
