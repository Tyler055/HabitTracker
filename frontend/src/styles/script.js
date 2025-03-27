export const toggleTheme = (isDarkMode, setIsDarkMode) => {
    setIsDarkMode((prev) => !prev);
  };
  
  export const addHabit = async (habitName) => {
    try {
      const response = await fetch("/api/add-habit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: habitName }),
      });
  
      if (response.ok) {
        return await response.json();
      } else {
        throw new Error("Failed to add habit.");
      }
    } catch (error) {
      alert(error.message);
    }
  };
  