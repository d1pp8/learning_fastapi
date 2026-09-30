from app.models import User, Wallet
from decimal import Decimal

def test_add_expense_success(
        db_session,
        client,
        user,
        wallet,
        auth_headers
):
    #Act
    response = client.post(
        '/api/v1/operations/expense',
        json={
            "wallet_name": "Master",
            "amount": 50,
            "description": "Card"
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code==200
    assert response.json()["message"] == "Expense added"
    assert response.json()["wallet"] == wallet.name
    assert Decimal(str(response.json()["amount"])) == Decimal(50)
    assert Decimal(str(response.json()["new_balance"])) == Decimal(150)
    assert response.json()["description"] == "Card"


def test_add_expense_negative_amount(
        db_session,
        client,
        wallet,
        user,
        auth_headers
):
    # Act
    response = client.post(
        '/api/v1/operations/expense',
        json={
            "wallet_name": "Master",
            "amount": -100,
            "description": "Card"
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )
    # Assert
    assert response.status_code == 422

def test_add_expense_wallet_name_is_empty(
        db_session,
        client,
        wallet,
        user,
        auth_headers,
):
    # Act
    response = client.post(
        '/api/v1/operations/expense',
        json={
            "wallet_name": "      ",
            "amount": 100,
            "description": "Card"
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )
    # Assert
    assert response.status_code == 422


def test_add_expense_wallet_not_exist(
        db_session,
        client,
        wallet,
        user,
        auth_headers,
):
    # Act
    response = client.post(
        '/api/v1/operations/expense',
        json={
            "wallet_name": "Queue",
            "amount": 100,
            "description": "Card"
        },
        headers=auth_headers
    )
    # Assert
    assert response.status_code == 404


def test_add_expense_unauthorized(
        client,
        auth_headers
):
    # Act
    response = client.post(
        '/api/v1/operations/expense',
        json={
            "wallet_name": "Master",
            "amount": 100,
            "description": "Card"
        },
        headers=auth_headers
    )
    # Assert
    assert response.status_code == 401



def test_add_expense_not_enough_money(
        db_session,
        client,
        user,
        wallet,
        auth_headers
):
    #Act
    response = client.post(
        '/api/v1/operations/expense',
        json={
            "wallet_name": "Master",
            "amount": 500,
            "description": "Card"
        },
        headers=auth_headers
    )

    #Assert
    assert response.status_code==400