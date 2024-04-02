from unittest.mock import MagicMock
from domain.services.MailService import (
    MailService,
)


def test_get_mails():
    # Create a mock IMailingServicePort instance
    mock_mailing_service_port = MagicMock()
    mock_mails = [
        MagicMock(),
        MagicMock(),
    ]  # Replace with actual Mail instances if needed
    mock_mailing_service_port.get_emails.return_value = mock_mails

    # Instantiate the MailService with the mock
    mail_service = MailService(mock_mailing_service_port)

    # Call the get_mails method
    result = mail_service.get_mails()

    # Assertions to ensure the IMailingServicePort methods are called correctly
    mock_mailing_service_port.connect.assert_called_once()
    mock_mailing_service_port.get_emails.assert_called_once()
    mock_mailing_service_port.disconnect.assert_called_once()

    # Assert that the result is as expected
    assert result == mock_mails
