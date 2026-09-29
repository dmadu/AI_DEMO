const express = require('express');
const router = express.Router();
const User = require('../models/User');
const authMiddleware = require('../middleware/auth');

// GET /api/dashboard - protected endpoint returning authenticated user profile
router.get('/', authMiddleware, async (req, res) => {
  try {
    // req.user is expected to be populated by authMiddleware (e.g. { userId: ... } or user object)
    const userId = req.user.userId || req.user.id;
    const user = await User.findById(userId).select('username email');
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.status(200).json({
      username: user.username,
      email: user.email
    });
  } catch (error) {
    res.status(500).json({ error: 'Server error', details: error.message });
  }
});

module.exports = router;
