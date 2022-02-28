from app.models.seconhouse_model import *

from flask import Flask, render_template, request
from pony.flask import Pony

app = Flask(__name__)
Pony(app=app)

PAGE_COUNT = 30


@app.route('/')
@app.route('/secondhouse/')
def homepage():
    args = request.args
    page = 1
    options = {}
    if args.get('page'):
        page = int(args.get('page'))
    if args.get('region_py'):
        options['region_py'] = args.get('region_py')
    if args.get('district_py'):
        options['district_py'] = args.get('region_py')
    offset = PAGE_COUNT * (page - 1)
    s = '%,'.join('%s=%s' % (key, options[key]) for key in options.keys())
    if s:
        sql = 'select house_id,title,community,community_id from guangzhou_secondhouse_common_info where %s limit %s offset %s' % (
        s, PAGE_COUNT, offset)
    else:
        sql = 'select house_id,title,community,community_id from guangzhou_secondhouse_common_info limit %s offset %s' % (
        PAGE_COUNT, offset)
    results = db.execute(sql=sql).fetchall()
    house_list = []
    for house in results:
        house_list.append({
            'house_id': house[0],
            'title': house[1],
            'community': house[2],
            'community_id': house[3],
        })
    print(house_list)
    return render_template('homepage.html', house_list=house_list)


@app.route('/ditiehouse/<string:subway>')
def subway(subway):
    pass


@app.route('/secondhouse/<string:house_id>')
def house_info(house_id):
    common_info = GuangZhouSecondHouseCommonInfo.get(house_id=house_id)
    special_info = GuangZhouSecondHouseSpecialInfo.get(house_id=house_id)
    info = {
        'title': common_info.title,
        'community': common_info.community,
        'community_id': common_info.community_id,
        'pictures': special_info.pictures
    }
    return render_template('secondhouse.html', **info)


@app.route('/community/<string:community_id>')
def community_info(community_id):
    community = GuangZhouCommunityInfo.get(community_id=community_id)
    info = {
        'name': community.name,
        'features': community.features
    }
    return render_template('community.html',**info)


if __name__ == '__main__':
    app.run(debug=True)
