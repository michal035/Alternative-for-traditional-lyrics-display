FROM node:14-alpine

WORKDIR /APP/FRONTEND

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev"]
