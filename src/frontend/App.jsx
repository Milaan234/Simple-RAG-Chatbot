import { useState, useRef, useEffect } from 'react'
import './App.css'
import UserQuestionInput from './UserQuestionInput'
import MessageTile from './MessageTile'

function App() {
  const messagesEndRef = useRef(null)
  const [messages, setMessages] = useState([
    {
      sender:'User',
      text:'What are the inputs and outputs of photosynthesis?'
    },
    {
      sender:'AI',
      text:'According to the text, the inputs of photosynthesis are six molecules of carbon dioxide, six molecules of water, and light energy. The outputs are one molecule of glucose and six molecules of oxygen.'
    },
  ])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <>
      <div>
        <div className='chatbotWrapper mt-5'>
          <div id='chatbot'>
            <h2>RAG Chatbot</h2>
            
              <div className='messagesContainer'>
                {messages.length > 0 && messages.map((message, index) => {
                  return (
                    <MessageTile key={index} message={message} />
                  )
                })}
                <div ref={messagesEndRef} />
              </div>
              
              <UserQuestionInput messages={messages} setMessages={setMessages}/>
            
          </div>
        </div>
      </div>
    </>
  )
}

export default App
