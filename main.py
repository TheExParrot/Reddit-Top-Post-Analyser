import requests
from bs4 import BeautifulSoup

# Magic Numbers
NUMBER_OF_POSTS = 10
NUMBER_OF_COMMENTS = 20


# Function that returns the top x comments of the post
def get_comments_text(post_url, num_comments):
    comment_response = requests.get(post_url, headers={'User-agent': 'Mozilla/5.0'})
    comment_soup = BeautifulSoup(comment_response.content, 'html.parser')
    comments = comment_soup.find_all('div', {'class': 'md'})
    comments_list = []
    for i in range(1, num_comments + 1):
        comments_list.append(comments[i].text.strip())
    return comments_list


# Get the website using the requests library
url = "https://old.reddit.com/r/worldnews/top/?sort=top&t=week"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# Obtain the html object from the subreddit
soup = BeautifulSoup(response.content, "html.parser")

# Scrape the posts page and filter out promoted posts/advertisements
posts = soup.find_all("div", class_="top-matter")
non_promoted_posts = [post for post in posts if "promoted by"
                      not in post.find("p", class_="tagline").text.strip()]

# Iterate through the top x posts and return the content of the top y comments
urls = []
for i in range(NUMBER_OF_POSTS):
    urls.append(non_promoted_posts[i].find("a", class_="bylink comments may-blank")['href'])
