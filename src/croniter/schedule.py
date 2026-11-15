"""区间展开工具：批量计算 cron 表达式在区间内的触发点。

提供 expand(expr, start, end)，返回带 times / count 的结果，
供调度巡检统计区间触发次数、比对任务撞车。
"""

import datetime as dt
from collections import namedtuple

from croniter import croniter

ExpandResult = namedtuple("ExpandResult", ["times", "count"])


def expand(expr, start, end):
    """展开 expr 在 (start, end] 内的触发点。

    左开右闭：start 本身不计入，end 计入。
    start >= end 时返回空结果。

    返回 ExpandResult：
      times  触发点的秒级时间戳列表（升序）
      count  len(times)
    """
    times = []
    if start < end:
        it = croniter(expr, start)
        while True:
            nxt = it.get_next(dt.datetime)
            if nxt > end:
                break
            times.append(nxt.timestamp())
    return ExpandResult(times=times, count=len(times))
