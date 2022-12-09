FROM node:18.12 AS build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build


FROM node:18.12

WORKDIR /app
COPY --from=build /app/package.json .
RUN npm install --omit=dev

COPY --from=build /app/build .

EXPOSE 3000
CMD ["node", "./index.js"]
