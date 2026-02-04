document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('taskInput');
    const addBtn = document.getElementById('addBtn');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const taskList = document.getElementById('taskList');
    const emptyMessage = document.getElementById('emptyMessage');

    let tasks = [];

    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    function loadTasksFromHTML() {
        const stored = localStorage.getItem('tasks');
        if (stored) {
            try {
                tasks = JSON.parse(stored) || [];
                return;
            } catch (e) {
                tasks = [];
            }
        }

        const existingLi = Array.from(taskList.querySelectorAll('li'));
        if (existingLi.length === 0) return;

        const parsed = [];
        existingLi.forEach(li => {
            const text = li.textContent || '';
            const parts = text.split(/\d+\.|\n/).map(p => p.trim()).filter(Boolean);
            if (parts.length > 0) {
                parts.forEach(p => parsed.push({ text: p, completed: false }));
            }
        });

        tasks = parsed;
        saveTasks();
    }

    function renderTasks(filter = '') {
        taskList.innerHTML = '';
        const normalizedFilter = filter.trim().toLowerCase();
        const shown = tasks
            .map((t, i) => ({ task: t, idx: i }))
            .filter(item => {
                const text = typeof item.task === 'string' ? item.task : (item.task.text || '');
                return text.toLowerCase().includes(normalizedFilter);
            });

        if (shown.length === 0) {
            emptyMessage.style.display = 'block';
        } else {
            emptyMessage.style.display = 'none';
        }

        shown.forEach(item => {
            const li = document.createElement('li');
            li.className = 'task-item';
            if (item.task.completed) {
                li.classList.add('completed');
            }

            const textSpan = document.createElement('span');
            textSpan.textContent = item.task.text || item.task;

            const actions = document.createElement('div');
            actions.className = 'task-actions';

            const completeBtn = document.createElement('button');
            completeBtn.textContent = item.task.completed ? '↩️' : '✓';
            completeBtn.className = 'complete-btn';

            completeBtn.addEventListener('click', () => {
                completeTask(item.idx);
            });

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = '🗑️';
            deleteBtn.className = 'delete-btn';

            deleteBtn.addEventListener('click', () => {
                removeTask(item.idx);
            });

            actions.appendChild(completeBtn);
            actions.appendChild(deleteBtn);
            li.appendChild(textSpan);
            li.appendChild(actions);
            taskList.appendChild(li);
        });
    }

    function addTask(text) {
        const t = text.trim();
        if (t === '') return;
        tasks.push({ text: t, completed: false });
        saveTasks();
        renderTasks(searchInput.value);
        taskInput.value = '';
        taskInput.focus();
    }

    function completeTask(index) {
        if (index < 0 || index >= tasks.length) return;
        tasks[index].completed = !tasks[index].completed;
        saveTasks();
        renderTasks(searchInput.value);
    }

    function removeTask(index) {
        if (index < 0 || index >= tasks.length) return;
        tasks.splice(index, 1);
        saveTasks();
        renderTasks(searchInput.value);
    }

    function handleSearch() {
        renderTasks(searchInput.value);
    }


    addBtn.addEventListener('click', () => addTask(taskInput.value));
    taskInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') addTask(taskInput.value);
    });

    // show/hide clear button based on existing input
    clearSearchBtn.style.display = (searchInput.value && searchInput.value.trim() !== '') ? 'inline-block' : 'none';

    // Live search as the user types. If input is empty, show full list and hide clear button.
    searchInput.addEventListener('input', () => {
        const val = searchInput.value;
        if (val.trim() === '') {
            clearSearchBtn.style.display = 'none';
            renderTasks();
        } else {
            clearSearchBtn.style.display = 'inline-block';
            renderTasks(val);
        }
    });

    // Enter to search, Escape to clear immediately
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleSearch();
        if (e.key === 'Escape') {
            searchInput.value = '';
            clearSearchBtn.style.display = 'none';
            renderTasks();
        }
    });

    searchBtn.addEventListener('click', handleSearch);

    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        clearSearchBtn.style.display = 'none';
        renderTasks();
    });

    loadTasksFromHTML();
    renderTasks();
});
