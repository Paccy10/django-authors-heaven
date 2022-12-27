from twitter import Api

from authors_heaven.settings.base import env

from ..error_messages import errors


class Twitter:
    """Twitter class to validate tokens and return user info"""

    @staticmethod
    def validate(access_token_key, access_token_secret):
        consumer_key = env("TWITTER_API_KEY")
        consumer_secret = env("TWITTER_API_SECRET")

        try:
            api = Api(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret,
            )
            profile = api.VerifyCredentials(include_email=True)

            return profile.__dict__

        except Exception:
            raise ValueError(errors["access_tokens"]["invalid"])
