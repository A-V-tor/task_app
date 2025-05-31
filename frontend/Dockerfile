FROM node:20.5.0 as build-stage

WORKDIR /app

# Копируем только файлы для установки зависимостей
COPY package*.json ./

RUN npm install

# Копируем остальные файлы
COPY . .

# Собираем приложение
RUN npm run build

# Production stage
FROM nginx:1.25 as production-stage

# Создаем директорию и копируем собранное приложение
COPY --from=build-stage /app/dist /app

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Добавляем healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
