import json
from logging import exception
import re
import mysql.connector
import datetime
from datetime import date, time, datetime
from time import sleep
import requests
from requests.api import request
from useful_stuff import pretty_response, write_to_file
from telegram1 import send_message
from time import sleep


BASE_URL = 'https://api.github.com'
ORG = 'Loopring'
KEYWORDS = [' GME ', 'Gamestop']

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="hashes"
)

mycursor = mydb.cursor()

def get_repos():
    repo_list = []
    url = '{}/orgs/{}/repos'.format(BASE_URL, ORG)
    request = requests.get(url)
    json_data =  request.json()
   
    for i in json_data:
        repo_list.append(i["name"])
    
    return repo_list

def get_branches(repo):
    url = '{}/repos/{}/{}/branches'.format(BASE_URL, ORG, repo)
    request = requests.get(url)
    return request.json()

def get_commits_shas(repo):
    shas = []
    url = '{}/repos/{}/{}/commits'.format(BASE_URL, ORG, repo)
    request = requests.get(url)
    json_data = request.json()
    for i in json_data:
        try:
            commit = i['sha']
            tmp = i['commit']['committer']['date']
            #datetime.datetime.strptime(tmp,"%Y-%m-%dT%H:%M:%SZ")
            now = datetime.now()
            pretty_date_delta = datetime.strptime(tmp,"%Y-%m-%dT%H:%M:%SZ") - now
            if pretty_date_delta.days *(-1) > 5:
                print('skipped cause too old')
                continue
            shas.append(i['sha'])
        except Exception as e:
            print(e + 'line 58')
    return shas

def get_commit_urls(repo, commit_sha):
    raw_urls = []

    url = '{}/repos/{}/{}/commits/{}'.format(BASE_URL, ORG, repo, commit_sha)
    request = requests.get(url)
    commit = request.json()

    try:
        files = commit["files"]
        for dictiniary in files:
            # TODO check if text based
            raw_urls.append(dictiniary["raw_url"])
        
        return raw_urls
    except Exception as e:
        print(e)

def insert_hash(hash, repo):
    sql = "INSERT IGNORE INTO hashes (hash, repo_name) VALUES (%s, %s)"
    val = (hash, repo)
    mycursor.execute(sql, val)
    mydb.commit()

def check_if_hash_exists(repo, hash):
    #sql = f'SELECT hash, repo_name from hashes WHERE repo_name={repo}'
    #val = (repo,)
    mycursor.execute("SELECT hash, repo_name from hashes WHERE repo_name = 'whitepaper'")
    myresult = mycursor.fetchall()
    mydb.commit()
    for i in myresult:
        if i[0] == hash:
            return True
    return False

    #sql = "SELECT 1 FROM hashes WHERE hash = 'hello' LIMIT 1;" # TODO

def insert_repos(repos):
    sql = 'INSERT IGNORE INTO repos (repo_name) VALUES (%s)'  
    for repo in repos:
        val = (repo,)
        mycursor.execute(sql, val)
        mydb.commit()

def check_keywords(url):
    #raw_data = requests.get(url).text
    # really bad solution
    if url[-3:] == 'apk':
        print('apk extension')
        return False
        
    print(url)


    raw_data = requests.get(url)
    if raw_data.headers.get('content-type')[0:4] != 'text':
        print('wrong data type??! ' + raw_data.headers.get('content-type'))
        return False
    raw_data = raw_data.text
    print('checking keywords, len of string: ' + str(len(raw_data)))
    for i in KEYWORDS:
        if re.search(i, raw_data, re.IGNORECASE):
            print('done with checking!!!')
            return True

    print('done with checking!!!')
    return False

def check_date_of_commit(repo, sha):
    url = '{}/repos/{}/{}/commits'.format(BASE_URL, ORG, repo)
    request = requests.get(url)
    json_data = request.json()
    
    pass



def main():
    global today
    today  = date.today()
    #t0 = time.time()
    repos = get_repos()
    for repo in repos:
        shas = get_commits_shas(repo)
        for sha in shas:
            if check_if_hash_exists(repo, sha):
                print('exists')
                continue
            print('new')
            insert_hash(sha, repo)
            urls = get_commit_urls(repo, sha)
            print('amount of files: ' + str(len(urls)))
            for url in urls:
                if check_keywords(url):
                    send_message(f'{url} there is somewhere one of the keywords found')
                    print('BIG')
                    print(url)
    #t1 = time.time()
    #print('total time: ', t1-t0)

while True:
    main()
    print('sleeping now')
    sleep(60*10)
        # repo = get_repos()[-3]
    # shas = get_commits_shas(repo)
    # #insert_hash(shas[2], repo)
    # urls = get_commit_urls(repo, shas[2])
    

    # #write_to_file('raw_urls.json', pretty_response(get_commit_content(urls)))
    # write_to_file('raw_urls.json', pretty_response(urls))
    # #write_to_file('commits.json', pretty_response(shas))
    # #print(get_branches(repos[-3]))
    # url = '{}/repos/{}/{}/commits'.format(BASE_URL, ORG, repo)
    # json_data = requests.get(url).json()
    # write_to_file('commits.json', pretty_response(json_data))




#main()
#insert_repos(get_repos())

#repos = get_repos()
#print(check_if_hash_exists('whitepaper', '7c0d341aef7c54dd1dae24fe41727e99083bec2e'))

# for repo in repos:
#     shas = get_commits_shas(repo)
#     for sha in shas:
#         insert_hash(sha, repo)
