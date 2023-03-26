import argparse


def parse_arguments():
    """
    Receives the arguments from the console
    """
    parser = argparse.ArgumentParser(description="Fetch comments from a Reddit thread.")

    parser.add_argument(
        "--username", type=str, required=True, help="Your Reddit username"
    )
    parser.add_argument(
        "--password", type=str, required=True, help="Your Reddit password"
    )
    parser.add_argument(
        "--client_id", type=str, required=True, help="Your Reddit API client ID"
    )
    parser.add_argument(
        "--client_key",
        type=str,
        required=True,
        help="Your Reddit API client secret/key",
    )
    parser.add_argument(
        "--user_agent",
        type=str,
        default="python:data_engineering_stack:v1.0: (by /u/Lord_Gonz0)",
        help='User agent for Reddit API requests (default: "Reddit Comment Fetcher")',
    )
    parser.add_argument("--thread_id", type=str, required=True, help="Thread id")

    args = parser.parse_args()

    return args
