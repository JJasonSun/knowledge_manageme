import sys
import os

# Add the parent directory to sys.path so we can import app
# Since this file is in tests/, we need to go up one level
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import test_connection

print("正在测试数据库连接 (MySQL + PostgreSQL)...")
success = test_connection()

# test_connection 现在如果 MySQL 工作正常则返回 True（向后兼容）
# 但它会打印两个数据库的状态。
# 我们可以手动检查输出或依赖函数逻辑。

if success:
    print("主数据库测试通过！")
else:
    print("主数据库测试失败！")
    sys.exit(1)
