from unittest.mock import patch

from apps.common.utils import send_email


class TestUtils:
    """Test common utils"""

    @patch("django.core.mail.EmailMessage.send")
    def test_send_email_function(self, send):
        send_email("Test Email", "I am testing email", ["test@app.com"])

        assert send.called is True
