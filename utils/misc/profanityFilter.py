from better_profanity import profanity


def censored_message(message):
    censored_text = profanity.censor(message)
    return censored_text
