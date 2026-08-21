def get_all_users():
    # connect to db -- run db query
    return [
        {"id": 1, "name": "John", "email": "j@k.com", "phone": 124356},
        {"id": 2, "name": "Steve", "email": "s@t.com", "phone": 345678},
    ]


def create_user(user):
    # connect to db -- exec db mutation
    return {
        "id": 3,
        **user.model_dump(),
        "message": "User created Successfully!",
    }


def fetch_user_by_id(user_id):
    print(user_id)
    # connect to db -- run db query
    return {"id": user_id, "name": "John", "email": "j@k.com", "phone": 124356}


def update_user_by_id(user_id, user):
    print("New Form Data:")
    print(user)
    # connect to db -- exec db mutation
    return {
        "id": user_id,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "message": "Updated Successfully",
    }
