import { Button } from './components/ui/button'
import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div><h1>Hello World</h1><Button onClick={() => setCount(count + 1)}>Count: {count}</Button></div>
    </>
  )
}

export default App
