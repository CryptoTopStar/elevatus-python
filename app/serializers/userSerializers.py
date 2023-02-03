def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "UUID": user["UUID"],
        "verified": user["verified"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def userResponseEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "UUID": user["UUID"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }

def userResponseTestEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "UUID": user["UUID"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def embeddedUserResponse(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]
