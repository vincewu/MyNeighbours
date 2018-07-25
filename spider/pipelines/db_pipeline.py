from spider.item.address import Address


class DB_Pipeline(object):
    def process(self, item, spider):
        if isinstance(item, Address):
            print(item)
        return item
