import { useState } from 'react'

export function Button() {
    const [count, setCount] = useState(0)
    return (
        <button style={{ margin: '3em' }} onClick={() => setCount((count) => count + 1)}>
            count is {count}
        </button>
    )
}