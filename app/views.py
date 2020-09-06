from app import app
from flask import render_template, url_for, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import json
import re


username = ''

@app.route('/', methods=['GET'])
def home():
    # Landing page!
    text = "Welcome! "
    text += "Visit /active/<user> or /downwards/<repo> to start"
    return render_template('user.html',result=text)


@app.route('/active/<user>', methods=['GET'])
def index(user):
    # An endpoint to return a json boolean; true when a user has pushe a code
    # within that last 24 hours and false when otherwise.
    global username
    username = user
    #return render_template('user.html',result=currentRepo(username))
    return jsonify(currentRepo(username))



@app.route("/downwards/<repo>")
def about(repo):
    # An endpoint that returns a json object; which is true when a give git repo
    # has more deletions than additions in the last 7 days and false when otherwise.
    user =  username
    #return render_template('repo.html', result=moreDeletions(repo, user))
    return jsonify(additionsAndDeletions(repo, user))

    

def currentRepo(username):
    # A function for the endpoint '/active/<user>'
    url = "https://github.com/"+username+"?tab=repositories"
    
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text
    
    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")# lxml
    #print(soup.prettify()) # print the parsed data of html
    months = ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    today = datetime.now()
    today_date = str(today).split(' ')[0]
    today_date = today_date.split('-')
    
    repo_urls = soup.find_all("relative-time")
    
    if not repo_urls:
        return "Wrong url: " + url
    
    for link in repo_urls:
        print(link)
        for count, ele in enumerate(months):
            if ele == link.text.split(' ')[0]:
                date_ = str(count+1) + ' ' + link.text.split(' ')[1][:-1] + ' ' \
                            + link.text.split(' ')[-1]
                date_ = date_.split(' ')
                repo_date = date(int(date_[2]), int(date_[0]), int(date_[1]))           
                today_ = date(int(today_date[0]), int(today_date[1]), int(today_date[2]))
                
                delta = today_ - repo_date
                if delta.days <= 1:
                    return json.dumps({ 'Pushed a code in last 24h': True})
    return json.dumps({ 'Pushed a repo in last 24h': False})


def additionsAndDeletions(repo, username):
    # A function for the endpoint '/downwards/<repo>'
    if not username:
        return "No user specified! Consider visiting the route /active/user "

    months = ['Jan', 'Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec']
    today_date = datetime.now()
    today_date = str(today_date).split(' ')[0]
    today_date = today_date.split('-')
    today_date = date(int(today_date[0]), int(today_date[1]), int(today_date[2]))
    
    # The URL of a given repo
    repo_url = r'https://github.com/' + username + '/' + repo

    
    def commitLogic(commit_date):
        """ A function to process the date that a commit was made.
        The format of the data is edited. String representation of 
        months is changed to digits"""
        
        date_ = commit_date.text
        date_ = str(date_).split(' ')
        date_ = date_[-3:]
        
        for count, ele in enumerate(months):
            if ele == date_[0]:
                month = count+1
        for item in range(len(date_)):
            if ',' in date_[item]:
                date_[item] = date_[item].replace(',','')
                
        date_ = date(int(date_[-1]), month, int(date_[1]))
        return date_
    
    
    # User commits
    # The URL displaying all the commits of a given repo
    commits = repo_url+'/commits/master'
    html_commits = requests.get(commits).text
    soup_commits = BeautifulSoup(html_commits, "html.parser")
    # Extracting specific data based on html tags
    commit_dates = soup_commits.find_all('div', class_='f6 text-gray min-width-0')
    commit_links = soup_commits.find_all('a', class_=re.compile('text-mono f6 btn btn-outline BtnGroup-item'))
    
    
    # The record of deletions and additions
    deletions = 0
    additions = 0
    
    # The very that the given url is valid
    if not commit_links:
        return "Invalid url: " + commits
    
    # Looping through the repos and considering only repos that were edited in less than a week
    for i in range(len(commit_dates)):
        delta = today_date - commitLogic(commit_dates[i])
        if delta.days <= 7:  
            ################### LINKS  ###################
            link = str(commit_links[i]).split()
            newLink = r'https://github.com' + link[6][6:-2]

            html_content = requests.get(newLink).text
            soupLink = BeautifulSoup(html_content, "html.parser")
            soupObj = soupLink.find_all('div', class_=re.compile("toc-diff-stats"))
            result = soupObj[0].find_all('strong')
            
            result = str(result).split(' ')
            deletion = [word for word in result[2] if word.isdigit()]
            addition = [word for word in result[0] if word.isdigit()]
            
            additions += int(''.join(addition))
            deletions += int(''.join(deletion))
            
    if deletions > additions:
        #print(deletions, ' ', additions)
        return json.dumps({"More deletions than additions": True})
    #print(deletions, ' ', additions)
    return json.dumps({"More deletions than additions": False})

