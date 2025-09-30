"""
获取所有平台账号数量统计
"""
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts_manager


async def all_accounts():
    """
    获取所有平台的账号数量统计(排除过期账号)

    Returns:
        响应格式: {
            "code": 0,
            "msg": "OK",
            "data": {
                "douyin": 3,
                "bilibili": 4,
                "kuaishou": 0,
                "weibo": 2,
                "xhs": 1
            }
        }
    """
    try:
        counts = await accounts_manager.get_all_counts()
        return reply(ErrorCode.OK, "OK", counts)
    except Exception as e:
        return reply(ErrorCode.ERROR, f"Failed to get accounts count: {str(e)}", {})