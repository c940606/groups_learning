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

#
a = Solution()
# print(a.leastOpsExpressTarget(7, 99))
# print(a.leastOpsExpressTarget(3, 19))
# print(a.leastOpsExpressTarget(5, 501))
# print(a.leastOpsExpressTarget(2, 2 * (10 ** 8)))
tmp = a.leastOpsExpressTarget(3, 200000000)
print(eval(tmp))


