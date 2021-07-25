import scrapy
import json
import functools
from scrapy import Request


class CoindeskSpider(scrapy.Spider):
    name = 'coindesk'
    allowed_domains = ['coindesk.com']
    page = 0
    download_delay = 0
    start_urls =  [
        'https://www.coindesk.com/wp-json/v1/articles/category/tech/0?mode=list',
        ]

    #URL format examples:
    #https://www.coindesk.com/wp-json/v1/articles/format/opinion/0?mode=list
    #https://www.coindesk.com/wp-json/v1/articles/category/markets/0?mode=list
    #https://www.coindesk.com/wp-json/v1/articles/tag/stablecoins/0?mode=list





    def parse(self, response):
        data = json.loads(response.text)
        posts = data["posts"]
        for article in posts:

            article_url = 'https://www.coindesk.com/' + article['slug']    
            full_name = article["authors"][0]['name']
            author_page_url = 'https://www.coindesk.com/author/' + article["authors"][0]['slug']
            article_title = article['title']
            article_description = article['text'],
            category= article['category']['name']
            tag = article['tag']['name']
            date = article['date']

            yield Request(author_page_url, callback=self.second_page,  dont_filter=True, meta={

                'Article_URL': article_url,
                'Full_Name': full_name,
                'Author_Page_URL': author_page_url,
                'Article_Title': article_title,  
                'Article_Description': article_description,
                'Category': category,
                'Tag': tag,
                'Date': date

                 })



        if data["next"]:  #increments the page by a value of '1' if it contains the word 'next'
            self.page += 1 #{self.page}
            url = f'https://www.coindesk.com/wp-json/v1/articles/category/tech/{self.page}?mode=list' #this URL will need to be changed as well if you change start_urls
            yield scrapy.Request(url=url, callback=self.parse)



    def second_page(self, response):

        article_url = response.meta.get('Article_URL')
        full_name = response.meta.get('Full_Name')
        author_page_url = response.meta.get('Author_Page_URL')
        article_title = response.meta.get('Article_Title')
        article_description = response.meta.get('Article_Description')   
        category = response.meta.get('Category')
        tag = response.meta.get('Tag')
        date = response.meta.get('Date')
        email = response.css('a[href*=mailto]::attr(href)').get().replace('mailto:', '')
        bio = response.xpath('/html/body/div/div[2]/main/section/div[1]/div/div/div[2]/div[2]/div/div/text()').get()
        
    


        yield Request(article_url, callback=self.third_page,  dont_filter=True, meta={

                'Article_URL': article_url,
                'Full_Name': full_name,
                'Author_Page_URL': author_page_url,
                'Article_Title': article_title,  
                'Article_Description': article_description,
                'Category': category,
                'Tag': tag,
                'Date': date,
                'Email': email,
                'Author_Bio': bio,

                 })


    def third_page(self, response):

        article_url = response.meta.get('Article_URL')
        full_name = response.meta.get('Full_Name')
        author_page_url = response.meta.get('Author_Page_URL')
        article_title = response.meta.get('Article_Title')
        article_description = response.meta.get('Article_Description')   
        category = response.meta.get('Category')
        tag = response.meta.get('Tag')
        date = response.meta.get('Date')
        email = response.meta.get('Email')
        bio = response.meta.get('Author_Bio')
        content  = response.css('div.article-pharagraph > p::text').getall() or response.css('div.classic-body > p::text').getall() or response.css('div.classic-body > p > span::text').getall() or response.css('div.classic-body > div > p::text').getall() or response.css('div.classic-body > p > span::text').getall()
        "".join(content)
        list = response.css('li::text').getall() or response.css('div.classic-body > ul > li > span::text').getall() or response.css('div.article-pharagraph > ul > li > span::text').getall() or  response.css('div.classic-body > ul  > li > span::text').getall()
        "".join(list)



        yield {
                'Full_Name': full_name,  
                'Author_Page_URL': author_page_url,
                'Email': email,
                'Author_Bio': bio,
                'Article_Title': article_title,
                'Article_URL': article_url,
                'Article_Description': article_description,
                'Category': category,
                'Tag': tag,
                'Date': date,
                'Article_Content': content,
                'Article_Lists': list,
                
        }