import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup
import re


class TikTokVideo:
    def __init__(self):
        self.baseUrl='https://www.tiktok.com'

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
        pattern = re.compile(fr'https://www\.tiktok\.com/@{userName}/video/')
        links = soup.find_all('a', href=pattern)
        data=[]
        for link in links:
            match=re.compile(r'(\w+)$').search(link['href'])
            data.append(match.group(1))
        print(data)
        print(len(data))
          
        



async def main():
    vd = TikTokVideo()
    await vd.getVideoIdListByUser('deykayana1')
   
      

asyncio.get_event_loop().run_until_complete(main())
