# 删除账号接口文档

## 概述
为 Crawler 项目的所有平台添加了删除账号功能,支持永久删除指定账号。

## 修改内容

### 1. 数据层 (data/driver.py)
在 `CommonAccount` 类中新增 `delete` 方法:
```python
async def delete(self, id: str) -> bool:
    """永久删除指定账号"""
    async with self._get_connection() as conn:
        try:
            sql = f'DELETE FROM {self.table_name} WHERE id = ?'
            await conn.execute(sql, (id,))
            await conn.commit()
            return True
        except Exception as e:
            logger.error(f'failed to delete account, error: {e}')
            await conn.rollback()
            return False
```

### 2. 视图层
为每个平台创建 `delete_account.py` 视图文件:
- `service/xhs/views/delete_account.py` - 小红书
- `service/douyin/views/delete_account.py` - 抖音
- `service/kuaishou/views/delete_account.py` - 快手
- `service/weibo/views/delete_account.py` - 微博
- `service/bilibili/views/delete_account.py` - B站

### 3. 路由注册
在每个平台的 `urls.py` 中添加路由:
```python
router.add_api_route('/delete_account', views.delete_account, methods=['POST'])
```

## API 接口

### 请求格式
- **方法**: POST
- **路径**: `/{platform}/delete_account`
- **Content-Type**: application/json

### 请求参数
```json
{
  "id": "账号ID"
}
```

### 响应格式
```json
{
  "code": 0,
  "message": "OK",
  "data": null
}
```

## 使用示例

### 删除小红书账号
```bash
curl -X POST http://localhost:8080/xhs/delete_account \
  -H "Content-Type: application/json" \
  -d '{"id": "user123"}'
```

### 删除抖音账号
```bash
curl -X POST http://localhost:8080/douyin/delete_account \
  -H "Content-Type: application/json" \
  -d '{"id": "user456"}'
```

### 删除快手账号
```bash
curl -X POST http://localhost:8080/kuaishou/delete_account \
  -H "Content-Type: application/json" \
  -d '{"id": "user789"}'
```

### 删除微博账号
```bash
curl -X POST http://localhost:8080/weibo/delete_account \
  -H "Content-Type: application/json" \
  -d '{"id": "user101"}'
```

### 删除B站账号
```bash
curl -X POST http://localhost:8080/bilibili/delete_account \
  -H "Content-Type: application/json" \
  -d '{"id": "user202"}'
```

## 注意事项
1. 删除操作是永久性的,无法恢复
2. 删除账号会从数据库中完全移除该记录
3. 与 `expire_account` 接口不同,`delete_account` 会物理删除数据
4. 建议在删除前进行确认提示

## 测试
运行测试脚本验证功能:
```bash
cd i:/programing/python/Crawler
python test_delete_account.py
```
