from unittest.mock import MagicMock
from domain.services.NotificationService import (
    NotificationService,
)
from domain.entities.Notification import Notification


def test_send_notification():
    # Create a mocks
    mock_notification = Notification(personality="Any", style="Any", message="Mock")
    mock_notificationServicePort = MagicMock()
    mock_llmServicePort = MagicMock()
    mock_llmServicePort.generate_notification.return_value = mock_notification

    # Instantiate the NotificationService with the mock
    notification_service = NotificationService(
        mock_notificationServicePort,
        mock_llmServicePort,
    )

    # Call the send_notification method
    transaction = MagicMock()
    notification_service.send_notification(transaction)

    # Assertions to ensure the methods are called correctly
    mock_llmServicePort.generate_notification.assert_called_once_with(transaction)
    mock_notificationServicePort.send_notification.assert_called_once_with(
        mock_notification.message
    )
