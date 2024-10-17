import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import IndexMovies from './pages/IndexMovies/IndexMovies';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<IndexMovies />} />
     
      </Routes>
    </Router>
  );
};

export default App;