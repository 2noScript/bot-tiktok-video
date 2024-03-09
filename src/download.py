import requests

class Download:

    def  downloadMp3(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print({
                'message':'error',
                'url':url
            })
    
    def  downloadMp4(self,url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
        else:
            print({
                'message':'error',
                'url':url
            })
    
