import requests
from bs4 import BeautifulSoup
import regex as re
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Update stopwords library
nltk.download('stopwords')

# Magic Numbers
NUMBER_OF_POSTS = 20
NUMBER_OF_COMMENTS = 30
NUMBER_OF_TOP_WORDS = 20


# Function that returns the top x comments of the post
def get_comments_text(post_url, num_comments):
    """Extracts the text of the top comments for a given reddit
    post URL and returns a list of the text in the comments.
    """
    comment_response = requests.get(post_url, headers={'User-agent': 'Mozilla/5.0'})
    comment_soup = BeautifulSoup(comment_response.content, 'html.parser')
    comments = comment_soup.find_all('div', {'class': 'md'})
    comments_list = []
    for i in range(1, min(num_comments + 1, len(comments))):
        comments_list.append(comments[i].text.strip())
    return comments_list


def get_subreddit_data(subreddit_name):
    """Extracts the top posts and comments for a given subreddit
    and returns a list of tuples with post titles and comment text.
    """
    # Get the website using the requests library
    subreddit_url = "https://old.reddit.com/r/" + subreddit_name + "/top/?sort=top&t=week"
    response = requests.get(subreddit_url, headers={"User-Agent": "Mozilla/5.0"})

    # Obtain the html object from the subreddit
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape the posts page and filter out promoted posts/advertisements
    posts = soup.find_all("div", class_="top-matter")
    non_promoted_posts = [post for post in posts if "promoted by"
                          not in post.find("p", class_="tagline").text.strip()]

    # Iterate through the top x posts and obtain the content of the top y comments
    data_list = []
    for i in range(min(NUMBER_OF_POSTS, len(non_promoted_posts))):
        url = non_promoted_posts[i].find("a", class_="bylink comments may-blank")['href']
        data_list.append((non_promoted_posts[i].find("a", class_="title").text.strip(),
                          get_comments_text(url, NUMBER_OF_COMMENTS)))
    return data_list


def process_text(content):
    """Processes the given text by removing non-alphabetic and
    stop words and converting all characters to lowercase.
    """
    # Convert all non-alphabetic and spacing characters
    # to a single whitespace
    non_alphabetic = r'[^a-zA-Z]+'
    content = re.sub(non_alphabetic, ' ', content)

    # Change all uppercase to lowercase
    content = content.lower()

    # Tokenise the content into a list of words
    content_list = re.split(' ', content)

    # Remove stop words and the word 'like' (as it appears alot everywhere)
    stop_words = set(stopwords.words('english'))
    return [word for word in content_list if len(word) > 2
            and word not in stop_words
            and word != 'like']


def get_processed_data(data_tuples):
    """Extracts all text from the given list of tuples
    and processes it into a list of words."""
    # Make a large string of all the data extracted
    complete_string = ""
    for post_text in data_tuples:
        complete_string += post_text[0]
        for comment_text in post_text[1]:
            complete_string += comment_text
    return process_text(complete_string)


def get_sorted_counts(words):
    """ Returns a sorted list of tuples with each unique
    word in the given list of words and its frequency.
    """
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)


def create_word_frequency_graph(words, num_top_words, filename):
    """Creates a bar graph of the frequency of the top num words in
    the given list of words and saves it to the given filename.
    """
    word_counts = get_sorted_counts(words)
    top_words = word_counts[:num_top_words]
    x_values = [word[0] for word in top_words]
    y_values = [word[1] for word in top_words]
    plt.bar(x_values, y_values)
    plt.xticks(rotation=90)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top {} Most Frequent Words this week on '
              'r/{}'.format(num_top_words, subreddit))
    plt.savefig(filename, bbox_inches='tight')


# Ask the user for the subreddit
subreddit = input("Enter the name of the subreddit to analyse: ")

# Extract the posts and comments data
print("Extracting posts and comments...")
data = get_subreddit_data(subreddit)

# Perform processing to the text
print("Processing text...")
words = get_processed_data(data)

# Save the output graph
filename = input("Enter filename for output graph: ")
create_word_frequency_graph(words, NUMBER_OF_TOP_WORDS, filename)
