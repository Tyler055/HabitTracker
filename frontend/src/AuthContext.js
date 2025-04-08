const { createContext, useContext, useState } = require("react");

const AuthContext = createContext();

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem("token", userData.token); // Store token in localStorage
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("token"); // Remove token from localStorage
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Export the context and the hook
module.exports = {
  AuthProvider,
  useAuth
};
