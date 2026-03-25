const API_URL = "https://todo-web-svs3.onrender.com/api/todos";
const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');

// lấy danh sách từ Cloud
async function fetchTodos() {
    const res = await fetch(API_URL);
    const data = await res.json();
    renderTodos(data.todos);
}

// Hiển thị lên màn hình
function renderTodos(todos) {
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="${todo.done ? 'done' : ''}">${todo.task}</span>
            <div class="actions">
                <i class="fas fa-check" onclick="toggleTodo(${todo.id}, ${todo.done})"></i>
                <i class="fas fa-trash" onclick="deleteTodo(${todo.id})"></i>
            </div>
        `;
        todoList.appendChild(li);
    });
}

// Thêm mới
addBtn.onclick = async () => {
    const task = input.value;
    if (!task) return;
    
    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task, done: false })
    });
    input.value = '';
    fetchTodos();
};

// Cập nhật trạng thái (Sửa)
async function toggleTodo(id, currentStatus) {
    await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done: !currentStatus })
    });
    fetchTodos();
}

// Xóa
async function deleteTodo(id) {
    if (!confirm("Xóa nhé?")) return;
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchTodos();
}

fetchTodos();