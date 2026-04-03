"""Shared authorization helpers for user-owned content."""


def can_modify_owned_content(user, owner_id):
    """
    True if the user is the owner (by primary key) or a site superuser (User.admin).
    """
    if not user.is_authenticated:
        return False
    return user.pk == owner_id or user.is_admin
