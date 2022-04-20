import copy


class GenerateOptions():
    def __init__(self, options):
        self.options = copy.deepcopy(options)

    def init_option(self, options):
        if not options:
            sql_options = ''
        else:
            special_option = self.init_special_option(options=options)
            sql_options = ['%s=%r' % (key, options[key]) for key in options.keys()]
            sql_options = f'{" and ".join(sql_options + special_option) if special_option else " and ".join(sql_options)}'
        return sql_options

    def init_special_option(self, options):
        pass

    def generate(self):
        sql_options = self.init_option(options=self.options)
        # print(sql_options)
        return sql_options


class HouseGenerateOptions(GenerateOptions):
    def init_special_option(self, options):
        special_options = []
        if options.get('total_price'):
            total_price = options.pop('total_price')
            if '-' in total_price:
                price_option = 'total_price between %s and %s' % (
                    total_price.split('-')[0], total_price.split('-')[1][:-1])
            elif '以下' in total_price:
                price_option = 'total_price<%s' % (total_price[:-3])
            else:
                price_option = 'total_price>%s' % (total_price[:-3])
            special_options.append(price_option)
        if options.get('size'):
            size = options.pop('size')
            if '-' in size:
                size_option = 'size between %s and %s' % (size.split('-')[0], size.split('-')[1][:-1])
            elif '以下' in size:
                size_option = 'size<%s' % (size[:-3])
            else:
                size_option = 'size>%s' % (size[:-3])
            special_options.append(size_option)
        if options.get('layout'):
            layout = options.pop('layout')
            if '以上' not in layout:
                layout_option = 'layout like %r' %(f'{layout[:2]}%%')
            else:
                layout_option = ' and '.join('layout not like %r' %(f'{i}室%%') for i in range(5))
            special_options.append(layout_option)

        return special_options
