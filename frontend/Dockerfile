# build stage
FROM node:gallium-slim as build-stage
WORKDIR /app
COPY package*.json ./
COPY vue.config.js .
COPY babel.config.js .
COPY public ./public
COPY src ./src

RUN npm install

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]