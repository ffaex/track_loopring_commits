import json
from time import sleep
import requests
from requests.api import request
from useful_stuff import pretty_response, write_to_file


BASE_URL = 'https://api.github.com'
ORG = 'Loopring'

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

def get_commits(repo):
    shas = []
    url = '{}/repos/{}/{}/commits'.format(BASE_URL, ORG, repo)
    request = requests.get(url)
    json_data = request.json()
    for i in json_data:
        shas.append(i['sha'])
    return shas

def get_commit(repo, commit_sha):
    url = '{}/repos/{}/{}/commits/{}'.format(BASE_URL, ORG, repo, commit_sha)
    request = requests.get(url)
    json_data = request.json()
    return json_data

def get_commit_content(commit):
    raw_urls = []
    files = commit["files"]
    for dictiniary in files:
        raw_urls.append(dictiniary["raw_url"])
    
    return raw_urls


def main():
    repo = get_repos()[-3]
    shas = get_commits(repo)
    tmp = get_commit(repo, shas[2])
    

    write_to_file('raw_urls.json', pretty_response(get_commit_content(tmp)))
    write_to_file('commit_data.json', pretty_response(tmp))
    #write_to_file('commits.json', pretty_response(get_commits(repo)))
    #print(get_branches(repos[-3]))


main()