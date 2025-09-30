"""
测试删除账号接口
"""
import asyncio
from data.driver import CommonAccount

async def test_delete_account():
    # 创建测试数据库
    test_db = CommonAccount("data/test_delete.db")
    
    print("1. 添加测试账号...")
    await test_db.save("test_user_1", "test_cookie_1", 0)
    await test_db.save("test_user_2", "test_cookie_2", 0)
    
    print("2. 查看账号列表...")
    accounts = await test_db.load()
    print(f"当前账号数: {len(accounts)}")
    for acc in accounts:
        print(f"  - ID: {acc['id']}, Expired: {acc['expired']}")
    
    print("\n3. 删除账号 test_user_1...")
    result = await test_db.delete("test_user_1")
    print(f"删除结果: {result}")
    
    print("\n4. 再次查看账号列表...")
    accounts = await test_db.load()
    print(f"当前账号数: {len(accounts)}")
    for acc in accounts:
        print(f"  - ID: {acc['id']}, Expired: {acc['expired']}")
    
    print("\n5. 清理测试数据...")
    await test_db.delete("test_user_2")
    
    print("\n✅ 测试完成!")

if __name__ == '__main__':
    asyncio.run(test_delete_account())
