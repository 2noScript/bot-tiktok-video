import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup
import re
from pydash import uniq,sample,find
import requests
from pprint import pprint


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
    
    def getInfoByVideoId(self,videId):
        videUrl=fr'https://{sample(WATER_MARK)}/aweme/v1/feed/?aweme_id={videId}'
        print(videUrl)
        response =requests.get(videUrl)
        if(response.status_code == 200):
               
            data=find(response.json()['aweme_list'],lambda item:item['aweme_id']==videId)
            if data==None:
                return {} 
            return {
                'videId':videId,
                'desc':data['desc'],
                'videoUrl':data['video']['play_addr']['url_list'],
                'audioUrl':data['music']['play_url']['uri'],
                'cover':data['video']['cover']['url_list']
            }


async def main():
    vd = TikTokVideo()
    result=vd.getInfoByVideoId('6951395225445158146')
    pprint(result)



   
      

asyncio.get_event_loop().run_until_complete(main())
