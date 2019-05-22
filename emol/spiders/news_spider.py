import json
import urllib.parse

import scrapy

YEARS = (2016, 2017, 2018, 2019)

COMMENTS_BASE_URL = "https://cache-comentarios.ecn.cl/Comments/Api?action=getComments&url=%s&includePending=true&format=json&limit=0&order=TIME_DESC&rootComment=true"


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        "https://www.emol.com/sitemap/"
    ]

    def parse(self, response):
        years_anchors = response.css("#articles_free")[0].css("a")
        for anchor in years_anchors:
            year = int(anchor.css("::text").get())
            if year in YEARS:
                href = response.urljoin(anchor.attrib["href"])
                yield scrapy.Request(href, callback=self.parse_year)
    
    def parse_year(self, response):
        # Ref.: https://www.emol.com/sitemap/noticias/2016/index.html
        parts_anchors = response.css(".articlesMonth li > a")
        for anchor in parts_anchors:
            href = response.urljoin(anchor.attrib["href"])
            yield scrapy.Request(href, callback=self.parse_part)
    
    def parse_part(self, response):
        # Ref.: https://www.emol.com/sitemap/noticias/2016/emol_noticias_2016_01_0000001.html
        news_anchors = response.css("#mainContent li > a")
        for anchor in news_anchors:
            href = anchor.attrib["href"]
            yield scrapy.Request(href, callback=self.parse_news)
    
    def parse_news(self, response):
        # Ref.: https://www.emol.com/noticias/Espectaculos/2016/01/25/785191/24-Legacy-sera-protagonizada-por-actor-de-The-Walking-Dead-y-Straight-Outta-Compton.html
        title = response.css("#cuDetalle_cuTitular_tituloNoticia::text").get()
        subhead = response.css("#cuDetalle_cuTitular_bajadaNoticia::text").get()
        date, time, agency = [item.strip() for item in response.css(".info-notaemol-porfecha::text").get().split("|")]
        text = " ".join(response.css("#cuDetalle_cuTexto_textoNoticia *::text").getall())

        news = {
            "url": response.url,
            "title": title,
            "subhead": subhead,
            "date": date,
            "time": time,
            "agency": agency,
            "text": text
        }

        href = COMMENTS_BASE_URL % urllib.parse.quote(response.url, safe="")
        request = scrapy.Request(href, callback=self.parse_comments)
        request.meta["news"] = news
        yield request
    
    def parse_comments(self, response):
        json_response = json.loads(response.body_as_unicode())
        news = response.meta["news"]
        news["comments_url"] = response.url
        news["comments"] = json_response["comments"]
        yield news


