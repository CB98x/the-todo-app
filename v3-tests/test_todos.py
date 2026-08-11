
from reminders import get_task_list, update_task_list


def test_save_and_load_round_trip(tmp_path):
    file_path = tmp_path / "todos.json"
    # arrange: make a small task list
    task_list = [{"title": "task_title1", "due_date": "06-03-2026", "done": False}, {"title": "task_title2", "due_date": "06-13-2026", "done": False}]
    # act: write it, then read it back
    update_task_list(task_list, file_path)
    read = get_task_list(file_path)
    # assert: what you read == what you wrote
    assert task_list == read

def test_get_task_list_returns_empty_when_file_missing(tmp_path):
    file_path = tmp_path / "todos.json"
    read = get_task_list(file_path)
    # assert: what you read == what you wrote
    assert read == []

def test_get_task_list_returns_empty_when_file_is_garbage(tmp_path):
    file_path = tmp_path / "todos.json"
    # arrange: make a small task list
    file_path.write_text("this is not json{{{")
    # act: read it back
    read = get_task_list(file_path)
    # assert: what you read == what you wrote
    assert read == []

