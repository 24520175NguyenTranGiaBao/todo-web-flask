from .database import get_db_connection
from flask import Blueprint, jsonify, request

todo_api = Blueprint('todo_api', __name__)

@todo_api.route('/todos', methods=['GET'])
def get_todo_list():
    conn = get_db_connection()
    todos_from_db = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()

    todos = []
    for item in todos_from_db:
        todos.append({
            "id" : item["id"],
            "task" : item["task"],
            "done" : bool(item["done"])
        })
        
    return jsonify({
        "status" : "success",
        "todos" : todos
    })


@todo_api.route('/todos', methods=['POST'])
def add_todo_items():
    request_data = request.get_json()
    task_name = request_data.get('task')
    task_status = request_data.get('done', False)
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO todos (task, done) VALUES (?, ?)', (task_name, task_status)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "status" : "success",
        "message" : "Todo item added successfully"
    }), 201

@todo_api.route('/todos/<int:todo_id>', methods = ['PUT'])
def update_todo(todo_id):
    req_data = request.get_json()
    conn = get_db_connection()

    item = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()

    if item is None:
        conn.close()
        return jsonify({
            "message" : "item not found"
        }), 404

    if "task" in req_data:
        new_task = req_data.get("task")
    else:
        new_task = item["task"]

    if "done" in req_data:
        new_done = req_data.get("done")
    else:
        new_done = item["done"]
    
    conn.execute('UPDATE todos SET task = ?, done = ? WHERE id = ?', (new_task, new_done, todo_id))
    conn.commit()
    conn.close()

    return jsonify({
        "status" : "success",
        "message" : "item updated successfully",
        "item" : {
            "id" : todo_id,
            "task" : new_task,
            "done" : bool(new_done)
        }
    }), 200

@todo_api.route('/todos/<int:todo_id>', methods = ['DELETE'])
def delete_item(todo_id):
    conn = get_db_connection()

    item = conn.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    
    if item is None:
        conn.close()
        return jsonify({
            "message" : "item not found"
        }), 404
    
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "status" : "success",
        "message" : "Item has been deleted"
    }), 200
