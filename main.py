from httpx import AsyncClient
import asyncio
from parsel import Selector

keywords = '%20'.join(input("Enter keywords to search: ").split())
print("\n")

client = AsyncClient(
    http2 = True,
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br"
    }, 
    timeout = 100
)

def parse_response(response):
    selector = Selector(response.text)
    internships = selector.xpath("//div[@class = 'container-fluid individual_internship view_detail_button  visibilityTrackerItem ']")

    for internship in internships:
        title = internship.xpath(".//h3[@class = 'job-internship-name']//text()").get()
        formatted_title = ' '.join(str(title).split())

        company = internship.xpath(".//p[@class = 'company-name']//text()").get()
        formatted_company = ' '.join(str(company).split())

        location = internship.xpath(".//div//div[2]//div[1]//div[1]//span//a//text()").get()

        stipend = internship.xpath(".//span[@class = 'stipend']//text()").get()

        duration = internship.xpath(".//div/div[2]/div[1]/div[2]/span/text()").get()
        
        time_posted = internship.xpath("./div/div[2]/div[2]/div[1]/div/span/text()").get()

        link = "https://internshala.com/" + internship.xpath(".//@data-href").get()

        print(f"""Internship: {formatted_title}
Company: {formatted_company}
Stipend: {stipend}
Location: {location}
Duration: {duration}
Link: {link}
Posted: {time_posted}\n\n""")

async def scraper():
    base_url = f"https://internshala.com/internships/keywords-{keywords}"
    for page_num in range(1, 10):
        url = base_url + f'/page-{page_num}/'
        response = await client.get(url)
        parse_response(response)

asyncio.run(scraper())
