import json
import re
import mysql.connector
from time import sleep
import requests
from requests.api import request
from useful_stuff import pretty_response, write_to_file


BASE_URL = 'https://api.github.com'
ORG = 'Loopring'
KEYWORDS = ['GME', 'Gamestop']

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
        shas.append(i['sha'])
    return shas

def get_commit_urls(repo, commit_sha):
    raw_urls = []

    url = '{}/repos/{}/{}/commits/{}'.format(BASE_URL, ORG, repo, commit_sha)
    request = requests.get(url)
    commit = request.json()

    files = commit["files"]
    for dictiniary in files:
        raw_urls.append(dictiniary["raw_url"])
    
    return raw_urls

def insert_hash(hash, repo):
    sql = "INSERT INTO hashes (hash, repo_name) VALUES (%s, %s)"
    val = (hash, repo)
    mycursor.execute(sql, val)
    mydb.commit()

def check_if_hash_exists():
    sql = "SELECT 1 FROM hashes WHERE hash = 'hello' LIMIT 1;" # TODO

def insert_repos(repos):
    sql = 'INSERT IGNORE INTO repos (repo_name) VALUES (%s)'  
    for repo in repos:
        val = (repo,)
        mycursor.execute(sql, val)
        mydb.commit()

def check_keywords(url):
    raw_data = requests.get(url).text
    for i in KEYWORDS:
        if re.search(i, raw_data, re.IGNORECASE):
            return True
    return False
    pass

def main():
    repo = get_repos()[-3]
    shas = get_commits_shas(repo)
    insert_hash(shas[2], repo)
    urls = get_commit_urls(repo, shas[2])
    

    #write_to_file('raw_urls.json', pretty_response(get_commit_content(urls)))
    write_to_file('raw_urls.json', pretty_response(urls))
    #write_to_file('commits.json', pretty_response(get_commits(repo)))
    #print(get_branches(repos[-3]))


#main()
insert_repos(get_repos())