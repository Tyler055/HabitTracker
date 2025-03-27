import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TaskBar from "./components/TaskBar";
import HabitTracker from "./pages/HabitTracker";
import Home from "./pages/Home";
import Page1 from "./pages/Page1";
import Page2 from "./pages/Page2";
import Page3 from "./pages/Page3";

const App = () => {
  return (
    <BrowserRouter>
      <TaskBar />
      <div style={{ marginTop: "60px" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/tracker" element={<HabitTracker />} />
          <Route path="/page1" element={<Page1 />} />
          <Route path="/page2" element={<Page2 />} />
          <Route path="/page3" element={<Page3 />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
