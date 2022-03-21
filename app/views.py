from app.models.seconhouse_model import *
from app import app
from app.sql_script import HouseGenerateOptions

from flask import render_template, request


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def get_ico():
    return app.send_static_file('img/favicon.ico')


@app.route('/secondhouse/')
def homepage():
    top = []
    for t in select(h for h in GuangZhouSecondHouseCommonInfo).order_by(
            desc(GuangZhouSecondHouseCommonInfo.total_price)).limit(3):
        top.append({
            'house_id': t.house_id,
            'title': t.title,
            'total_price': t.total_price
        })
    options = dict(request.args)

    page = 1
    if options.get('page'):
        page = int(options.pop('page'))
    sql_class = HouseGenerateOptions(options=options)
    sql_options = sql_class.generate()

    if sql_options:
        nums = select(h for h in GuangZhouSecondHouseCommonInfo).where(raw_sql(sql_options)).count()
        results = select(h for h in GuangZhouSecondHouseCommonInfo).where(raw_sql(sql_options)).page(pagenum=page,
                                                                                                     pagesize=20)
    else:
        nums = 92010
        results = select(h for h in GuangZhouSecondHouseCommonInfo).page(pagenum=page, pagesize=20)

    options['label'] = 'district'
    if options.get('district_cn'):
        district_cn = options.get('district_cn')
        options['regions'] = []
        for region in select(r for r in GuangZhouRegion if r.district_cn == district_cn):
            options['regions'].append(region.region_cn)
    if options.get('subway_id'):
        subway = options.get('subway_id')
        options['label'] = 'subway'
        options['stations_name'] = []
        options['stations_id'] = []
        for station in select(s for s in GuangZhouSubwayStation if s.subway_id == subway):
            options['stations_name'].append(station.name)
            options['stations_id'].append(station.id)
        print(options)
    subway = []
    for s in select(s for s in GuangZhouSubway):
        subway.append({
            'id': s.id,
            'name': s.name
        })
    house_list = []
    for house in results:
        house_list.append({
            'house_id': house.house_id,
            'total_price': house.total_price,
            'unit_price': house.unit_price,
            'title': house.title,
            'cover': house.cover,
            'community': house.community,
            'community_id': house.community_id,
            'layout': house.layout,
            'region_cn': house.region_cn,
            'district_cn': house.district_cn,
            'size': house.size
        })
    print(options)
    return render_template('homepage.html', top=top, nums=nums, house_list=house_list, options=options, subway=subway)


@app.route('/secondhouse/<string:house_id>')
def house_info(house_id):
    common_info = GuangZhouSecondHouseCommonInfo.get(house_id=house_id)
    special_info = GuangZhouSecondHouseSpecialInfo.get(house_id=house_id)
    subway_info = {}
    if common_info.station_id:
        station = GuangZhouSubwayStation.get(id=common_info.station_id).name
        subway = GuangZhouSubway.get(id=common_info.subway_id).name
        subway_info['subway_dis'] = f'近{subway}{station}'
        subway_info['subway_id'] = common_info.subway_id
        subway_info['station_id'] = common_info.station_id

    recommend = []
    for r in select(h for h in GuangZhouSecondHouseCommonInfo).where(community_id=common_info.community_id).random(4):
        recommend.append({
            'house_id': r.house_id,
            'cover': r.cover,
            'title': r.title,
            'size': r.size,
            'layout': r.layout,
            'total_price': r.total_price,
            'unit_price': r.unit_price
        })

    top = []
    for r in select(h for h in GuangZhouSecondHouseCommonInfo).where(community_id=common_info.community_id).order_by(
            desc(GuangZhouSecondHouseCommonInfo.total_price)).limit(4):
        top.append({
            'house_id': r.house_id,
            'cover': r.cover,
            'title': r.title,
            'size': r.size,
            'layout': r.layout,
            'total_price': r.total_price,
            'unit_price': r.unit_price
        })

    info = {
        'region': common_info.region_cn,
        'district': common_info.district_cn,
        'subway': subway_info,
        'title': common_info.title,
        'total_price': common_info.total_price,
        'unit_price': common_info.unit_price,
        'layout': common_info.layout,
        'direction': common_info.direction,
        'size': common_info.size,
        'floor_height': common_info.floor_height,
        'floor_num': common_info.floor_num,
        'renovation': common_info.renovation,
        'year': common_info.year,
        'type': common_info.type,
        'community': common_info.community,
        'community_id': common_info.community_id,
        'base': special_info.base,
        'features': special_info.features,
        'trade': special_info.trade,
        'pictures': special_info.pictures,
        'layout_detail': special_info.layout_detail,
        'recommend': recommend,
        'top': top
    }
    print(info)
    return render_template('secondhouse.html', **info)


@app.route('/community/')
def community_page():
    top = []
    for t in select(h for h in GuangZhouCommunityInfo).order_by(desc(GuangZhouCommunityInfo.unit_price)).limit(3):
        top.append({
            'id': t.community_id,
            'name': t.name,
            'unit_price': t.unit_price
        })

    options = dict(request.args)
    page = 1
    if options.get('page'):
        page = int(options.pop('page'))
    sql_class = HouseGenerateOptions(options=options)
    sql_options = sql_class.generate()

    if sql_options:
        nums = select(h for h in GuangZhouCommunityInfo).where(raw_sql(sql_options)).count()
        results = select(h for h in GuangZhouCommunityInfo).where(raw_sql(sql_options)).page(pagenum=page,
                                                                                             pagesize=20)
    else:
        nums = 5473
        results = select(h for h in GuangZhouCommunityInfo).page(pagenum=page, pagesize=20)

    if options.get('district_cn'):
        district_cn = options.get('district_cn')
        options['regions'] = []
        for region in select(r for r in GuangZhouRegion if r.district_cn == district_cn):
            options['regions'].append(region.region_cn)

    community_list = []
    for community in results:
        address = community.address.split(')')[1]
        if community.pictures:
            cover = community.pictures[0]
        else:
            cover = ''
        community_list.append({
            'community_id': community.community_id,
            'name': community.name,
            'region_cn': community.region_cn,
            'district_cn': community.district_cn,
            'unit_price': community.unit_price,
            'address': address,
            'year': community.features['建筑年代'],
            'cover': cover
        })
    print(options)
    return render_template('community.html', top=top, community_list=community_list, nums=nums, options=options)


@app.route('/community/<string:community_id>')
def community_info(community_id):
    community = GuangZhouCommunityInfo.get(community_id=community_id)
    recommend = []
    for r in select(h for h in GuangZhouSecondHouseCommonInfo).where(community_id=community.community_id).random(4):
        recommend.append({
            'house_id': r.house_id,
            'cover': r.cover,
            'title': r.title,
            'size': r.size,
            'layout': r.layout,
            'total_price': r.total_price,
        })
    info = {
        'name': community.name,
        'address': community.address,
        'district': community.district_cn,
        'region': community.region_cn,
        'unit_price': community.unit_price,
        'pictures': community.pictures,
        'features': community.features,
        'recommend': recommend

    }
    return render_template('community_info.html', **info)


@app.route('/search/')
def search():
    options = dict(request.args)
    page = 1
    if options.get('page'):
        page = int(options.pop('page'))
    if options['type'] == 'house':
        sql_options = 'title like %r or community like %r' % (f'%%{options["keyword"]}%%', f'%%{options["keyword"]}%%')
        print(sql_options)
        nums = select(h for h in GuangZhouSecondHouseCommonInfo).where(raw_sql(sql_options)).count()
        results = select(h for h in GuangZhouSecondHouseCommonInfo).where(raw_sql(sql_options)).page(pagenum=page,
                                                                                                     pagesize=20)
        house_list = []
        for house in results:
            house_list.append({
                'house_id': house.house_id,
                'total_price': house.total_price,
                'unit_price': house.unit_price,
                'title': house.title,
                'cover': house.cover,
                'community': house.community,
                'community_id': house.community_id,
                'layout': house.layout,
                'region_cn': house.region_cn,
                'district_cn': house.district_cn,
                'size': house.size
            })
        return render_template('search.html', house_list=house_list, options=options, nums=nums)
    if options['type'] == 'community':
        sql_options = 'name like %r or address like %r' % (f'%%{options["keyword"]}%%', f'%%{options["keyword"]}%%')
        nums = select(h for h in GuangZhouCommunityInfo).where(raw_sql(sql_options)).count()
        results = select(h for h in GuangZhouCommunityInfo).where(raw_sql(sql_options)).page(pagenum=page, pagesize=20)
        community_list = []
        for community in results:
            address = community.address.split(')')[1]
            if community.pictures:
                cover = community.pictures[0]
            else:
                cover = ''
            community_list.append({
                'community_id': community.community_id,
                'name': community.name,
                'region_cn': community.region_cn,
                'district_cn': community.district_cn,
                'unit_price': community.unit_price,
                'address': address,
                'year': community.features['建筑年代'],
                'cover': cover
            })
        return render_template('search.html', community_list=community_list, options=options, nums=nums)
