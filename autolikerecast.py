import requests
import json
import random
import time
import re


from collections import Counter
import json

import time
timestamp_milidetik_now = int(time.time() * 1000)
from datetime import datetime
waktuNow = datetime.fromtimestamp(timestamp_milidetik_now / 1000)
print("Jam waktu:", waktuNow.strftime("%Y-%m-%d %H:%M:%S"))

try :
    with open('conf.txt', 'r') as file:
      content = file.readline()
      tokenBarier=content.replace('\n', '')
      content = file.readline()
      myUname=content.replace('\n', '')
      print("get fid",myUname)
      print("get barier",tokenBarier)
except Exception as e:
  print("Terjadi pengecualian:", str(e))
  sys.exit()

from urllib.parse import urlparse


threshold = 1000 
urlGetFollowers = "https://client.warpcast.com/v2/followers?fid={}&limit={}"
urlGetFollowings = "https://client.warpcast.com/v2/following?fid={}&limit={}"
urlGetFollowerCount = "https://client.warpcast.com/v2/profile-casts?fid={}&limit=1"
#https://client.warpcast.com/v2/user-thread-casts?castHashPrefix=0xa8fba659&username=safiudinzz&limit=16
urlGetCastByHash = "https://client.warpcast.com/v2/user-thread-casts?castHashPrefix={}&username={}&limit=15"
urlRecast= "https://client.warpcast.com/v2/recasts"
urlLike= "https://client.warpcast.com/v2/cast-likes"
urlFollow = "https://client.warpcast.com/v2/follows"
urlCast = "https://client.warpcast.com/v2/casts"
urlGetProfile = "https://client.warpcast.com/v2/user-by-username?username={}"
urlGetListCast = "https://client.warpcast.com/v2/casts?fid={}&limit={}"
urlGetListProfCast = "https://client.warpcast.com/v2/profile-casts?fid={}&limit={}"
urlGetCastLikes = "https://client.warpcast.com/v2/cast-likes?castHash={}&limit={}"
urlGetCastRecasters = "https://client.warpcast.com/v2/cast-recasters?castHash={}&limit={}"


word = "Great post! Thanks for sharing.|Really interesting perspective. Appreciate you putting this out there.|This is very insightful. Keep up the good work!|I enjoyed reading this. Thanks for posting!|Thanks for the information. Very helpful!|Loved this! Keep it coming.|Wonderful content as always.|This really made me think. Thanks for sharing.|Fantastic read! Looking forward to more posts like this.|Informative and well-written. Great job!|This was very enlightening. Thank you!|Your insights are always appreciated.|Well said! I couldn't agree more.|This is exactly what I needed to read today.|Thank you for sharing your knowledge.|Always enjoy reading your posts. Keep them coming!|This is a great addition to the conversation.|You always provide such valuable content.|Thanks for the inspiration!|This is an excellent piece. Well done!|Informative and engaging as always.|This post really resonated with me. Thank you.|I appreciate your perspective on this topic.|Great content! Very thought-provoking.|You have a unique way of presenting information. Keep it up!|This is a refreshing take. Thanks for sharing.|Loved the insights you provided here.|Thanks for breaking this down so clearly.|Your posts are always a great read.|Excellent points made in this post.|I always learn something new from your posts.|Thanks for providing such valuable information.|This is a must-read. Thanks for sharing!|Your posts are consistently top-notch.|Really enjoyed this. Thanks for posting!|This is very well articulated. Kudos!|Great explanation. Very helpful.|You have a great way of explaining things.|This is so well written. Great job!|I appreciate the depth of your insights.|Impressive growth!|Well played in the crypto market!|Incredible progress in the crypto space!|Fantastic results in the crypto world!|Great strides in the crypto industry!|Awesome performance in the crypto sector!|Amazing achievement in the cryptocurrency realm!|Brilliant success in the digital currency market!|Outstanding gains in the crypto market!|Superb advancement in the blockchain world!|bring me to the moon!!|marveolus project sir!"
myFid="239815" 
sentences = word.split("|")

def setupRequest(METHODE,URL,HEADERS,PAYLOAD):
    time.sleep(1)
    return json.loads(requests.request(METHODE, URL, headers=HEADERS, data=PAYLOAD).text.replace('\n', ''))
payload = {}
headers = {
  'authority': 'client.warpcast.com',
  'accept': '*/*',
  'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
  'authorization': tokenBarier,
  'content-type': 'application/json; charset=utf-8',
  'fc-amplitude-device-id': 'RHcQ1GzjH-9qsvlnMlVriG',
  'fc-amplitude-session-id': '1707233061257',
  'if-none-match': 'W/"J+6FScokLa8cs2EWfP+Ka3mLI0A="',
  'origin': 'https://warpcast.com',
  'referer': 'https://warpcast.com/',
  'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

def is_link(text):
    parsed_url = text
    if parsed_url.scheme and parsed_url.netloc:
        return True
    else:
        return False


def getListUserByFid(myFid,isGetFollowing=False):
    getFollowerCount = setupRequest("GET", urlGetFollowerCount.format(myFid), headers, payload)
    fidUser = getFollowerCount["result"]["casts"][0]["author"]["displayName"]
    getFollowerCount = getFollowerCount["result"]["casts"][0]["author"]["followerCount"]
    print("jumlah follower {}".format(fidUser),getFollowerCount)
    resp = setupRequest("GET", urlGetFollowers.format(myFid,str(getFollowerCount)), headers, payload)
    if isGetFollowing :
       resp = setupRequest("GET", urlGetFollowings.format(myFid,1000), headers, payload)
    return resp["result"]["users"]
    
def extract_urls(text):
    # Define the regular expression for URLs
    url_regex = r'(https?://[^\s]+)'
    # Find all matches in the text
    urls = re.findall(url_regex, text)
    return urls

def doBatchLike(mode,myLink):
    file_path = "list-cast.txt"
    count = 0
    listNotLike = []
    if myUname != "imposteruck" :
        doForAuthor()
    # likers = checkMyLiker(myLink)

    with open(file_path, "r", encoding="utf8") as file:
        content = file.read()
        urls = extract_urls(content)
        for line in urls:
            print(">> ",line.strip())
            random_sentence = random.choice(sentences)+"🎭"

            #  # Bagi baris menjadi bagian berdasarkan spasi
            # parts = line.split()
            # print(parts,len(parts))
            # # Cek apakah bagian kedua adalah URL
            # if len(parts) >= 3 and parts[2].startswith("http"):
            #     print(parts[2])
            #     line = parts[2]
            # else :
            #     continue

            urls = re.findall(r'(https?://\S+)', line.strip())
            if len(urls) < 1 :
                continue
            line = urls[0]

            parsed_url = urlparse(line)
            if not is_link(parsed_url):
                continue
            path_parts = parsed_url.path.split("/")
            username = path_parts[1]
            identifier = path_parts[2]
            identifier = identifier[:10]
            print("Username:", username)
            if username == myUname :
                print("akun lu sendiri mang")
                continue

            if username == "imposteruck" and myUname != "imposteruck" :
                print("author gak minta tip, cuman minta recast comment otomatis ketika menjumpai link raid author 🥰")
                mode="12"
            # if username not in likers :
            #     listNotLike.append(username)
            print("Identifier:", identifier)
            getHash = setupRequest("GET",urlGetCastByHash.format(identifier,username),headers,payload)
            for hash in getHash['result']['casts'] :
                isRecasted = hash["viewerContext"]["recast"]
                isReacted = hash["viewerContext"]["reacted"]
                hash = hash['hash']
                if identifier not in hash:
                    continue
                print("\n//////////////////////////////////////////////////")
                print("target",hash)
                headers['authorization'] = tokenBarier
                payload_hash = json.dumps({"castHash": hash})
                count+=1
                if not isReacted and "1" in mode:
                    time.sleep(17)
                    response = requests.request("PUT", urlLike, headers=headers, data=payload_hash)
                    print("[",count,"] like resp >",response.text)
                if not isRecasted and "2" in mode:
                    time.sleep(17)
                    response = requests.request("PUT", urlRecast, headers=headers, data=payload_hash)
                    print("[-] recast resp >",response.text)
                    payload_hash = json.dumps({"text": random_sentence,"parent":{"hash":hash},"embeds":[]})
                    time.sleep(17)
                    response = requests.request("POST", urlCast, headers=headers, data=payload_hash)
                    print("[-] comment resp >",response.text)
                print("//////////////////////////////////////////////////\n")
                mode="1"
    print("Total Task",count)
    print("Not like",listNotLike,"Total Not like",len(listNotLike))

def doLike(fid,limitCast):
    getListCast = setupRequest("GET", urlGetListProfCast.format(fid,limitCast), headers, payload)
    for cast in getListCast['result']['casts']:
        hash = cast['hash']
        isReacted = cast["viewerContext"]["reacted"]
        print("\n//////////////////////////////////////////////////")
        print("target",hash)
        payload_hash = json.dumps({"castHash": hash})
        if not isReacted :
            time.sleep(18)
            response = requests.request("PUT", urlLike, headers=headers, data=payload_hash)
            print(">> like resp",response.text)
        print("//////////////////////////////////////////////////\n")

def doRecastComment(fid,limitCast):
    getListCast = setupRequest("GET", urlGetListProfCast.format(fid,limitCast), headers, payload)
    for cast in getListCast['result']['casts']:
        random_sentence = random.choice(sentences)+"🎭"
        hash = cast['hash']
        isRecasted = cast["viewerContext"]["recast"]
        print("\n//////////////////////////////////////////////////")
        print("target",hash)
        payload_hash = json.dumps({"castHash": hash})
        if not isRecasted :
            time.sleep(18)
            response = requests.request("PUT", urlRecast, headers=headers, data=payload_hash)
            print(">> recast resp",response.text)
            payload_hash = json.dumps({"text": random_sentence,"parent":{"hash":hash},"embeds":[]})
            time.sleep(18)
            response = requests.request("POST", urlCast, headers=headers, data=payload_hash)
            print(">> comment resp",response.text)
            print("//////////////////////////////////////////////////\n")

        
def doFollow(user):
    isFollowing = user["viewerContext"]["following"]
    isFollowedBy = user["viewerContext"]["followedBy"]

    if not isFollowing and isFollowedBy :
        print("you didn't follow",user["displayName"])
        payload = json.dumps({"targetFid": user["fid"]})
        response = requests.request("PUT", urlFollow, headers=headers, data=payload)
        print(response.text)
    elif isFollowing and isFollowedBy :
        print("you're mutual",user["displayName"])

def doBackToOtherUser():
    post = []
    getListCast = setupRequest("GET", urlGetListProfCast.format(239815,5), headers, payload)
    for cast in getListCast['result']['casts']:
        hash = cast['hash']
        getListLiker = setupRequest("GET",urlGetCastLikes.format(hash,100),headers,payload)
        fidLiker = []
        for liker in getListLiker['result']['likes']:
            # if not int(timestamp_milidetik_last_run) < (liker['timestamp']):
                # print(liker['timestamp'],"Setelah",timestamp_milidetik_last_run)
                fidLiker.append(liker['reactor']['fid'])
                doFollow(liker['reactor'])
        getListRecaster = setupRequest("GET",urlGetCastRecasters.format(hash,100),headers,payload)
        
        fidRecaster = []
        for recaster in getListRecaster['result']['users']:
            fidRecaster.append(recaster['fid'])
            doFollow(recaster)
        post.append([fidLiker,fidRecaster])
    flatten_data = [item for sublist in post[0] for item in sublist]
    counted_data = Counter(flatten_data)

    result_json = {key: value for key, value in counted_data.items()}
    print(json.dumps(result_json))
    for i in result_json.keys():
        doLike(i,result_json[i])

    flatten_data = [item for sublist in post[1] for item in sublist]
    counted_data = Counter(flatten_data)

    result_json = {key: value for key, value in counted_data.items()}
    print(json.dumps(result_json))
    for i in result_json.keys():
        doRecastComment(i,result_json[i])

def doForAuthor() :
    print("author gak minta tip, cuman minta recast komen otomatis pada 5 postingan teratas 🥰")
    doLike(myFid,5)
    doRecastComment(myFid,5)


def checkMyLiker(line):
    print(">> ",line.strip())

    urls = re.findall(r'(https?://\S+)', line.strip())
    line = urls[0]
    isMoreThan100 = True
    cursor = ""
    fidLiker = []

    parsed_url = urlparse(line)
    if not is_link(parsed_url):
        return
    path_parts = parsed_url.path.split("/")
    username = path_parts[1]
    identifier = path_parts[2]
    print("Username:", username)
    print("Identifier:", identifier)
    getHash = setupRequest("GET",urlGetCastByHash.format(identifier,username),headers,payload)
    for hash in getHash['result']['casts'] :
        hash = hash['hash']
        if identifier not in hash:
            continue
        getListLiker = setupRequest("GET",urlGetCastLikes.format(hash,100),headers,payload)
        while isMoreThan100 :
            lenLike = len(getListLiker['result']['likes'])
            print(lenLike)
            if lenLike >=100 :
                isMoreThan100 = True
                cursor = getListLiker['next']['cursor']
            else :
                isMoreThan100 = False
            for liker in getListLiker['result']['likes']:
                fidLiker.append(liker['reactor']['username'])
            getListLiker = setupRequest("GET",urlGetCastLikes.format(hash,100)+"&cursor="+cursor,headers,payload)
    return fidLiker



import sys

def split_text_into_chunks(text, chunk_size=320, separator='--'):
    # Split the text into chunks of the given size
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    # Join the chunks with the separator
    return separator.join(chunks)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found."
    except IOError:
        return "An error occurred while reading the file."


# file_path = 'list-cast.txt'
# file_content = read_file(file_path)
# username_pattern = re.compile(r'https?://warpcast\.com/([^/]+)')
# usernames = username_pattern.findall(file_content)
# print(usernames)
# sys.exit()

# spli=split_text_into_chunks(file_content)
# print(spli)

arguments = [".\autolikerecast.py","2","1","0"]
if myUname == "imposteruck" :
    arguments = sys.argv
    print("Total arguments:", len(arguments))
    print("Arguments:", arguments)
if arguments[1] == "1" :
    doBackToOtherUser()
    with open('last-run.txt', 'w') as file:
        # Menulis konten ke dalam file
        file.write('{}'.format(timestamp_milidetik_now))
elif arguments[1] == "2" and len(arguments) > 3:
    doBatchLike(arguments[2],arguments[3])
elif arguments[1] == "3" :
    listLiker = checkMyLiker(arguments[2])
    listNotLike = []
    textFile = read_file("list-cast.txt")
    username_pattern = re.compile(r'https?://warpcast\.com/([^/]+)')
    usernames = username_pattern.findall(textFile)
    for u in usernames:
        if u not in listLiker:
            listNotLike.append(u)
    print(listNotLike,"jumlah :",len(listNotLike))

else :
    print("Do Nothing")
