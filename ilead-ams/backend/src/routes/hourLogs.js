const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');

router.get('/', authenticate, (req, res) => {
  res.json({ message: 'Hour logs list endpoint' });
});

router.post('/', authenticate, (req, res) => {
  res.json({ message: 'Submit hour log endpoint' });
});

module.exports = router;
