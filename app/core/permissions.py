
def has_permission(user_role: str, allowed: list[str]) -> bool:
    return user_role in allowed
