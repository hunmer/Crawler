from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_search
import random

async def search(keyword: str, offset: int = 0, limit: int = 10, search_id: str = None):
    """
    获取视频搜索

    Args:
        keyword: 搜索关键词
        offset: 偏移量
        limit: 返回数量
        session_id: 可选的搜索会话ID,用于保持搜索上下文
    """
    # 调试日志:打印接收到的所有参数
    logger.info(f'search view received params - keyword: {keyword}, offset: {offset}, limit: {limit}, search_id: {search_id}')

    # 构建 params 字典,转换为底层需要的 search_id
    params = {}
    if search_id:
        params['search_id'] = search_id

    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_search(keyword, account.get('cookie', ''), offset, limit, params if params else None)
        if res == {} or not succ:
            logger.error(f'search failed, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}')
            continue
        logger.info(f'search success, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'search failed, keyword: {keyword}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')