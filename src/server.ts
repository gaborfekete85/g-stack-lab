import { createApp } from './app'

const port = Number(process.env.PORT ?? 3000)
const app = createApp()

Bun.serve({ port, fetch: app.fetch })
console.log(`g-stack-lab on http://localhost:${port}`)
