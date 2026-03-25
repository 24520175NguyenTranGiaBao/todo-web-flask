const API_URL = "https://todo-web-svs3.onrender.com/api/todos";
const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');
const themeSwitch = document.getElementById('theme-switch');

// Dark Mode Toggle
themeSwitch.onclick = () => {
    document.body.classList.toggle('dark-theme');
    const isDark = document.body.classList.contains('dark-theme');
    themeSwitch.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
};

// Khôi phục theme cũ
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-theme');
    themeSwitch.innerHTML = '<i class="fas fa-sun"></i>';
}

// Gọi API lấy dữ liệu
async function fetchTodos() {
    const res = await fetch(API_URL);
    const data = await res.json();
    render(data.todos);
}

function render(todos) {
    todoList.innerHTML = '';
    todos.forEach(t => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="task-content ${t.done ? 'done' : ''}">
                <input type="checkbox" id="check-${t.id}" style="display:none" ${t.done ? 'checked' : ''} onchange="toggle(${t.id}, ${t.done})">
                <label for="check-${t.id}" class="custom-cb"></label>
                <span>${t.task}</span>
            </div>
            <i class="fas fa-trash" onclick="del(${t.id})"></i>
        `;
        todoList.appendChild(li);
    });
}

// Thêm, Sửa, Xóa
addBtn.onclick = async () => {
    if (!input.value) return;
    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: input.value, done: false })
    });
    input.value = '';
    fetchTodos();
};

async function toggle(id, status) {
    await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done: !status })
    });
    fetchTodos();
}

async function del(id) {
    if (confirm("Xóa nhé?")) {
        await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        fetchTodos();
    }
}

fetchTodos();