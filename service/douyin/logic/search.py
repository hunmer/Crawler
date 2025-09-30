from .common import common_request
from typing import Optional

# 缓存 search_id 和对应的 cookie
_search_id_cache: dict[str, str] = {}

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10, params: Optional[dict] = None) -> tuple[dict, bool]:
    """
    请求抖音获取搜索信息

    Args:
        keyword: 搜索关键词
        cookie: 账号 cookie
        offset: 偏移量
        limit: 返回数量
        params: 可选参数对象,可包含 search_id

    Returns:
        tuple[dict, bool]: (响应数据, 是否成功)
    """
    request_params = {
        "keyword": keyword,
        "search_channel": 'aweme_general',
        "search_source": 'normal_search',
        "query_correct_type": '1',
        "is_filter_search": '1',
        "filter_selected": '{"sort_type":"0","publish_time":"0","content_type":"1"}',
        'offset': offset,
        'count': limit
    }

    # 处理 search_id
    if params and 'search_id' in params:
        search_id = params['search_id']
        if search_id:
            request_params['search_id'] = search_id

            # 检查缓存,如果该 search_id 已有记录的 cookie,则使用缓存的 cookie
            if search_id in _search_id_cache:
                cookie = _search_id_cache[search_id]
            else:
                # 缓存当前 search_id 和 cookie 的映射
                _search_id_cache[search_id] = cookie

    headers = {"cookie": cookie}
    resp, succ = await common_request('/aweme/v1/web/general/search/single/', request_params, headers)
    if not succ:
        return resp, succ
    ret = resp.get('data', {})
    return ret, succ
