from better_profanity import (
    profanity,
)


def censored_message(message: str) -> str:
    """
    Get censored message.

    This function only works with English words.
    """
    censored_text = profanity.censor(message)
    return censored_text
