FROM justadudewhohacks/opencv-nodejs

WORKDIR /app

COPY . /app

RUN npm install

ENV NODE_PATH=/usr/lib/node_modules

EXPOSE 5000

CMD ["nodemon", "app.js"]