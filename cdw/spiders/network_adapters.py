import scrapy
from scrapy import Request
from cdw.items import CdwItem
import re
import json
import requests

class NetworkAdaptersSpider(scrapy.Spider):
    name = 'network_adapters'   #Name of the Spider Crawler

    def start_requests(self):

        #to reproduce the body, headers and form parameters of the request

        url = 'https://www.cdw.com/api/product/1/data/GetProductReviewSummary'

        headers = {
            "authority": "www.cdw.com",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/json; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "sec-ch-ua-platform": "\"Linux\"",
            "origin": "https://www.cdw.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.cdw.com/search/networking/network-adapters/?w=RB&pcurrent=1",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ta;q=0.7"
        }

        cookies = {
            "A8A8F83D13EA4F8B917AA5F211762060": "97CE882452A3426499F68CAEAB465E5D",
            "BA9AA5C91598458BA251A10B273627B6": "B8ACFF8D5A3C497C9FF1A697F4003259",
            "dtCookie": "v_4_srv_5_sn_F2265BF3DC7C9BD26C3F842578088120_perc_100000_ol_0_mul_1_app-3A9daca7aae537f807_1_rcs-3Acss_0",
            "bm_sz": "BF5E86DBA8C80B668E8D19ED88FC99F8~YAAQn7csMVxa69yAAQAAMQxCBQ9vR+JqeaHEzxQJMbOD4Jh8maLyfxgNzjNEgrExDAnYcpsPb1P8DvWRdmCgY/ULnzbvu0nwKowZaklHGxpfFEPRVAkaNfTiQWhPNa184rOkdeIQxEQhJJWmV8xiSZT8N/n2xYboZVMn5zQZuKXEcOVgtgFWXt+GM1pTH/4aoPUQtz9za+OGf2CiWsPWUaBs3OkOXXaxDWswHBcXZiw8T8YaqavlSIPxdf0FTZO2/aZTIxlQtA1OpWx/IPO7tSJxDnL361x2Ybqdu5slSWg=~3683141~3159353",
            "rxVisitor": "1653650624062ACP9AIMILN64HAG77F2VP1E8FJ25SC56",
            "newVisitor": "true",
            "optimizelyEndUserId": "oeu1653650624957r0.44828126847676075",
            "_rdt_uuid": "1653650627485.02f1eb98-ec90-41a4-a63c-8c79cb735943",
            "_li_dcdm_c": ".cdw.com",
            "_lc2_fpi": "464f01cb1133--01g42m46xr3n69kdqghdh4zpek",
            "_gcl_au": "1.1.693458203.1653650628",
            "265B10B0AD854F37A02410D8F39E9723": "D9E03756-34B1-4B31-8FD3-89BA0070DA6E",
            "70549A6B29AD46CF90DA19BC17972419": "T-cdNvb9AJCDtHAbfyv2XG2UIS_tgbc9x53lmVUOxtKfDy-1jJaUNxfX9tZivR4vdyTbfqblNepF4QAeAwvaycxZ4541",
            "_abck": "6AC25FDB5352D866CB3CCA843944CE14~0~YAAQn7csMYta69yAAQAAGiNCBQeERb6xujtK9B7DkWxgAwAJSRN1R1w7gZYw4KRZr7pu+WJltO4+Mzd/VJM8BQaNt4zOQiZ/zdK+JjU1zn/SqLdwhMoeFcmaosW8vf9h5oGrDO11AILE+X90aNHqy+X7LWEEVsk76BXK7solkop9SZUN4eXxae+aBi+bn5gDTI1zE58p1h/QM3V/pMU8QQH8fJZ7p6lfGfpNV0EWg0zbThrNYATvTJTHQXvP4yIK3EQUvidqv7QU6H+2aZlRrVaB6pgxZxShYhVsM7LuFTIgfS9SQAyQlvojqUT1PJbC9sgUR8p3a3yF1iTV8Zox4qQtFaEsWfjnE9c1Rg1WJ88SlF/adlx/BKW/iam610/MWQ103OZ+RusFHNLqWaedbt3a9HE=~-1~||-1||~-1",
            "bluecoreNV": "true",
            "AMCVS_6B61EE6A54FA17010A4C98A7%40AdobeOrg": "1",
            "s_cc": "true",
            "_hjSessionUser_540806": "eyJpZCI6IjQwMmU4ZDMwLWQxNmMtNTc5Mi1iMTk2LTE1MTJmODAyOGI3MSIsImNyZWF0ZWQiOjE2NTM2NTA2OTM3NzMsImV4aXN0aW5nIjp0cnVlfQ==",
            "_hjSessionUser_68143": "eyJpZCI6Ijk4MDAxMjk3LWE4ODctNTI0Zi04N2NjLTRkOTdhNmU3MzliMiIsImNyZWF0ZWQiOjE2NTM2NTA2MjkwNDYsImV4aXN0aW5nIjp0cnVlfQ==",
            "B7D99A893A2F4D6EB8C66F2801F35BF6": "True",
            "4112525968F44D5C99DF0BDE0C235561": "_6025231",
            "rr_rcs": "eF5jYSlN9kgzSDUzs0wy1E1LtLTQNTE0S9Q1TzRO0gWKGpgYmqSZJZmlcuWWlWSm8BkZmOoa6hoCAI7-DjM",
            "_hjAbsoluteSessionInProgress": "0",
            "SC_LINKS": "%5B%5BB%5D%5D",
            "s_sq": "%5B%5BB%5D%5D",
            "s_dl": "1",
            "s_dl1": "1",
            "s_dl2": "1",
            "s_dl3": "1",
            "AKA_A2": "A",
            "bm_mi": "6F551EC47FCE9ABA3465BF57EA01EEAC~YAAQn7csMd2F69yAAQAAZWDXBQ9JQ9vc6AQfSZxy3js8+ZS4e5Rqt0C9Qb67UPywT8LgmTPifN4ZjlLDhm9SYY1GbnBde+5T5hKNdcrWg0luaPC+Vn7zu9KTJg5elV2iCCFYzK5wQB2QFHIwJV7eHJaMWeSjlhmsXzVEnPJQuAhnV+9ICzlomZlmRI3lbHLgE9ml5UxeZgkhXdzcPh4R7f/d8Wj+harLnnoGlEaxFKcE2VjmwqdAsiTcpc3VKsY6W5S+1tbpuNZptQMqGvaPSwEQgIg6WiKZal5wRqQOSTh8Vd4imXTzvp39Qch+dAtFUGgUkV4HHsRpTEttMuaKSS2vAcE0Hjfpr9d3GxsJ~1",
            "AMCV_6B61EE6A54FA17010A4C98A7%40AdobeOrg": "1585540135%7CMCMID%7C65591291336208266391752091674266569668%7CMCAAMLH-1654265213%7C12%7CMCAAMB-1654265213%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1653667613s%7CNONE%7CMCSYNCSOP%7C411-19147%7CvVersion%7C4.4.0",
            "s_visit": "1",
            "ak_bmsc": "BB3FC65BCAAE791C73A4F9DE9BF425BB~000000000000000000000000000000~YAAQn7csMUqG69yAAQAAoXTXBQ8t+6lnNZeVRxQ3x0yNxz+hGN+W3nYGE4cH0kUQeAL4ffDhzBgw90XcqnGu7yA+iEVB78+JE66kmesvIq32druNKimV9imw2kUoAMNK8GQ6opwMUcoV+Ckfp2JOL49B9XovidgDeWXQFU6VrZjKlPZAvHqDAPJ937/hZzxISlvbHWknQty01rdR+otC4GDdIm+xASZrWav1Xr71/Mmd2bKUdYS8blqNt1wcNqLmuAU9zUl5s4RQhuQakGaoKzRWmoJ1uBAP0Q2e/b4MbZRudZLHKNv5VkUJuF5B1+aDXtoYsCWZcjR3MhFNJu3eSgoTjnH0/HmaEtWbIImrJZm1KS4vlR8VpoWM4GzmV4sxq2z0xoNd4IbtKVJY0DAD4YW3NyQeLwRnUYR0KKCcU/QfDzrQjiODlUCakjnQ4K40HbG6IDsBAV6ddX8=",
            "bc_invalidateUrlCache_targeting": "1653660416373",
            "_hjIncludedInSessionSample": "0",
            "_hjSession_68143": "eyJpZCI6IjIzMmEyODQ3LTljYTUtNDcxMy1iYWQ1LWM2MDJiMzkwOTdjMSIsImNyZWF0ZWQiOjE2NTM2NjA0MTY1MzcsImluU2FtcGxlIjpmYWxzZX0=",
            "needleopt": "Saant0-usOnly",
            "needlepin": "N190d16536506293700001200816459b01816459b0100000000000000000000000000000000",
            "gpv_pn": "Fusion%20Search%20Results%3A%20Successful%20%28page%201%29-Networking",
            "s_dfa": "cdwglobalstaging%2Ccdwusprod%2Ccdwglobalprod",
            "dtSa": "-",
            "dtLatC": "31",
            "_uetsid": "797bac60ddaf11ecb2c129a2bb8d9c25",
            "_uetvid": "797be470ddaf11ec8f8b3782254b8576",
            "s_ppvl": "Fusion%2520Search%2520Results%253A%2520Successful%2520%2528page%25201%2529-Networking%2C8%2C80%2C7763%2C1294%2C412%2C1366%2C768%2C1%2CL",
            "mp_cdw_mixpanel": "%7B%22distinct_id%22%3A%20%2218105421a21aa-07a12afa413c5b-162d1e0a-100200-18105421a2238f%22%2C%22bc_persist_updated%22%3A%201653650627109%7D",
            "CartKey": "f120d9ec73114e6fa84d4789e2582ca7",
            "s_ppv": "Fusion%2520Search%2520Results%253A%2520Successful%2520%2528page%25201%2529-Networking%2C8%2C80%2C7763%2C1294%2C412%2C1366%2C768%2C1%2CL",
            "utag_main": "v_id:0181054212a90065d701213f95540506800140600086e$_sn:3$_se:6$_ss:0$_st:1653662440276$vapi_domain:cdw.com$dc_visit:3$ses_id:1653660411869%3Bexp-session$_pn:3%3Bexp-session$dcsyncran:1%3Bexp-session$dc_event:6%3Bexp-session$dc_region:ap-east-1%3Bexp-session",
            "rxvt": "1653662441254|1653659573705",
            "RT": "\"z=1&dm=cdw.com&si=75049286-548e-4390-bee5-47fa4a258211&ss=l3oiplb7&sl=1&tt=46d&bcn=%2F%2F684d0d41.akstat.io%2F&ld=4zr1\"",
            "dtPC": "5$60636998_228h-vBTVFGKCWMSPNKPMSHRRMCIDRCSRHCAHH-0e0",
            "bm_sv": "D617A6871B0E35922EF2DADE7CF70853~YAAQn7csMYuK69yAAQAAeujaBQ8+0a7+bkM9c/PsC9YSFmYghDfAqkxKDT08mteJJqAblF90+ZCH/o6cYrPsO46zDSppy9o0yT4EMwegC/ihVcLJKpCncERwBvIihl5DN8oU7529eg8gRuGbv96eaR2235Hhv3x+Vem9LrA7jRKInfC59zX4f2b/I3uPZmXOn8ejR17ZhYA3s8ZM5nrYCjX9CvkSf0N61q++3O+HNoFrO3Sj9xb4gZFcE/P56A==~1",
            "s_ptc": "0.00%5E%5E0.01%5E%5E0.00%5E%5E0.04%5E%5E0.81%5E%5E0.02%5E%5E4.41%5E%5E0.04%5E%5E5.41"
        }

        body = '{"ProductCodes":["3473399","3780527","4754426","4760794","6760906","4476597","4955073","4955068"],"Source":"search_page.json_rr3"}'
        
        for i in range(2,360):
            url = f'https://www.cdw.com/search/networking/network-adapters/?w=RB&pcurrent={i}'
            yield scrapy.Request(url=url, method='POST', cookies=cookies, headers=headers, body=body)

    def parse(self, response):
       
        #Selecting the elements using xpath selector
        blocks = response.xpath("//div[@class='search-result coupon-check']//div[@class='product-specs col-3']")

        for block in blocks:

            url = block.xpath("./h2/a/@href").get()
            url = response.urljoin(url)
            sku = block.xpath("./div[@class='product-codes']/span[@class='mfg-code']//text()").get()
            cdw_part_number = block.xpath("./div[@class='product-codes']/span[@class='cdw-code']//text()").get()
            
            #Storing the scraped data into newly created dictionary 'meta'
            meta = {}
            meta['sku'] = sku
            meta['cdw_part_number'] = cdw_part_number

            yield scrapy.Request(url, callback=self.parse_details, meta=meta)

        next_page = response.xpath("//a[@aria-label='Next Page']").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):

        sku = response.meta['sku']
        cdw_part_number = response.meta['cdw_part_number']

        #Getting the name, categories and base_image from the script tag 
        script = ' '.join(response.xpath("//script[contains(.,'window.cdwTagManagementData')]").getall())
        data = re.findall("window.cdwTagManagementData =(.*);",script)
        data = ' '.join(data).replace("'",'"')
        res = json.loads(data)  #Converting JSON to Dict
        
        name = res.get('product_name')
        categories = res.get('product_category')
        base_image = res.get('product_image')

        price = response.xpath("//div[@class='price']//text()").get()
        
        description = response.xpath("//div[@itemprop='description']//text()").get()

        short_description = response.xpath("//div[@class='quick-tech-spec']").get()

        #Thumb Image
        link = base_image
        link = ' '.join(re.findall('(.*)\?',link))
        lst = ['a','b','c','d','e','f','g','h','i','j']
        thumbnail_image=[]
        for i in lst:
            timage_link = link+i
            resp = requests.get(timage_link, allow_redirects = False)
            if not resp.status_code==403:
                thumbnail_image.append(timage_link)

        #Creating item object and pushing all the extracted data to the fields 
        item = CdwItem()
        item['name'] = name
        item['sku'] = sku
        item['cdw_part_number'] = cdw_part_number
        item['price'] = price
        item['description'] = description
        item['short_description'] = short_description
        item['base_image'] = base_image
        item['thumbnail_image'] = thumbnail_image
        item['categories'] = categories
        yield item