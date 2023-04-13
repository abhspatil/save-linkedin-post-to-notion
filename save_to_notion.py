import requests
from notion_client import Client
from bs4 import BeautifulSoup
from linkedin_api import Linkedin


# Set up Notion API client
notion = Client(auth="<NOTION_API_KEY>")
db_name = "Database Name" # Replace with the name of your database in Notion


# Set up LinkedIn API client
linkedin = Linkedin()
linkedin_login = linkedin.login("<LINKEDIN_EMAIL>", "<LINKEDIN_PASSWORD>")


# Fetch data from LinkedIn post
post_url = "https://www.linkedin.com/posts/username_postcontent"
post_request = requests.get(post_url)
post_html = post_request.text
soup = BeautifulSoup(post_html, "html.parser")

# Extract necessary data from the post HTML
post_content = soup.find(class_="break-words").get_text()
post_likes = soup.find(class_="social-details-reactors-tab-count").get_text()
post_comments = soup.find(class_="social-details-comments-tab-count").get_text()
post_author = soup.find(class_="feed-shared-actor__name").get_text()


# Create new page in Notion database
database = notion.databases.retrieve(database_id="<NOTION_DATABASE_ID>") # Replace with your database ID
new_page = {
    "Post Content": {"title": [{"text": {"content": post_content}}]},
    "Likes": {"number": int(post_likes)},
    "Comments": {"number": int(post_comments)},
    "Author": {"title": [{"text": {"content": post_author}}]}
}
notion.pages.create(parent={"database_id": database_id}, properties=new_page)
