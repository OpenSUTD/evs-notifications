from .exec import execute_and_commit


def insert_command(name: str, chat_id: int, is_completed: bool, is_cancelled: bool) -> None:
    query = f"""
        INSERT INTO command (name, chat_id, is_completed, is_cancelled)
        VALUES ('{name}', {chat_id}, {'TRUE' if is_completed else 'FALSE'}, {'TRUE' if is_cancelled else 'FALSE'})
    """
    execute_and_commit(query)
