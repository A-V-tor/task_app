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
    <div class="max-w-[1200px] mx-auto p-2 sm:p-4 w-full">
        <section class="py-4">
            <h2 class="font-stretch-semi-expanded font-extrabold from-neutral-950 text-3xl sm:text-4xl md:text-5xl text-center">
                Текущие задачи
            </h2>
        </section>

        <section class="py-4">
            <div class="flex flex-col items-center gap-4">
                <div class="w-full max-w-[400px]">
                    <input
                        v-model="newTaskTitle"
                        type="text"
                        placeholder="Заголовок задачи"
                        :disabled="isSubmitting"
                        class="w-full py-2 px-4 border border-gray-300 rounded-md text-sm sm:text-base focus:outline-none focus:border-gray-400 text-center placeholder:text-center"
                    />
                </div>
                <button
                    @click="createTask"
                    :disabled="isSubmitting || !newTaskTitle.trim()"
                    class="px-4 sm:px-6 py-2 bg-green-600 text-white border-none rounded-md cursor-pointer text-sm sm:text-base transition-colors hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                    {{ isSubmitting ? "Добавление..." : "Добавить" }}
                </button>
            </div>
        </section>

        <div v-if="loading" class="text-center p-4 sm:p-8 text-gray-500">Загрузка задач...</div>

        <div v-else-if="error" class="text-red-300 text-center p-4">
            {{ error }}
        </div>
        <div v-else-if="tasks.length === 0" class="text-red-300 text-center p-4">Задачи не найдены</div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4 md:gap-6 p-2 sm:p-4">
            <div
                v-for="task in tasks"
                :key="task.id"
                class="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 text-center w-full h-auto min-h-[180px] sm:min-h-[200px] flex flex-col justify-between"
            >
                <div class="h-full flex flex-col justify-between">
                    <h3 class="mb-4 sm:mb-6 text-base sm:text-lg overflow-hidden text-ellipsis line-clamp-4">
                        {{ task.title }}
                    </h3>
                    <div class="space-y-2">
                        <span
                            :class="[
                                'inline-block px-2 py-1 rounded text-xs sm:text-sm w-full box-border bg-amber-50 text-amber-800',
                                task.completed
                                    ? 'inline-block px-2 py-1 rounded text-xs sm:text-sm w-full box-border bg-green-50 text-green-800'
                                    : '',
                            ]"
                        >
                            {{ task.completed ? 'Выполнено' : 'В процессе' }}
                        </span>
                        <button
                            @click="deleteTask(task.id)"
                            class="w-full px-3 py-1 bg-red-600 text-white border-none rounded cursor-pointer text-xs sm:text-sm transition-colors hover:bg-red-700"
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
/* Удаляем стили h2, так как они теперь в Tailwind классах */
</style>
