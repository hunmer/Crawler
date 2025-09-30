"""
账号统计和管理路由
"""
from . import views
from fastapi import APIRouter

router = APIRouter(prefix='/accounts')

router.add_api_route('/all', views.all_accounts, methods=['GET'])
router.add_api_route('/reset', views.reset_accounts, methods=['POST'])