EMAIL = 'ijazkhan095@gmail.com'
PASSWORD = '#####'

def download_file(url,name):
    local_filename = name
    headers = {}
    if os.path.exists(local_filename):
        headers = {'Range': 'bytes=%d-' % (os.path.getsize(local_filename))}
        print("[>] Resuming Video")
    with get(url, stream=True,headers=headers) as r:
        if not r and headers:
            print("[+] Video Already Downloaded")
            return
        total_size = int(r.headers.get('content-length', 0))
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        r.raise_for_status()
        with open(local_filename, 'ab') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                t.update(len(chunk))
                if chunk: 
                    f.write(chunk)
        t.close()
        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")

from requests import get,post
from tqdm import tqdm
import json,os,slug
def login():

    headers = {
    'authority': 'craigs-school-3964.thinkific.com',
    'cache-control': 'max-age=0',
    'origin': 'https://craigs-school-3964.thinkific.com',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'referer': 'https://craigs-school-3964.thinkific.com/users/sign_in',
    'accept-language': 'en-US,en;q=0.9',
}
    data = [
      ('utf8', '✓'),
      ('authenticity_token', 'FSWXtPnCr63xutzxpr9jx4Jp1W8GGP5xQqjwOJRUzZ5i50hJaM1fSKCOtPx6adXNgJO5d9YGQn9Ma093e94lqQ=='),
      ('user[email]', EMAIL),
      ('user[password]', PASSWORD),
      ('user[remember_me]', '1'),
    ]

    response = post('https://craigs-school-3964.thinkific.com/users/sign_in',allow_redirects=False, headers=headers, data=data)
    print(response.headers)
    return dict(response.cookies)
headers = {
    'authority': 'craigs-school-3964.thinkific.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

cookies = login()
print(cookies)
import json
exit()
js = json.load(open('response.json'))
if not os.path.exists('Advance SEO Course'):
    os.mkdir('Advance SEO Course')
chaps = {}
for chap in js['chapters']:
    chaps[chap['id']] = chap['name']
contents = {}
for cont in js['contents']:
    if contents.get(chaps[cont['chapter_id']]):
        contents[chaps[cont['chapter_id']]].append(cont['contentable_id'])
    else:
        contents[chaps[cont['chapter_id']]] = [cont['contentable_id']]
for chap in chaps.values():
    if not os.path.exists(os.path.join('Advance SEO Course',slug.slug(chap))):
        os.mkdir(os.path.join('Advance SEO Course',slug.slug(chap)))
    print(chap)
    for lesson in contents[chap]:
        r = get(f'https://craigs-school-3964.thinkific.com/api/course_player/v2/lessons/{lesson}',headers=headers,cookies=cookies)
        if r.json().get('videos'):
            for video in r.json().get('videos'):
                download_file('Advance SEO Course',video['url'],os.path.join(chap,video['url'].split('/')[-1]))
