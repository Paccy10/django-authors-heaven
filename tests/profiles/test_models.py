from apps.profiles.models import get_upload_to


class TestProfileModel:
    """Test profile model"""

    def test_user_str(self, profile):
        assert profile.__str__() == f"{profile.user.username}'s profile"

    def test_get_upload_to(self, profile):
        path = get_upload_to(profile, "default.png")
        path_parts = path.split("/")
        parent_folder = path_parts[0]
        sub_folder = path_parts[1]

        assert parent_folder == "profiles"
        assert sub_folder == profile.user.username
