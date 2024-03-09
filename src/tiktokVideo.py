import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup
import re
from pydash import uniq,sample

from constants import WATER_MARK,BASE_URL


class TikTokVideo:
    def __init__(self):
        self.baseUrl=BASE_URL

    async def getContextByUser(self,userName):
        url=f'{self.baseUrl}/@{userName}'
        browser = await launch(headless=True)
        page = await browser.newPage()
        await stealth(page) 
        await page.goto(url,waitUntil='networkidle2')
        content =await page.content()
        await browser.close()
        return content
    
    async def getVideoIdListByUser(self,userName):
        content=await self.getContextByUser(userName)
        soup = BeautifulSoup(content, 'html.parser')
        pattern = re.compile(fr'{self.baseUrl}/@{userName}/video/')  # check match is video url
        links = soup.find_all('a', href=pattern)
        data=[]
        for link in links:
            match=re.compile(r'(\w+)$').search(link['href'])
            data.append(match.group(1))
        return uniq(data)
    
    def getUrlWaterMark(self,videId):
        return f'https://{sample(WATER_MARK)}/aweme/v1/feed/?aweme_id={videId}'
    

          
        



async def main():
    vd = TikTokVideo()
    print(vd.getUrlWaterMark('6951395225445158146'))


   
      

asyncio.get_event_loop().run_until_complete(main())
