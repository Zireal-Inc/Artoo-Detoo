// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import { Header } from "../components/Header"
// import './App.css'
// import '@mc/ui/src/style/index.css';
// import { Button } from "@rd/ui/src/componenets/ui/button"
// import * as abc from "../../"
import { Button } from "../../../../../packages/ui/src/components/ui/button"

function App() {
	// const [count, setCount] = useState(0)

	return (
		<div className="dark:bg-white">
			<Header/>
			<Button variant={'default'}>Shared button</Button>
		</div>
	)
}

export default App
