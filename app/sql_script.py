from app.models.seconhouse_model import *


class FetchInfo():
    PAGE_COUNT = 30

    def __init__(self, *args, options, table):
        self.args = args[0]
        self.options = options
        self.table = table

    def init_sql(self, special_option):
        page = 1
        if self.options.get('page'):
            page = int(self.options.pop('page'))
        offset = self.PAGE_COUNT * (page - 1)
        sql_options = '%,'.join('%s=%r' % (key, self.options[key]) for key in self.options.keys())
        if sql_options:
            print(self.args)
            sql = f'select {",".join(self.args)} from {self.table} where {sql_options} {"and "+ special_option if special_option else ""} limit {self.PAGE_COUNT} offset {offset}'
        else:
            sql = f'select {",".join(self.args)} from {self.table} where {special_option if special_option else ""} limit {self.PAGE_COUNT} offset {offset}'
        return sql

    def init_special_option(self):
        pass

    def fetch(self):
        special_option = self.init_special_option()
        sql = self.init_sql(special_option)
        print(sql)
        results = db.execute(sql=sql).fetchall()
        return results


class FetchHouseInfo(FetchInfo):
    def init_special_option(self):
        special_options = []
        if self.options.get('total_price'):
            total_price = self.options.pop('total_price')
            if '-' in total_price:
                price_option = 'total_price between %s and %s' % (
                    total_price.split('-')[0], total_price.split('-')[1][:-1])
            elif '以下' in total_price:
                price_option = 'total_price<%s' % (total_price[:-3])
            else:
                price_option = 'total_price>%s' % (total_price[:-3])
            special_options.append(price_option)
        if self.options.get('size'):
            size = self.options.pop('size')
            if '-' in size:
                size_option = 'size between %s and %s' % (size.split('-')[0], size.split('-')[1][:-1])
            elif '以下' in size:
                size_option = 'size<%s' % (size[:-3])
            else:
                size_option = 'size>%s' % (size[:-3])
            special_options.append(size_option)
        return ' and'.join(special_options)


class FetchCommunityInfo(FetchInfo):
    pass
