const express = require('express');
const router = express.Router();
const { authenticate } = require('../middleware/auth');

router.get('/', authenticate, (req, res) => {
  res.json({ message: 'Apprentices list endpoint' });
});

router.post('/', authenticate, (req, res) => {
  res.json({ message: 'Create apprentice endpoint' });
});

module.exports = router;
