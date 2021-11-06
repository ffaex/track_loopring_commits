from time import sleep
import requests
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

def main():
    repos = get_repos()
    print(get_branches(repos[-3]))


main()