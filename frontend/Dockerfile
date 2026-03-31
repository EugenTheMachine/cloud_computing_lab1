# Dockerfile for Lab #2
# by Yevhen Ponomarov, CS-S125

# -------- Stage 1: Build (Vite) --------
FROM node:18 AS build

WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build project (Vite → dist/)
RUN npm run build


# -------- Stage 2: Production (nginx) --------
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy Vite build output
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
