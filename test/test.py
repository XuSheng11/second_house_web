from app.models.seconhouse_model import *

regions = GuangZhouRegion.select(lambda r: r.district_py == 'huadou' or r.district_py=='nansha')
print(regions)
