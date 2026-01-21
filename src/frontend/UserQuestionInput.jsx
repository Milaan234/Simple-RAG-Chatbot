import { useState, useRef } from 'react'
import './App.css'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function UserQuestionInput({messages, setMessages}) {
  const [userQuestion, setUserQuestion] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  function addUserQuestion() {
    setMessages(prev => [
      ...prev,
      { sender: 'User', text: userQuestion }
    ]);
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  

  async function askAI() {

    if(!userQuestion.trim()) return;
    setIsLoading(true);

    addUserQuestion()

    setMessages(prev => [
      ...prev,
      {sender: 'AI', text: 'Thinking...'}
    ]);
    
    await sleep(5000);
    try {
      
      const response = await fetch('/askAI', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userQuestion: userQuestion,
        }),
      });

      if(!response.ok) {
        console.log("error: ", response)
        setMessages(prev => [
          ...prev.slice(0, -1),
          {sender: 'AI', text: 'Error'}
        ]);
      } else {
        const data = await response.json();
        console.log(data)
        setMessages(prev => [
          ...prev.slice(0, -1),
          {sender: 'AI', text: data.ai_response}
        ]);
      }
    } catch(error) {
      setMessages(prev => [
        ...prev.slice(0, -1),
        {sender: 'AI', text: 'Error'}
      ]);
      console.log("Error fetching: ", error)
    }

    setUserQuestion("");

    setIsLoading(false);
  }

  function handleUserQuestionChange(e) {
    setUserQuestion(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
  }

  return (
    <>
      <div id='userQuestionInputArea' className='mt-3'>
        <Form onSubmit={(e) => e.preventDefault()}>
          <div className='questionInputRow'>
            <Form.Control as='textarea' id='userQuestion' rows={1} value={userQuestion} placeholder='Enter a question' onChange={handleUserQuestionChange} disabled={isLoading} />
            <Button onClick={askAI} disabled={isLoading}>Ask AI</Button>
          </div>
        </Form>
      </div>
    </>
  )
}

export default UserQuestionInput
