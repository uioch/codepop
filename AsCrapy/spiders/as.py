import copy
import scrapy
import urllib3

from As.items import AsItem,ASPW

class AsSpider(scrapy.Spider):
    name = 'as'
    allowed_domains = []
    start_urls = ['http://m.as.com/tk/aszsd/']

    headers = {
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, \
                    callback=self.parse, \
                    headers=self.headers, \
                    errback=self.errback)

    def errback(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):
        for qc in response.css('article.list_panel'):
            if not qc.css('ul.tag_panel'):
                self.logger.warn('tag_panel not Found, ignoring')
                continue
            
            item = AsItem()
            item['qc'] = qc.css('top::text').get()
            
            for qt in qc.css('ul.tag_panel i.tag a'):
                item['qt'] = qt.css('::text').get()
                self.logger.warn('##### %s %s %s', \
                    item['qc'], item['qt'], \
                    qt.attrib['href'])
                yield scrapy.Request(qt.attrib['href'], \
                        callback=self.parse_qt, \
                        headers=self.headers, \
                        errback=self.errback, \
                        cb_kwargs={
                            'item' : copy.deepcopy(item),
                        })


    def parse_qt(self, response, item):
        item2 = copy.deepcopy(item)
        for ws in response.css('article.list_panel'):
            for wl in ws.css('ul.news_list li a'):
                item['qurl']  = wl.attrib['href']
                item['qname'] = wl.css('h3::text').get()
                item['pw'] = 'q'
                if type(item['qname']) is not str or len(item['qname']) <= 0:
                    self.logger.warn('ignore: %s', item['qurl'])
                    continue
                
                self.logger.warn('+++++ %s ', str(item))
                yield scrapy.Request(
                        response.urljoin(item['qurl']), \
                        callback=self.parse_wpage, \
                        headers=self.headers, \
                        errback=self.errback, \
                        cb_kwargs={'item':copy.deepcopy(item)})
            
            if ws.css('div.list_page'):
                for wsp in ws.css('div.list_page a'):
                    if wsp.css('::text').get() == '下一页':
                        self.logger.warn('##### %s %s', str(item), \
                            wsp.xpath('@href').get())
                        yield scrapy.Request(
                            response.urljoin(wsp.xpath('@href').get()), \
                            callback=self.parse_qt, \
                            headers=self.headers, \
                            errback=self.errback, \
                            cb_kwargs={'item':item2})

    def parse_wpage(self, response, item):
        c = response.css('article.content_box div.self_content')
        if not c:
            self.logger.warn('ERROR: wcont not found! %s', response.url)
            return
        
        cp = c.css('p')
        p  = None
        for i in range(len(cp)):
            if not cp[i].css('strong'):
                continue
            cps = cp[i].css('strong::text').get()
            if hasattr(cps, 'find') and cps.find(ASPW[item['pw']]) >= 0 and i < (len(cp) - 1):
                p = cp[i+1]
                break

        if not p:
            self.logger.warn('Error wcont not found 2 use all text! %s', response.url)
            p = c
        
        pimg  = p.css('img::attr(src)').getall()
        pimg  = list(set(pimg))
        img_ign = 'https://www.baidu.com/logo.png'
        if img_ign in pimg:
            pimg.remove(img_ign)

        ptext = [x.strip() for x in p.css('::text').getall()]
        pts = ''
        for t in ptext:
            if len(t) <= 0:
                continue
            if t.find('咨询群：') >= 0:
                continue
            if t.find('2020年小学1-6年级期末试题及答案！') >= 0:
                continue
            if t.find('2021小升初绝密资料免费领取') >= 0:
                continue
            if t.find('相关推荐') >= 0:
                continue
            if t.find('点击下一页查看答案') >= 0:
                continue
            if t.find('加群讨论') >= 0:
                continue
            pts += t + '\n'
        
        item[item['pw'] + 'text'] = pts
        item[item['pw'] + 'url'] = response.url
        if type(pimg) is list and len(pimg) > 0:
            item[item['pw'] + 'img'] = pimg
            if 'file_urls' in item:
                item['file_urls'] += pimg
            else:
                item['file_urls'] = pimg
        else:
            item[item['pw'] + 'img'] = ''

        self.logger.warn('@@@@@ %s', str(item))

        has_next_page = False
        for wsp in response.css('article.content_box div.list_page a'):
            wst = wsp.css('::text').get()
            wsh = wsp.xpath('@href').get()
            self.logger.warn('NEXT_PAGE CHECK: (%s)%s (%s)%s', type(wst), wst, type(wsh), wsh)
            if type(wst) is not str or type(wsh) is not str :
                continue
            wsh = wsh.strip()
            wst = wst.strip()
            self.logger.warn('NEXT_PAGE CHECK2: (%s)%s (%s)%s', type(wst), wst, type(wsh), wsh)
            if len(wsh) <= 0:
                continue
            if wst != '下一页':
                continue

            has_next_page = True
            item['pw'] = 'qa'
            yield scrapy.Request(
                response.urljoin(wsp.xpath('@href').get()), \
                callback=self.parse_wpage, \
                headers=self.headers, \
                errback=self.errback, \
                cb_kwargs={'item': item})

        if not has_next_page:
            self.logger.warn('***** %s', str(item))
            yield item
