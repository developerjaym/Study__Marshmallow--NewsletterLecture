import logo from './logo.svg';
import './App.css';
import {useEffect, useState} from 'react'

function App() {
  const [newsletters, setNewsletters] = useState([]);
  useEffect(()=>{
    var requestOptions = {
      method: 'GET',
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:5000/newsletters", requestOptions)
      .then(response => response.json())
      .then(fetchedNewsletters => setNewsletters(fetchedNewsletters))
      .catch(error => console.log('error', error));
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Newsletters
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Welcome to my page!
        </a>
      </header>
    {newsletters.map(newsletter => (<div key={newsletter.id}>{newsletter.title}</div>))}
    </div>
  );
}

export default App;
