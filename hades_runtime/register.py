"""Register from flags. Display name is not identity."""


def select_register(
    is_partner: bool = False,
    is_family: bool = False,
    display_name: str | None = None,
    chat_count: int = 0,
    **_kwargs,
) -> str:
    del display_name, chat_count
    if is_family:
        return "sister"
    if is_partner:
        return "partner"
    return "stranger"
