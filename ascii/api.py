from urllib import request, parse
import re
import json
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def search(keywords, max_results=1):
    url = 'https://duckduckgo.com/'
    params = parse.urlencode({'q': keywords}).encode()

    logger.debug("Hitting DuckDuckGo for Token");

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    req = request.Request(
        url,
        data=params,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    
    res = request.urlopen(req, timeout=10)
    res_text = res.read().decode('utf-8')
    searchObj = re.search(r'vqd=([\d-]+)\&', res_text, re.M|re.I)


    if not searchObj:
        logger.error("Token Parsing Failed !");
        return -1;

    logger.debug("Obtained Token");

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = {
        'l': 'us-en',
        'o': 'json',
        'q': keywords,
        'vqd': searchObj.group(1),
        'f': ',,,',
        'p': '1',
        'kp': '-2',
        'v7exp': 'a'
    }

    params = parse.urlencode(params).encode()

    requestUrl = url + "i.js"

    logger.debug("Hitting Url : %s", requestUrl)

    check = 0

    while True:
        while True:
            try:
                req = request.Request(
                    requestUrl,
                    data=params,
                    headers=headers
                )
                res = request.urlopen(req, timeout=10)
                data = json.loads(res.read().decode('utf-8'))
                break
            except ValueError as e:
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl)
                time.sleep(5)                
                continue
        logger.debug("Hitting Url Success : %s", requestUrl)
        check += download(data["results"],max_results-check)
        if check >= max_results or "next" not in data:
            logger.debug("No Next Page - Exiting")
            print("------------------------------------------------------------------------------")
            logger.debug("Downloaded %d Images", check)
            break
        print("-----------------------------------Next Page----------------------------------")

        requestUrl = url + data["next"];

def printJson(objs):
    for obj in objs:
        # print("Width {0}, Height {1}".format(obj["width"], obj["height"]))
        # print("Thumbnail {0}".format(obj["thumbnail"]))
        # print("Url {0}".format(obj["url"]))
        # print("Title {0}".format(obj["title"].encode('utf-8')))
        print("------")
        print("Image: {0}".format(obj["image"]))
        

def download(objs,max_results):
    n=0
    # if len(objs)>=max_results:
    #     objs = objs[:max_results]

    for obj in objs:
        if(n >= max_results):
            break
        try:
            # response = request.urlretrieve(obj["image"],"./inputs/nft_input"+str(n)+".jpg", "wb")
            # if(response.content == None):
            #     continue
            # file = open("./inputs/nft_input"+str(n)+".jpg", "wb")
            # file.write(response.content)
            # file.close()
            request.urlretrieve(obj["image"],"./inputs/nft_input"+str(n)+".jpg")
            print("-----------------\n")
            print("Downloaded "+str(n+1)+" Image: {0}".format(obj["image"]))
            print("\n-----------------")
            n+=1
        except Exception as e:
            print("-----------------")
            print("Image Download Failed: {0}".format(obj["image"]))
            print("Error: {0}".format(e))
            print("-----------------")
    return n

# search("cat",10)