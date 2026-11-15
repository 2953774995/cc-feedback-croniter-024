#!/usr/bin/env python3
"""区间内 cron 触发点批量展开验收探针。

契约：
  from croniter.schedule import expand
  res = expand("*/5 * * * *", start, end)
  res.times   区间内的秒级时间戳列表（含 start 之后、end 之前）
  res.count   len(times)
"""

import sys
import datetime as dt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

FAILED = 0
PASSED = 0


def check(code, desc, fn):
    global FAILED, PASSED
    try:
        fn()
        print(f"[PASS] {code} {desc}")
        PASSED += 1
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {code} {desc}")
        print(f"        {type(exc).__name__}: {exc}")
        FAILED += 1


def main():
    try:
        from croniter.schedule import expand  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] P0 导入 croniter.schedule 失败：{type(exc).__name__}: {exc}")
        print("-" * 60)
        print("探针汇总：0/5 通过")
        return 1

    START = dt.datetime(2024, 1, 1, 0, 0)
    END = dt.datetime(2024, 1, 1, 1, 0)

    def p1():
        res = expand("*/5 * * * *", START, END)
        assert res.count == 12, res.count

    def p2():
        res = expand("*/5 * * * *", START, END)
        assert all(isinstance(x, (int, float)) for x in res.times), res.times[:2]

    def p3():
        res = expand("0 * * * *", START, END)
        assert res.count == 1, res.count

    def p4():
        res = expand("*/5 * * * *", START, START)
        assert res.count == 0, res.count

    def p5():
        from croniter import croniter
        it = croniter("*/5 * * * *", START)
        assert it.get_next(dt.datetime) == dt.datetime(2024, 1, 1, 0, 5)

    check("P1", "整点区间内次数", p1)
    check("P2", "返回时间戳列表", p2)
    check("P3", "每小时一次", p3)
    check("P4", "空区间", p4)
    check("P5", "既有 croniter 不变", p5)

    print("-" * 60)
    print(f"探针汇总：{PASSED}/{PASSED + FAILED} 通过")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
