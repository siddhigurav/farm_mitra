# Stage 1: Build the React application
FROM node:16-alpine as builder

WORKDIR /app

COPY ./insect_monitoring_system/frontend/package.json /app/package.json
COPY ./insect_monitoring_system/frontend/package-lock.json /app/package-lock.json

RUN npm install

COPY ./insect_monitoring_system/frontend /app

RUN npm run build

# Stage 2: Serve the built application with Nginx
FROM nginx:1.21-alpine

COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx config if you have one
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
