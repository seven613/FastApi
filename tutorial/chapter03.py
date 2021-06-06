from enum import Enum
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Query
app03 = APIRouter()
# 函数的顺序就是路由的顺序，会优先匹配第一个正确的路径


@app03.get('/path/parameters')
def path_params01(parammeters: str):
    return {'message': parammeters}


@app03.get('/path/{parameters}')
def path_params01(parammeters: str):
    return {'message': '这是路径参数中的parammeters'}

# 使用枚举类型


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get('/enum/{city}')  # 枚举类型参数
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {'city_name': city, 'confirmed': 1433}
    else:
        return{'city_name': city, 'confirmed': 2342}

# 文件路径参数，斜杠的问题


@app03.get('/files/{file_path:path}')
def filepath(file_path: str):
    return f'文件路径是:{file_path}'


@app03.get('/path_/{num}')
def path_params_validate(num: int = Path(None, title="数字参数", description="不可描述", ge=1, le=10)):
    return num


@app03.get('/query')
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return{'page': page, 'limit': limit}
    return {'page': page}


@app03.get('/query/bool/conversion')
def type_conversion(param: bool = False):
    return param


@app03.get('/query/validations')
def query_param_validate(
        value: str = Query(..., min_length=8, max_length=16, regex="^a"),
        values: List[str] = Query(default=['v1', 'v2'], alias="别名")):
    return value, values


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")
    country: str
    country_code: str = None
    country_population: int = Field(
        default=800, title="人口数量", description="国家人口数量")

    class Config:
        schema_extra = {
            "example": {
                "name": "Beijing",
                "country": "China",
                "country_code": "CN",
                "country_population": 14000000
            }
        }


@app03.get('/request_body/city')
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()

@app03.put('/request_body/city/{name}')
def min_city_info(
    name: str,
    city01: CityInfo,
    city02: CityInfo,
    confirmed: int = Query(ge=0, description="确诊数", default=0),
    death: int = Query(ge=0, description="死亡数", default=0)
):
    if name == "Shanghai":
        return{"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()
