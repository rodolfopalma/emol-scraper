# EMOL scraper (WIP)

Scraper para las noticias publicadas por EMOL entre los años 2016 y 2019, ambos incluidos. Se seleccionó esta ventana de tiempo debido a que antes de esos años la funcionalidad de comentarios no se encuentra implementada.

Para ejecutar el scraper: `scrapy crawl news -o news.jl`

Se genera el archivo `news.jl`. Cada línea de este archivo corresponde a un objeto JSON con la información perteneciente a una noticia.