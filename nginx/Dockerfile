# --- 1) Build del frontend ---
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend .
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
RUN npm run build             # genera /app/dist

# --- 2) Nginx sirve estáticos + proxys API ---
FROM nginx:alpine
# 2.1) Copiamos el build del front
COPY --from=builder /app/dist /usr/share/nginx/html
# 2.2) Configuración custom
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]
