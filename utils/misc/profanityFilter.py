from better_profanity import profanity


def censored_message(message) -> str:
    """
    This function working only with english words
    """
    censored_text = profanity.censor(message)
    return censored_text
