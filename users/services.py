import requests


class Profiles:
    API_URL = 'https://some-url'

    @staticmethod
    def get_profile_uuid_by_email_or_none(email):
        # todo:
        query = """
            query get_email($value: String!) {
                profile {
                    uuid
                }
            }
        """

        # resp = requests.get(Profiles.API_URL, params={
        #     'query': query,
        #     'variables': {'value': email}
        # })

        # parse response
        person_uuid = None

        return person_uuid

    @staticmethod
    def create_new_profile(email):
        # todo: (P)-[HAS]->(E), create email if DNE
        person_uuid = None

        return person_uuid


class Emails:
    API_URL = 'https://some-url'

    def send_account_claim_token_email(self, email, claim_token):
        pass
