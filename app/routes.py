from flask import Blueprint, jsonify, request
import psycopg2.extras
from .database import get_db_connection

todo_api = Blueprint('todo_api', __name__)

@todo_api.route('/todos', methods=['GET'])
def get_todo_list():
    conn = get_db_connection()
    # Mở cursor đặc biệt để Postgres trả về Dictionary giống như SQLite
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute('SELECT * FROM todos')
    todos_from_db = cur.fetchall()
    
    cur.close()
    conn.close()

    todos = []
    for item in todos_from_db:
        todos.append({
            "id" : item["id"],
            "task" : item["task"],
            "done" : item["done"]
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
    cur = conn.cursor()
    
    cur.execute(
        'INSERT INTO todos (task, done) VALUES (%s, %s)', (task_name,task_status)
    )
    conn.commit()
    
    cur.close()
    conn.close()

    return jsonify({
        "status" : "success",
        "message" : "Todo item added successfully"
    }), 201


@todo_api.route('/todos/<int:todo_id>', methods = ['PUT'])
def update_todo(todo_id):
    req_data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
    item = cur.fetchone()

    if item is None:
        cur.close()
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
    
    cur.execute('UPDATE todos SET task = %s, done = %s WHERE id = %s', (new_task, new_done, todo_id))
    conn.commit()
    
    cur.close()
    conn.close()

    return jsonify({
        "status" : "success",
        "message" : "item updated successfully",
        "item" : {
            "id" : todo_id,
            "task" : new_task,
            "done" : new_done
        }
    }), 200


@todo_api.route('/todos/<int:todo_id>', methods = ['DELETE'])
def delete_item(todo_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
    item = cur.fetchone()
    
    if item is None:
        cur.close()
        conn.close()
        return jsonify({
            "message" : "item not found"
        }), 404
    

    cur.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
    conn.commit()
    
    cur.close()
    conn.close()

    return jsonify({
        "status" : "success",
        "message" : "Item has been deleted"
    }), 200