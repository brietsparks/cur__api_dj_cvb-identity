from users.models import User


class AccountState:
    def __init__(self, email_claimed, username_claimed, profile_uuid):
        self.email_claimed = email_claimed
        self.username_claimed = username_claimed
        self.profile_uuid = profile_uuid
        
    def is_taken(self):
        return self.email_claimed or self.username_claimed
    
    def exists_but_unclaimed(self):
        return (
            self.email_claimed is False and
            self.username_claimed is False and
            self.profile_uuid
        )

    def does_not_exist(self):
        return (
            self.email_claimed is False and
            self.username_claimed is False and
            not self.profile_uuid
        )


class AccountStateFactory:

    @staticmethod
    def get_state(email, username):
        email_claimed = User.objects.filter(email=email).exists()
        username_claimed = User.objects.filter(username=username).exists()

        if email_claimed or username_claimed:
            return AccountState(email_claimed, username_claimed, False)

        profile_uuid = get_profile_uuid_by_email_or_none(email)
        if profile_uuid:
            return AccountState(False, False, profile_uuid)

        return AccountState(False, False, None)


def get_profile_uuid_by_email_or_none(email):
    # todo: send a request to the profile service to get-or-none profile uuid given email address
    return 1


