const express = require('express');
const router = express.Router();

router.post('/make', (req, res) => {
  res.json({ message: 'Make.com webhook endpoint' });
});

router.get('/status', (req, res) => {
  res.json({ message: 'Webhook status endpoint' });
});

module.exports = router;
