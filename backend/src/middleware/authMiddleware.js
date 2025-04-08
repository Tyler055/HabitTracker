const jwt = require("jsonwebtoken");

const authMiddleware = async (req, res, next) => {
  const token = req.cookies.token;

  if (!token) {
    return res.status(401).json({ message: "Not authenticated" });
  }

  try {
    // Validate the JWT token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // Attach user data to the request object

    // Optionally, fetch user details from the database
    const [rows] = await db.execute("SELECT * FROM users WHERE id = ?", [
      decoded.id,
    ]);

    if (rows.length === 0) {
      return res.status(401).json({ message: "User not found" });
    }

    req.userDetails = rows[0]; // Add user details to the request object
    next(); // Continue to the next middleware or route handler
  } catch (err) {
    console.error(err);
    res.status(403).json({ message: "Invalid or expired token" });
  }
};

module.exports = authMiddleware;
