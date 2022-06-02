import requests,json,random
from bs4 import BeautifulSoup

query = "Model Media"
limit = int(10)
#https://spankbang.com/s/model+media/?p=m
r = requests.get(f"https://spankbang.com/s/{query}?p=m").text
soup = BeautifulSoup(r, 'lxml')
seedata = []
for item in soup.find_all('div', class_='video-item')[0:limit]:
    try:
        full_video = item.find("a", class_='thumb')['href']
    except:
        print(f'No videos found for: {query}')
    if "/category/" in full_video:
        continue
    title = full_video.split('/')[3].replace('+', ' ')
    vvid = full_video.split("/")[1]
    prev = item.picture.img
    try:
        prev_vid = prev['data-preview']
        image = prev['data-src']
    except:
        prev_vid = "Not Found"
        image = "Not Found"
    seedata.append({
        "SPTitle": title,
        "PreviewVideo": prev_vid,
        "Thumbnail": image,
        "urlPP": "https://pnck-ytdl.herokuapp.com/api/info?url=https://spankbang.com/"+vvid+"/embed/"
    })
    
SExsa = random.choice(seedata)
urlsp = requests.get(SExsa['urlPP'])
text = urlsp.text
datapX = json.loads(text)
playMP4 = []
for mp4play in datapX['info']['formats']:
    if mp4play['url'].startswith("https://vdownload"):
        playMP4.append(mp4play['url'])
        
print(playMP4[-1],SExsa['SPTitle'],SExsa['PreviewVideo'],SExsa['Thumbnail'])
    # print(
    #     f"""
    #     Title: {title}
    #     Thumbnail: {image}
    #     PreviewVideo: {prev_vid}
    #     InfoVideo: https://pnck-ytdl.herokuapp.com/api/info?url=https://spankbang.com/{vvid}/embed
    #     Play: https://pnck-ytdl.herokuapp.com/api/play?url=https://spankbang.com/{vvid}/embed/
    #     """
    # )