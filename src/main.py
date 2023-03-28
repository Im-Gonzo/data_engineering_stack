import praw
import logging
from utils import parse_arguments as args

logging.basicConfig(level=logging.INFO)

def get_tech_stack_comment(comments: list) -> list:
    """
    Comment patterns:
    1. Pattern 1 
        1.2.3...
        7. Tech stack:
            Golang
            Terraform
            Argo Workflows
            AWS S3, Macie, IAM etc.
            Snowflake
            DBT
    2.
    """
    tech_stacks: list = []
    all_comments: list = []
    nested_comments: list = []

    # Split the comments by break line
    for comment in comments:
        all_comments.append(comment.body.split('\n\n'))
    
    # Some comment's are in one line separated by \n , we need to split them
    for comment in all_comments:
        if len(comment) == 1:
            nested_comments.append(comment[0].split('\n'))
    
    # Flat list of list
    nested_comments = [line for sublist in nested_comments for line in sublist]

    # We save the comments with the tech stack
    for comment in nested_comments:
        if comment.startswith('7'):
            tech_stacks.append(comment)

    # Extract the tech stack from the pattern
    # for comment in all_comments:
        # logging.info('+'*100)

    # for i, line in enumerate(comment):
    #     # print(f'Line {i+1} \n {line}')
    #     if line.startswith('7') or line.startswith('7)'):
    #         tech_stacks.append(comment[i:])
    #     try:
    #         nested_comment: list = line.split('\n\n')
    #         for nested in enumerate(nested_comment):
    #             if nested.startswith('7') or nested.startswith('7)'):
    #                 tech_stacks.append(nested)
    #     except Exception as e :
    #         pass
    #         # logging.info(str(e))
            
    for tech in tech_stacks:
        print('-'*100)
        print(tech)



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

    
    print(f'Successfully connected as user = {reddit.user.me()}')

    # Fetch and return the comments
    submission.comments.replace_more(limit=None)
    comments = [comment for comment in submission.comments.list()]

    return comments


if __name__ == "__main__":

    arguments = args.parse_arguments()
    username: str = arguments.username
    password: str = arguments.password
    client_id: str = arguments.client_id
    client_key: str = arguments.client_key
    user_agent: str = arguments.user_agent
    thread_id: str = arguments.thread_id

    comments: list = retrieve_comments(username, password, client_id, client_key, user_agent, thread_id)
    tech_stack_comments: list = get_tech_stack_comment(comments)