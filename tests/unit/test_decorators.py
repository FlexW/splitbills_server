from unittest.mock import patch, MagicMock
from app.models.user import User
from app.decorators import confirmation_required


@patch("app.decorators.get_authorized_user")
@patch("app.decorators.abort")
def test_error_on_not_confirmed(mock_abort, mock_get_authorized_user):
    @confirmation_required
    def requires_confirmation():
        pass

    mock_get_authorized_user.return_value = User(email="muster@mail.de",
                                                 confirmed=False)

    requires_confirmation()

    mock_abort.assert_called_with(403, "Account needs to be confirmed for this operation")


@patch("app.decorators.get_authorized_user")
@patch("app.decorators.abort")
def test_confirmation_required(mock_abort, mock_get_authorized_user):
    mock_function = MagicMock()

    mock_function = confirmation_required(mock_function)

    mock_get_authorized_user.return_value = User(email="muster@mail.de",
                                                 confirmed=True)

    mock_function()()

    mock_abort.assert_not_called()
    mock_function().assert_called()
