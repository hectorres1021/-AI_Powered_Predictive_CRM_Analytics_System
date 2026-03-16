const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');

router.get('/dashboard', authenticate, (req, res) => {
  res.json({ message: 'Dashboard analytics endpoint' });
});

module.exports = router;
