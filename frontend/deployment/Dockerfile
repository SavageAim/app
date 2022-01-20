# Build image
FROM node:16

WORKDIR /savage-aim

COPY . .

# Install the stuff and build it
RUN npm install && npm run build

# NGINX image for serving static content
FROM nginx:latest

RUN rm /usr/share/nginx/html/*

COPY --from=0 /savage-aim/dist /usr/share/nginx/html

COPY deployment/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
