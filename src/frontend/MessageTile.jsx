import { useState } from 'react'
import './App.css'

function MessageTile({message}) {

  return (
    <>
      <div className={message.sender === 'User' ? 'userMessage' : 'AIMessage'}>
        {message.text}
      </div>
    </>
  )
}

export default MessageTile
