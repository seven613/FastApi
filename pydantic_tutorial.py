from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# 创建一个用户数据模型类


class User(BaseModel):
    id: int  # 没有默认值的是必填字段
    name: str = "John Snow"  # 有默认值，选填
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


# 数据
external_data = {
    "id": 123,
    "signup_ts": "2021-06-03 21:40",
    "friends": [1, 2, "3"]
}
# 使用python的解包将数据做解析验证
user = User(**external_data)
# 可以使用数据了
print(user.name,user.friends,user.signup_ts)
print(user.dict())