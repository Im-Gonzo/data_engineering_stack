import praw
import logging
import json
from utils import parse_arguments as args
from collections import Counter

logging.basicConfig(level=logging.INFO)


def clean_word_list(words: list, non_tech_words: str = 'json/non_tech_words.json') -> list:
    """
    Gets rid of the following characters in each word of the following:
    ,()/\\[]+7.\t\n*…:“”
    """
    with open (non_tech_words, 'r') as f:
        not_tech_words = json.load(f)['words']

    chars = ",()/\\[]+7.\t\n*…:“”"
    table = str.maketrans("", "", chars)
    cleaned_words = []
    for word in words:
        if "/" in word:
            cleaned_words.extend([w.translate(table) for w in word.split("/")])
        else:
            cleaned_words.append(word.translate(table))

    result: list = list(filter(None, cleaned_words))
    
    result_tech = [word for word in result if word not in not_tech_words]

    return result_tech


def get_insights(stack: list, tech_stack: str = "json/tech_stack.json") -> dict:
    """"""

    stack_count: dict = Counter(stack)
    with open(tech_stack, "r") as f:
        data = json.load(f)

    print(data)
    return stack_count


def parse_tech_stack(stack: list) -> list:
    """
    Parse the comments from the valid json stack categories
    src/json/tech_stack.json
    """
    dirty_words: list = []

    # Get all words from list
    for i, comment in enumerate(stack):
        dirty_words.append(comment.split(" "))

    # Flatten nested list of lists
    dirty_words = [line.lower() for sublist in dirty_words for line in sublist]
    clean_words = clean_word_list(dirty_words)

    return clean_words


def parse_nested_comments(comments: list) -> list:
    """
    Parse the list of nested comments.
    """

    tech_stacks: list = []
    all_comments: list = []
    nested_comments: list = []
    nested: list = []

    # Split the comments by break line
    for comment in comments:
        all_comments.append(comment.body.split("\n\n"))

    # Some comment's are in one line separated by \n , we need to split them
    for comment in all_comments:
        if len(comment) == 1:
            nested_comments.append(comment[0].split("\n"))
        else:
            # Some comments are nested
            for i, line in enumerate(comment):
                if line.startswith("7"):
                    nested.append(comment[i:])

    # Flat list of list
    nested_comments = [line for sublist in nested_comments for line in sublist]
    nested = [line for sublist in nested for line in sublist]

    # We save the comments with the tech stack
    for comment in nested_comments:
        if comment.startswith("7"):
            tech_stacks.append(comment)

    # Add stacks from nested comments
    tech_stacks.extend(nested)

    return tech_stacks


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

    # Create a Reddit instance using PRAW
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_key,
        password=password,
        user_agent=user_agent,
        username=username,
    )

    # Fetch the submission using the thread_id
    submission = reddit.submission(id=thread_id)

    print(f"Successfully connected as user = {reddit.user.me()}")

    # Fetch and return the comments
    submission.comments.replace_more(limit=None)
    comments = [comment for comment in submission.comments.list()]

    return comments


if __name__ == "__main__":

    with open("json/thread_ids.json", "r") as f:
        data = json.load(f)

    threads: list = list(data["id"])

    arguments = args.parse_arguments()
    username: str = arguments.username
    password: str = arguments.password
    client_id: str = arguments.client_id
    client_key: str = arguments.client_key
    user_agent: str = arguments.user_agent
    thread_id: str = arguments.thread_id

    if thread_id not in threads:
        # save new thread id into existing thread ids

        # check if new tech stack exist, if so add them to tech_stack.json

        pass

    # extract comments and parse them
    comments: list = retrieve_comments(
        username, password, client_id, client_key, user_agent, thread_id
    )
    parsed_comments: list = parse_nested_comments(comments)
    tech_stack: list = parse_tech_stack(parsed_comments)
    # Get insights
    count: dict = get_insights(tech_stack)
    print(tech_stack)
