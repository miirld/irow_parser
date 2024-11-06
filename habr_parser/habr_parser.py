from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse
import json

base_url = "https://habr.com/en/search/page{}/?q=wcag&target_type=posts&order=relevance"
data = []
article_num = 0 

for page_num in range(1, 6):
    url = base_url.format(page_num)
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    
    articles = bs.find_all("article", class_="tm-articles-list__item")
    
    for article in articles:
        article_num += 1

        title_tag = article.find("a", class_="tm-title__link")
        title = title_tag.text.strip() if title_tag else "No title"

        author_tag = article.find("a", class_="tm-user-info__username")
        author = author_tag.text.strip() if author_tag else "No author"
        
        link = urllib.parse.urljoin("https://habr.com", title_tag["href"]) if title_tag else "No link"

        annotation_tag = article.find("div", class_="article-formatted-body")
        annotation = annotation_tag.text.strip() if annotation_tag else "No annotation" 
        
        data.append({"number":article_num, "title": title, "author": author, "link": link, "annotation": annotation})


with open("./habr_parser/articles.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
