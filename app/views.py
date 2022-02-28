from app.models.seconhouse_model import *
from app import app
from app.sql_script import FetchHouseInfo

from flask import render_template,request

PAGE_COUNT = 30


@app.route('/')
@app.route('/secondhouse/')
def homepage():
    table = 'guangzhou_secondhouse_common_info'
    options = dict(request.args)
    fetch_class = FetchHouseInfo(['house_id','title','community','community_id'],options=options,table=table)
    results = fetch_class.fetch()
    house_list = []
    for house in results:
        house_list.append({
            'house_id': house[0],
            'title': house[1],
            'community': house[2],
            'community_id': house[3],
        })
    return render_template('homepage.html', house_list=house_list)


@app.route('/secondhouse/<string:house_id>')
def house_info(house_id):
    common_info = GuangZhouSecondHouseCommonInfo.get(house_id=house_id)
    special_info = GuangZhouSecondHouseSpecialInfo.get(house_id=house_id)
    info = {
        'title': common_info.title,
        'community': common_info.community,
        'community_id': common_info.community_id,
        'features': special_info.features,
        'trade': special_info.trade,
        'pictures': special_info.pictures
    }
    return render_template('secondhouse.html', **info)

@app.route('/community/')
def community_page():
    table = 'guangzhou_community_info'
    options = dict(request.args)
    results = fetch(['community_id','name','region_cn','district_cn'],options=options,table=table)
    communitys = []
    for house in results:
        communitys.append({
            'house_id': house[0],
            'name': house[1],
            'region_cn': house[2],
            'district_cn': house[3],
        })
    return render_template('homepage.html', communitys=communitys)


@app.route('/community/<string:community_id>')
def community_info(community_id):
    community = GuangZhouCommunityInfo.get(community_id=community_id)
    info = {
        'name': community.name,
        'address': community.address,
        'pictures': community.pictures,
        'features': community.features
    }
    return render_template('community.html', **info)
