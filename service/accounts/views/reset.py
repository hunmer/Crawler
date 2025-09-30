"""
重置所有平台账号的过期状态
"""
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts_manager


async def reset_accounts():
    """
    重置所有平台的所有账号过期状态
    将所有 expired=1 的账号重置为 expired=0

    Returns:
        响应格式: {
            "code": 0,
            "msg": "OK",
            "data": {
                "success": true,
                "affected": {
                    "douyin": 2,
                    "bilibili": 3,
                    "kuaishou": 0,
                    "weibo": 1,
                    "xhs": 0
                }
            }
        }
    """
    try:
        result = await accounts_manager.reset_all_accounts()
        if result['success']:
            return reply(ErrorCode.OK, "All accounts reset successfully", result)
        else:
            return reply(ErrorCode.ERROR, "Some accounts failed to reset", result)
    except Exception as e:
        return reply(ErrorCode.ERROR, f"Failed to reset accounts: {str(e)}", {
            'success': False,
            'affected': {}
        })