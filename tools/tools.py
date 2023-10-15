from langchain.serpapi import SerpAPIWrapper


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret


def get_profile_url(text: str) -> str:
    """Searches for Linkedin Profile"""
    serp_api = CustomSerpAPIWrapper()
    results = serp_api.run(f"{text}")
    return results


def check_profile_url(url: str) -> bool:
    """Checks if URL is a valid Linkedin Profile Page."""
    # check if url is in this format: https://www.linkedin.com/in/eden-marco/
    if "linkedin.com/in/" in url:
        return True
    else:
        return False


def extract_unique_identifier(url: str) -> str:
    """Extracts a unique identifier from a LinkedIn Profile URL."""

    # Check if the URL is a LinkedIn profile URL
    if "linkedin.com/in/" in url:
        # Split the URL based on "linkedin.com/in/"
        parts = url.split("linkedin.com/in/")

        # Ensure we have the correct part and handle any query parameters
        unique_name = parts[1].split("?")[0]

        # Remove any trailing slashes
        unique_name = unique_name.rstrip("/")

        return unique_name
    else:
        raise ValueError("The provided URL is not a valid LinkedIn profile URL")


def reformat_linkedin_url(url: str) -> str:
    """Reformats a LinkedIn Profile URL to a standard format."""
    unique_name = extract_unique_identifier(url)

    return f"https://www.linkedin.com/in/{unique_name}/"
