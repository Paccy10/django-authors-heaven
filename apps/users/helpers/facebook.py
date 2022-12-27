import pdb

import requests
from facebook import GraphAPI, GraphAPIError

from ..error_messages import errors


class Facebook:
    """Facebook class to validate token and return user profile"""

    @staticmethod
    def validate(auth_token):
        try:
            graph = GraphAPI(access_token=auth_token)
            profile = graph.request(
                "/me?fields=first_name,last_name,middle_name,name,email"
            )

            return profile

        except GraphAPIError:
            raise ValueError(errors["token"]["invalid"])
