from config import MYSQL_SETTINGS

from pony.orm import *

db = Database()
db.bind(
    provider='mysql',
    host=MYSQL_SETTINGS['host'],
    port=MYSQL_SETTINGS['port'],
    user=MYSQL_SETTINGS['user'],
    passwd=MYSQL_SETTINGS['password'],
    db=MYSQL_SETTINGS['database']
)
set_sql_debug(debug=False)


# 广州区域表
class GuangZhouRegion(db.Entity):
    _table_ = 'guangzhou_region'
    region_py = Required(str)
    region_cn = Required(str)
    district_py = Required(str)
    PrimaryKey(region_py, district_py)


# 广州地铁站表
class GuangZhouSubwayStation(db.Entity):
    _table_ = 'guangzhou_subway_station'
    id = PrimaryKey(str)
    name = Required(str)
    subway_id = Required(str)


# 广州二手房普通信息表
class GuangZhouSecondHouseCommonInfo(db.Entity):
    _table_ = 'guangzhou_secondhouse_common_info'
    house_id = PrimaryKey(str)
    title = Required(str)
    cover = Optional(str, nullable=True)
    type = Required(str)
    direction = Optional(str, nullable=True)
    elevator = Optional(str, nullable=True)
    floor_num = Optional(int, nullable=True)
    floor_height = Optional(str, nullable=True)
    community = Required(str)
    community_id = Required(str)
    layout = Required(str)
    total_price = Optional(int, nullable=True)
    unit_price = Optional(int, nullable=True)
    renovation = Optional(str, nullable=True)
    size = Optional(float, nullable=True)
    year = Optional(int, nullable=True)
    district_cn = Required(str)
    region_cn = Required(str)
    station_id = Optional(str, nullable=True)
    subway_id = Optional(str, nullable=True)

    @classmethod
    @db_session
    def find_many(cls, **kwargs) -> list:
        """
        根据查询条件查询多个实例对象
        :param kwargs: 查询条件
        :return:
        """
        print(kwargs)
        handler = select(x for x in cls)
        """注意handler的链式调用"""
        for name, val in kwargs.items():
            handler = handler.where(lambda x: getattr(x, name=name) == val)
        result = [x.to_dict() for x in handler]
        return result


# 广州二手房特殊信息表
class GuangZhouSecondHouseSpecialInfo(db.Entity):
    _table_ = 'guangzhou_secondhouse_special_info'
    house_id = PrimaryKey(str)
    features = Optional(Json, nullable=True)
    layout_detail = Optional(Json, nullable=True)
    pictures = Optional(Json, nullable=True)
    trade = Optional(Json, nullable=True)
    base = Optional(Json, nullable=True)


# 广州二手房小区信息表
class GuangZhouCommunityInfo(db.Entity):
    _table_ = 'guangzhou_community_info'
    community_id = PrimaryKey(str)
    name = Required(str)
    address = Required(str)
    district_cn = Required(str)
    region_cn = Required(str)
    unit_price = Optional(str, nullable=True)
    features = Optional(Json, nullable=True)
    pictures = Optional(Json, nullable=True)

# 映射到数据库，不直接建表
db.generate_mapping(create_tables=False)
