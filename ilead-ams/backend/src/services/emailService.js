const nodemailer = require('nodemailer');

// Email templates
const templates = {
  welcomeUser: (name, email, tempPassword) => ({
    subject: 'Welcome to I-LEAD AMS',
    html: `
      <h2>Welcome to I-LEAD Apprenticeship Management System</h2>
      <p>Dear ${name},</p>
      <p>Your account has been created. Here are your login credentials:</p>
      <ul>
        <li><strong>Email:</strong> ${email}</li>
        <li><strong>Temporary Password:</strong> ${tempPassword}</li>
      </ul>
      <p>Please log in and update your password immediately.</p>
      <p><strong>Account Status:</strong> Pending administrator approval</p>
      <p>You will be notified when your account is approved.</p>
    `
  }),

  accountApproved: (name) => ({
    subject: 'Your I-LEAD AMS Account Has Been Approved',
    html: `
      <h2>Account Approved</h2>
      <p>Dear ${name},</p>
      <p>Your I-LEAD AMS account has been approved and is now active.</p>
      <p>You can now log in and start using the system.</p>
      <p><strong>Reminder:</strong> Your account was approved, so you should change your temporary password to a secure password you choose.</p>
    `
  }),

  hourSubmitted: (apprenticeName, supervisorName) => ({
    subject: 'New Hours Submitted for Review',
    html: `
      <h2>Hours Submitted</h2>
      <p>Dear ${supervisorName},</p>
      <p><strong>${apprenticeName}</strong> has submitted hours for your review in the I-LEAD AMS.</p>
      <p>Please log in to review and approve/reject the submission.</p>
    `
  }),

  hourApproved: (apprenticeName, hours, score) => ({
    subject: 'Your Hours Have Been Approved',
    html: `
      <h2>Hours Approved</h2>
      <p>Dear ${apprenticeName},</p>
      <p>Your hour submission has been approved!</p>
      <ul>
        <li><strong>Hours:</strong> ${hours}</li>
        <li><strong>Competency Score:</strong> ${score}/5</li>
      </ul>
      <p>Your progress has been updated in the system.</p>
    `
  }),

  hourRejected: (apprenticeName, reason) => ({
    subject: 'Your Hours Need Revision',
    html: `
      <h2>Hours Rejected</h2>
      <p>Dear ${apprenticeName},</p>
      <p>Your hour submission has been returned for revision.</p>
      <p><strong>Reason:</strong> ${reason}</p>
      <p>Please review and resubmit.</p>
    `
  }),

  passwordReset: (resetLink) => ({
    subject: 'Reset Your I-LEAD AMS Password',
    html: `
      <h2>Password Reset Request</h2>
      <p>You requested to reset your password. Click the link below to create a new password:</p>
      <p><a href="${resetLink}">Reset Password</a></p>
      <p><strong>Note:</strong> This link will expire in 24 hours.</p>
      <p>If you did not request this, please ignore this email.</p>
    `
  })
};

class EmailService {
  constructor() {
    this.transporter = null;
    this.initializeTransporter();
  }

  initializeTransporter() {
    // Try to use SendGrid if API key is available
    if (process.env.SENDGRID_API_KEY) {
      const sgTransport = require('nodemailer-sendgrid-transport');
      this.transporter = nodemailer.createTransport(
        sgTransport({
          auth: {
            api_key: process.env.SENDGRID_API_KEY
          }
        })
      );
      console.log('📧 Email service initialized with SendGrid');
      return;
    }

    // Fall back to SMTP (Gmail or custom SMTP server)
    if (process.env.SMTP_HOST) {
      this.transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: process.env.SMTP_PORT || 587,
        secure: process.env.SMTP_PORT === '465', // true for 465, false for other ports
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS
        }
      });
      console.log('📧 Email service initialized with SMTP');
      return;
    }

    // Development: log to console instead
    console.log('⚠️  Email service in development mode (logs to console)');
    this.isDevelopment = true;
  }

  async send(to, templateName, templateData) {
    try {
      if (!templates[templateName]) {
        throw new Error(`Email template "${templateName}" not found`);
      }

      const template = templates[templateName](...templateData);
      const from = process.env.SMTP_FROM || 'noreply@i-leadusa.org';

      // Development mode: log instead of send
      if (this.isDevelopment) {
        console.log(`\n📧 Email (Development Mode):`);
        console.log(`   To: ${to}`);
        console.log(`   Subject: ${template.subject}`);
        console.log(`   Body: ${template.html.substring(0, 200)}...`);
        return { messageId: 'dev-' + Date.now() };
      }

      if (!this.transporter) {
        console.warn('Email transporter not configured, skipping email send');
        return { messageId: null };
      }

      const result = await this.transporter.sendMail({
        from,
        to,
        subject: template.subject,
        html: template.html
      });

      console.log(`✅ Email sent to ${to}: ${result.messageId}`);
      return result;
    } catch (err) {
      console.error(`❌ Email send failed for ${to}:`, err.message);
      throw err;
    }
  }

  // Specific email methods
  async sendWelcomeEmail(email, name, tempPassword) {
    return this.send(email, 'welcomeUser', [name, email, tempPassword]);
  }

  async sendApprovedEmail(email, name) {
    return this.send(email, 'accountApproved', [name]);
  }

  async sendHourSubmittedEmail(supervisorEmail, supervisorName, apprenticeName) {
    return this.send(supervisorEmail, 'hourSubmitted', [apprenticeName, supervisorName]);
  }

  async sendHourApprovedEmail(apprenticeEmail, apprenticeName, hours, score) {
    return this.send(apprenticeEmail, 'hourApproved', [apprenticeName, hours, score]);
  }

  async sendHourRejectedEmail(apprenticeEmail, apprenticeName, reason) {
    return this.send(apprenticeEmail, 'hourRejected', [apprenticeName, reason]);
  }

  async sendPasswordResetEmail(email, resetLink) {
    return this.send(email, 'passwordReset', [resetLink]);
  }
}

module.exports = new EmailService();
