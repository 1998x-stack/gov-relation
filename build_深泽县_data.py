#!/usr/bin/env python3
"""深泽县数据构建（根目录别名）—— 委托给 scripts/build/ 下的正式脚本。"""

import os
import runpy


def main():
    canonical = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "scripts", "build", "build_深泽县_data.py")
    runpy.run_path(canonical, run_name="__main__")


if __name__ == "__main__":
    main()
