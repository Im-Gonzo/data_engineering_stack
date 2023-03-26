import requests
import logging
from requests.auth import HTTPBasicAuth
from utils import parse_arguments as args

logging.basicConfig(level=logging.INFO)


def retrieve_comments(
    username: str,
    password: str,
    client_id: str,
    client_key: str,
    user_agent: str,
    thread_id: str,
) -> list:
    """
    Connects to the Reddit API and fetches comments from the specified thread.

    :param username: Reddit account username
    :param password: Reddit account password
    :param client_id: Reddit API client ID
    :param client_key: Reddit API client secret
    :param user_agent: User agent string for API requests
    :param thread_id: Reddit thread ID
    """
    if not username or not password:
        logging.warning("Either username or password not provided")
        return

    if not client_id or not client_key:
        logging.warning("Either client id or client key not provided")
        return

    if not thread_id:
        logging.warning("Quarterly id not provided")
        return

    auth = HTTPBasicAuth(client_id, client_key)
    data: dict = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    headers: dict = {"User-Agent": user_agent}

    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )
    response.raise_for_status()
    access_token = response.json()["access_token"]

    # Get the comments using the Reddit API
    headers["Authorization"] = f"bearer {access_token}"
    response = requests.get(
        f"https://oauth.reddit.com/comments/{thread_id}?depth=10&limit=500",
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()

    # Extract and print the comments
    comments: list = data[1]["data"]["children"]

    return comments


if __name__ == "__main__":

    arguments = args.parse_arguments()
    username: str = arguments.username
    password: str = arguments.password
    client_id: str = arguments.client_id
    client_key: str = arguments.client_key
    user_agent: str = arguments.user_agent
    thread_id: str = arguments.thread_id

    retrieve_comments(username, password, client_id, client_key, user_agent, thread_id)
