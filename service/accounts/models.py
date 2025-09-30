"""
账号统计和管理模型
"""
from service.douyin.models import accounts as douyin_accounts
from service.bilibili.models import accounts as bilibili_accounts
from service.kuaishou.models import accounts as kuaishou_accounts
from service.weibo.models import accounts as weibo_accounts
from service.xhs.models import accounts as xhs_accounts


class AccountsManager:
    """账号管理器"""

    def __init__(self):
        self.platforms = {
            'douyin': douyin_accounts,
            'bilibili': bilibili_accounts,
            'kuaishou': kuaishou_accounts,
            'weibo': weibo_accounts,
            'xhs': xhs_accounts,
        }

    async def get_all_counts(self) -> dict:
        """
        获取所有平台的账号数量统计(排除过期账号)

        Returns:
            dict: {'douyin': 3, 'bilibili': 4, ...}
        """
        counts = {}

        for platform, account_model in self.platforms.items():
            try:
                # 获取该平台的所有账号
                all_accounts = await account_model.load()
                # 统计未过期的账号数量 (expired != 1)
                valid_count = sum(1 for acc in all_accounts if acc.get('expired', 0) != 1)
                counts[platform] = valid_count
            except Exception as e:
                # 如果获取失败，记录为0
                counts[platform] = 0

        return counts

    async def reset_all_accounts(self) -> dict:
        """
        重置所有平台的所有账号过期状态
        将所有账号的 expired 设置为 0

        Returns:
            dict: {'success': True/False, 'affected': {'douyin': 2, 'bilibili': 3, ...}}
        """
        affected = {}
        success = True

        for platform, account_model in self.platforms.items():
            try:
                # 获取该平台的所有过期账号
                all_accounts = await account_model.load()
                count = 0

                for account in all_accounts:
                    if account.get('expired', 0) == 1:
                        # 重新保存账号，设置 expired 为 0
                        result = await account_model.save(
                            id=account['id'],
                            cookie=account['cookie'],
                            expired=0
                        )
                        if result:
                            count += 1
                        else:
                            success = False

                affected[platform] = count
            except Exception as e:
                affected[platform] = 0
                success = False

        return {
            'success': success,
            'affected': affected
        }


# 创建单例实例
accounts_manager = AccountsManager()