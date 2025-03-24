docker run -it --rm -v ${PWD}:/app -w /app node:16-alpine sh
npm create vite@latest . -- --template vue
npm install vue@3.5.13
