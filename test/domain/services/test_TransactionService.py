# tests/test_mail_service.py
from unittest.mock import MagicMock, ANY
from domain.services.TransactionService import (
    TransactionService,
)


def test_get_transaction():
    # Create a mocks
    mock_accounts = [MagicMock(), MagicMock()]
    mock_tags = [MagicMock()]
    mock_dbRepository = MagicMock()
    mock_llmServicePort = MagicMock()

    mock_dbRepository.get_all_accounts.return_value = mock_accounts
    mock_dbRepository.get_all_tags.return_value = mock_tags

    # Instantiate the TransactionService with the mock
    notification_service = TransactionService(
        mock_llmServicePort,
        mock_dbRepository,
    )

    # Call the get_transaction method
    mail = MagicMock()
    notification_service.get_transaction(mail)

    # Assertions to ensure the methods are called correctly
    mock_dbRepository.get_all_accounts.assert_called_once()
    mock_dbRepository.get_all_tags.assert_called_once()
    mock_llmServicePort.extract_transaction.assert_called_once_with(
        ANY, mock_accounts, mock_tags
    )
