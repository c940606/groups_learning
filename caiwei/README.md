

# 总结

这次实战学习了很多，主要有以下几个方面：

1. 算法(动态规划)
2. `Python` 单元测试

通过实战过程，把自己的学习过程串起来，总结一下。

##  Python 单元测试 （unittest）

要了解什么是测试驱动开发（TDD），其实和我们平时写代码是一样的：

先写好代码（有bug）→通过`print`大法找bug→修改→`print`→.....，最后使自己的代码健壮。

TDD的流程也是如此：

![](D:\tmp_desktop\中兴工作\image-20200318150641764.png)

TDD三项法则：

1. 在编写失败的单元测试之前，不要编写任何产品代码
2. 只要有一个单元测试失败了，就不再写测试代码；
3. 产品代码能够让当前失败的单元测试成功通过即可，不要多写

`Python`有自带的测试库`unittest`，内置库，简洁易用。对于如下题目：

> 给定两个正整数 `i` 和 `v`，使用 +, -, *, \ 运算符对 `i`进行运算，使得结果为 `v`，要求用到的运算符个数最少。
>
> 约束：
>
> 1. 运算符只支持加、减、乘、除，不支持括号、不支持负号；
> 2. 运算符的优先级走义：乘/除同级；加/减同级；乘/除高于加/减；同级按限从左往右的方式始合；
> 3. `i`位于2到98之间；
> 4. `v`位于1到10的9次方的2倍之间。

示例：

```
    输入：i = 7， v = 99
    输出：7 * 7 + 7 * 7 + 7/7
```

思路：

**动态规划**

首先，这个问题一定有解，大不了我们一直用`x/x = 1`加到目标值。

其次，因为要最少运算符，所以尽量使用乘法，快速增长到目标值附近。

最后，到目标值附近，有三种可能（假如通过乘法到底目标值附近的值为`cur`）：

1. `cur  =  target`，这种情况直接输出即可；
2. `cur  >  target`，比如`cur  =  4，target  =  3, x  =  2`，这时候需要使用减法(比如`4 - 2/2 `)，只需找到能求得`cur - target`的最小运算符是什么即可；
3. `cur < target`，比如`cur  =  3, target  =  7, x  =  3`，这时候需要使用加法，只需找到`target - cur`最小运算符是什么即可。

但是，当`target < x`时候，比如`target = 2, x = 3`，我们有两种方法到达目标值，一种是`3/3 + 3/3`；一种是`3- 3/3`，换句话说，一种全是用`1`相加，一种先用`x`再减`1`，判断谁用操作符最少。

所以，我们可以用带记忆法递归求的解，代码如下，并将文件存储成`least_operators.py`

```python
class Solution:
    def leastOpsExpressTarget(self, x: int, target: int) -> int:
        from functools import lru_cache
        import math

        @lru_cache(None)
        def dfs(cur):
            # 当cur < x, 比如 cur = 2, x = 3, 需要判断使用 3/3 + 3/3 和 3 - 3/3,哪个用运算符最少
            if cur < x:
                tmp1 = (str(x) + "/" + str(x) + "+") * cur
                tmp2 = str(x) + ("-" + str(x) + "/" + str(x)) * (x - cur)
                return min(tmp1[:-1], tmp2, key=lambda s: sum(a in {"+", "-", "*", "/"} for a in s))
            if cur == 0:
                return ""
            # 到cur 需要几个x相乘,
            p = int(math.log(cur, x))
            sums = x ** p
            # cur < sums 的情况,就是要加
            t = (str(x) + "*") * p
            ans = t[:-1] + "+" + dfs(cur - sums)
            # sums > cur, 就是要减去多少才能到底目标值, 这个判断条件是有严格的数学证明的
            if sums * x - cur < cur:
                ans = min(ans, t + str(x) + "-" + dfs(sums * x - cur).translate(str.maketrans("+-", "-+")),
                          key=lambda s: sum(a in {"+", "-", "*", "/"} for a in s))
            return ans if ans[-1] not in {"+", "-"} else ans[:-1]

        return dfs(target)

```

我们要对上面的代码，有如下需要几方面测试：

1. 输出结果是否有非 `+, -,  *, /`和数字的运算符；
2. 是否满足预期结果，即求出的字符串是否等于`v`。

下面，通过测试上面的代码学习`unittest`库。

## TestCase测试用例

```python
import unittest
from ddt import ddt, data, unpack
from caiwei.least_operators import Solution

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
    @unittest.skip("想临时跳过这个测试用例") # 5 
    def test_illgal_character(self, i, v):
        """
        1. 可能会出现非 + - * / 数字的字符
        2. 可能出现 +2+2 , -2+2, 2+2-, 2+2+, 2+2*, 2+2/ 类似这样不合法的字符串
        """
        print("测试非法字符")
        self.skipTest("跳过这个测试用例") # 6
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

    @data((2, 10))
    @unpack
    def test_expected_results(self, i, v):
        print("测试预期结果")
        result = eval(self.a.leastOpsExpressTarget(i, v))
        self.assertEqual(result, v, msg="预期结果错误")
    
    def test_func(self):
        print("测试函数")
        
    


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

注意:

1. 一个`class`继承了`unittest.TestCase`，便是一个测试用例；
2. 在每一个测试用例中在代码中 `1, 2, 3, 4 `位置，重写以下函数：
   `setUp()`该测试用例执行前的设置工作、
   `tearDown()`该测试用例执行后的清理工作、
   `setUpClass()`所有测试用例前的设置工作、
   `tearDownClass()`所有测试用例执行后的清洗工作；
3. 每一个测试用例中可以通过`skip，skipIf，skipUnless`装饰器跳过某个测试函数，或者用`TestCase.skipTest`方法跳过测试函数，代码 `5, 6` 所示；
4. 每个测试方法均以` test `开头，否则是不被`unittest`识别的。每一个test开头的方法都会加载为独立的测试用例。执行顺序按函数名字典排序顺序依次执行；
5. 在`unittest.main()`中加 `verbosity` 参数可以控制输出的错误报告的详细程度，默认是` 1`，如果设为 `0`，则不输出每一用例的执行结果。如果参数为2则表示输出详细结果。

暂时忽略`from ddt import ddt, data, unpack`，这是数据驱动库，后面会介绍。当然上面两个测试可以写在一起，但是为了学习方便，拆成两个。



## TestSuite测试组

**TestSuite用来控制多个测试用例和多个测试文件之间的测试顺序。**(默认顺序是按函数名字典排序顺序依次执行)，在`Pycharm` 最好另起一个文件写，要不很麻烦。

```python
import unittest

from caiwei.tests import HTMLTestRunner
from caiwei.tests.test_solution import TestLeastOperators

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
```

注意：

1. 多种方法将多个测试用例打包，一起测试

2. 测试报告，可以打印`txt`, `html`和输出控制台。其中html的输出需要加载HTMLTestRunner.py模块

   链接：https://pan.baidu.com/s/1vxzf47JjDZsr0LJbvAa4rw 
   提取码：ca7e 
   复制这段内容后打开百度网盘手机App，操作更方便哦



## ddt数据驱动 

**当我们想对一个功能使用多次测试数据时候**，这时候使用`DDT`来完成，DDT是 “Data-Driven Tests”的缩写。

> #### dd.ddt：
>
> 装饰类，也就是继承自TestCase的类。
>
> #### ddt.data：
>
> 装饰测试方法。参数是一系列的值。
>
> #### ddt.file_data：
>
> 装饰测试方法。参数是文件名。文件可以是`json` 或者 `yaml`类型。
>
> 注意，如果文件以`”.yml”`或者`”.yaml”`结尾，ddt会作为`yaml`类型处理，其他所有文件都会作为`json`文件处理。
>
> 如果文件中是列表，每个列表的值会作为测试用例参数，同时作为测试用例方法名后缀显示。
>
> 如果文件中是字典，字典的key会作为测试用例方法的后缀显示，字典的值会作为测试用例参数。
>
> #### ddt.unpack：
>
> 传递的是复杂的数据结构时使用。比如使用元组或者列表，添加unpack之后，ddt会自动把元组或者列表对应到多个参数上。
>

直接举个用例子说明：

```python
import unittest
from ddt import ddt, data, unpack
from caiwei.least_operators import Solution


@ddt # 1
class TestLeastOperators(unittest.TestCase):

    @data((2, 10), (3, 10)) # 2 测试两组数据
    @unpack # 3 相当于把第一组数据[2, 10]分别传参给i, v
    def test_expected_results(self, i, v, correct):
        print("测试预期结果")
        result = eval(self.a.leastOpsExpressTarget(i, v))
        self.assertEqual(result, v, msg="预期结果错误") # 测试预期结果

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

注意：

1. 代码1处装饰类，也就是继承自TestCase的类。

2. 代码2处采用@ddt进行装饰，测试方法上装饰@data()，data可以是数值，也可以是字符串。测试方法后会被ddt加一个后缀，ddt会尝试把测试数据转化为后缀附在测试方法后，组成一个新的名字。

   data 可以传入列表，元组和字典都可以;

3. 代码3就是解包，分别传参了到相应参数。

我们还可以直接传入`json`或者`yaml`文件，这里我们只用`json`举例子，新建一个文件`test_data.json`

```json
[
  {
    "i": 7,
    "v":99
  },
  {
    "i": 3,
    "v":19
  },
  {
    "i": 5,
    "v":501
  },
  {
    "i": 3,
    "v":20000000
  }
]
```

`file_data`的用法学习

```python
import unittest
from ddt import ddt, file_data
from mathfunc import multi

@ddt  # 1
class TestMathFunc(unittest.TestCase):

    @file_data("test_data.json")
    def test_expected_results(self, i, v):
        print("测试预期结果")
        result = eval(self.a.leastOpsExpressTarget(i, v))
        self.assertEqual(result, v, msg="预期结果错误") # 测试预期结果
```



## 最后

这次学到很多，代码不仅仅只是实现功能，还有考虑代码的鲁棒性，健壮性，这就需要通过测试才行。

以上代码，GitHub地址：https://github.com/c940606/learning/tree/master



参考链接：

1. https://zhuanlan.zhihu.com/p/29968920
2. https://blog.csdn.net/luanpeng825485697/article/details/79459771
3. https://www.cnblogs.com/miniren/p/7099187.html