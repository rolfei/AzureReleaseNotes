import requests
import json
import re

organization = ''
project = ''
repository = ''
tag1 = 'tag1.0'
tag2 = 'tag4.0'
access_token = ''

base_url = f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository}'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {access_token}',
}

# Get the commit associated with the first tag
def getTagCommitId(tagname):
    response = requests.get(
        f'{base_url}/refs?filter=tags/{tagname}&api-version=7.0',
        headers=headers,
    )
    data = response.json()
    #print (response.content)
    commit_id = data['value'][0]['objectId']
    return commit_id

commit_id1= getTagCommitId(tag1)
commit_id2 = getTagCommitId(tag2)

def getTagChanges(tag1,tag2):
    # Get the diff between the two tags, just list the chnages
    response = requests.get(
        f'{base_url}/diffs/commits?baseVersion={tag1}&baseVersionType=tag&targetVersion={tag2}&targetVersionType=tag&api-version=7.0',
        headers=headers,
    )
    data = response.json()
    #print (response.content)
    return data

def getTagDiffCommits(tag1,tag2):
    # Get the diff between the two tags, just list the chnages
    response = requests.get(
        f'{base_url}/commits?searchCriteria.compareVersion.version={tag2}&searchCriteria.itemVersion.version={tag1}&searchCriteria.compareVersion.versionType=tag&searchCriteria.itemVersion.versionType=tag&api-version=7.0',
        headers=headers,
    )
    data = response.json()
    print (response.content)
    return data


def getCommitDetails(commitId):
    response = requests.get(
    f'{base_url}/commits/{commitId}?api-version=7.0',
    headers=headers,
    )
    data = response.json()

    return data

def extractJiraID(message):
      pattern = re.compile('(^[A-Z]{2,4}-[0-9]{1,5}:?) +(.*)')
      match = re.search(pattern, message)
      if match:
          return match.group(1)
      else:
          return 'Missing JIRA-ID'

# Output the commit message and timestamp of all differences

diffData=getTagDiffCommits(tag1,tag2)
release_summary=''
for commit in diffData['value']:
   
    commitDetails=getCommitDetails(commit['commitId'])
    jiraID = extractJiraID(commitDetails['comment'])
    print(f"jira ID: {jiraID}  author:{commitDetails['author']['email']} comment: {commitDetails['comment']} {commitDetails['committer']['date']}")




 
