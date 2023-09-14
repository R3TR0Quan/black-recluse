import requests
import bs4
import re
import sqlite3

def get_privacy_policy(url):

  """Gets the privacy policy for the given URL."""

  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.content, "html.parser")

  privacy_policy_link = soup.find(href=re.compile(r"/main-content"))
  if privacy_policy_link is not None:
    privacy_policy_url = privacy_policy_link["href"]

    response = requests.get(privacy_policy_url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    privacy_policy = soup.find(id="privacy-policies")
    if privacy_policy is not None:
      privacy_policy_text = privacy_policy.text
      return privacy_policy_text

  return None

def crawl_websites(starting_urls):

  """Crawls the given websites and extracts their privacy policies."""

  database = sqlite3.connect("privacy_policies.db")
  cursor = database.cursor()

  cursor.execute("CREATE TABLE IF NOT EXISTS privacy_policies (url TEXT, privacy_policy TEXT)")

  for starting_url in starting_urls:
    privacy_policy = get_privacy_policy(starting_url)
    if privacy_policy is not None:
      cursor.execute("INSERT INTO privacy_policies (url, privacy_policy) VALUES (?, ?)", (starting_url, privacy_policy))

  database.commit()
  database.close()

def main():
  starting_urls = ["https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement"]
  crawl_websites(starting_urls)

if __name__ == "__main__":
  main()
