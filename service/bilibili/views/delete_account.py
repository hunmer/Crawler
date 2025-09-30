from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from pydantic import BaseModel

class Param(BaseModel):
    id: str

async def delete_account(param: Param):
    '''
    删除B站账号
    '''
    await accounts.delete(param.id)
    return reply(ErrorCode.OK, "OK", None)