FROM node:16-alpine as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

FROM node:16-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=build /app/build /app
CMD ["serve", "-s", ".", "-l", "3000"]

EXPOSE 3000
