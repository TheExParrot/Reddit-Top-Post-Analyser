import requests
from bs4 import BeautifulSoup

NUMBER_OF_POSTS = 10
NUMBER_OF_COMMENTS = 10

# Get the website using the requests library
url = "https://old.reddit.com/r/worldnews/top/?sort=top&t=week"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# Obtain the html object from the subreddit
soup = BeautifulSoup(response.content, "html.parser")

# Scrape the posts page and filter out promoted posts/advertisements
posts = soup.find_all("div", class_="top-matter")
non_promoted_posts = [post for post in posts if "promoted by"
                      not in post.find("p", class_="tagline").text.strip()]

# Get a list of the top posts URLs
urls = []
for i in range(NUMBER_OF_POSTS):
    urls.append(non_promoted_posts[i].find("a", class_="bylink comments may-blank")['href'])