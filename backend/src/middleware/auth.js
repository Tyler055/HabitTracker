const jwt = require("jsonwebtoken");

const authMiddleware = (req, res, next) => {
  // Try both standard headers
  const bearerHeader = req.headers["authorization"];
  const xAuthToken = req.header("x-auth-token");

  // Prefer "Authorization: Bearer <token>" if available
  let token = null;
  if (bearerHeader && bearerHeader.startsWith("Bearer ")) {
    token = bearerHeader.slice(7);
  } else if (xAuthToken) {
    token = xAuthToken;
  }

  if (!token) {
    return res.status(401).json({ msg: "No token, authorization denied" });
  }

  try {
    // Decode token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded.user || decoded; // Support both formats
    next();
  } catch (err) {
    return res.status(401).json({ msg: "Token is not valid" });
  }
};

module.exports = authMiddleware;
