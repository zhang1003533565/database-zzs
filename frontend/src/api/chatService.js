// src/api/chatService.js
import axios from 'axios'

export async function sendChat(input, history = []) {
  const res = await axios.post('http://localhost:8000/api/chat/', {
    input,
    history
  })
  return res.data
}
