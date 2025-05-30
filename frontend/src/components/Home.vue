<script setup>
import { ref, onMounted } from "vue";

const tasks = ref([]);
const loading = ref(true);
const error = ref(null);
const newTaskTitle = ref("");
const isSubmitting = ref(false);

const fetchTasks = async () => {
    try {
        const response = await fetch("/api/tasks", {
            method: "GET",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        });
        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }
        tasks.value = await response.json();
    } catch (e) {
        error.value = e.message;
        console.error("Что-то пошло не так:", e);
    } finally {
        loading.value = false;
    }
};

const createTask = async () => {
    if (!newTaskTitle.value.trim()) return;

    isSubmitting.value = true;
    try {
        const response = await fetch("/api/tasks", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ title: newTaskTitle.value }),
        });

        if (!response.ok) {
            throw new Error("Ошибка при создании задачи!");
        }

        newTaskTitle.value = "";
        await fetchTasks(); // Обновляем список задач
    } catch (e) {
        error.value = e.message;
        console.error("Что-то пошло не так:", e);
    } finally {
        isSubmitting.value = false;
    }
};

const deleteTask = async (taskId) => {
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: "DELETE",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error("Ошибка при удалении задачи!");
        }

        await fetchTasks(); // Обновляем список задач после удаления
    } catch (e) {
        error.value = e.message;
        console.error("Что-то пошло не так:", e);
    }
};

onMounted(() => {
    fetchTasks();
});
</script>

<template>
    <div class="tasks-container">
        <h2>Tasks</h2>

        <form @submit.prevent="createTask" class="task-form">
            <input
                v-model="newTaskTitle"
                type="text"
                placeholder="Заголовок задачи"
                :disabled="isSubmitting"
                class="task-input"
            />
            <button
                type="submit"
                :disabled="isSubmitting || !newTaskTitle.trim()"
                class="task-submit"
            >
                {{ isSubmitting ? "Добавление..." : "Добавить" }}
            </button>
        </form>
        <h1 class="text-3xl font-bold underline text-blue-500">Hello world!</h1>
        <div v-if="loading" class="loading-message">Loading tasks...</div>

        <div v-else-if="error" class="error-message">
            {{ error }}
        </div>
        <div v-else-if="tasks.length === 0" class="no-tasks-message">No tasks found</div>
        <div v-else class="tasks-list">
            <div v-for="task in tasks" :key="task.id" class="task-item">
                <div class="task-content">
                    <h3>{{ task.title }}</h3>
                    <div class="task-meta">
                        <span :class="['status', task.completed ? 'completed' : '']">
                            {{ task.completed }}
                        </span>
                        <button
                            @click="deleteTask(task.id)"
                            class="delete-button"
                            title="Удалить задачу"
                        >
                            Удалить
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.tasks-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem;
    width: 100%;
}

h2 {
    text-align: center;
    margin-bottom: 2rem;
}

.task-form {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.task-input {
    flex: 1;
    padding: 0.5rem 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.task-input:focus {
    outline: none;
    border-color: #999;
}

.task-submit {
    padding: 0.5rem 1.5rem;
    background: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
}

.task-submit:hover:not(:disabled) {
    background: #45a049;
}

.task-submit:disabled {
    background: #cccccc;
    cursor: not-allowed;
}

.tasks-list {
    display: grid;
    grid-template-columns: repeat(4, 280px);
    gap: 1.5rem;
    padding: 1rem;
    justify-content: center;
}

.task-item {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    width: 280px;
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.task-content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.task-content h3 {
    margin: 0 0 1.5rem 0;
    font-size: 1.2rem;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
}

.task-meta {
    margin-top: auto;
}

.status {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
    width: 100%;
    box-sizing: border-box;
}

.status.completed {
    background: #e6ffe6;
    color: #006600;
}

.status:not(.completed) {
    background: #fff3e6;
    color: #cc6600;
}

.loading-message,
.error-message,
.no-tasks-message {
    text-align: center;
    padding: 2rem;
    color: #666;
}

.error-message {
    color: #dc2626;
    background: #fee2e2;
    border-radius: 0.5rem;
}

.delete-button {
    margin-top: 0.5rem;
    padding: 0.25rem 0.75rem;
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: background-color 0.2s;
    width: 100%;
}

.delete-button:hover {
    background: #b91c1c;
}

@media (max-width: 1200px) {
    .tasks-list {
        grid-template-columns: repeat(3, 280px);
    }
}

@media (max-width: 992px) {
    .tasks-list {
        grid-template-columns: repeat(2, 280px);
    }
}

@media (max-width: 768px) {
    .tasks-list {
        grid-template-columns: 280px;
    }

    .task-form {
        flex-direction: column;
    }
}
</style>
