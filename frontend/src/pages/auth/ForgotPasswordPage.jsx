import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../../components/common/Button';

const ForgotPasswordPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-simplyfi-dark-navy to-simplyfi-navy flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center gap-2 mb-4">
            <div className="w-10 h-10 bg-simplyfi-gold rounded-lg flex items-center justify-center font-bold text-simplyfi-dark-navy">
              SF
            </div>
            <span className="text-3xl font-bold text-white">SimplyFI</span>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-simplyfi-text-dark mb-2">Reset Password</h2>
          <p className="text-simplyfi-text-muted text-sm mb-6">
            Enter your email to receive password reset instructions
          </p>

          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Email Address
              </label>
              <input type="email" placeholder="you@example.com" className="form-input" />
            </div>

            <Button variant="primary" size="lg" fullWidth className="mt-6">
              Send Reset Link
            </Button>
          </form>

          <p className="text-center text-simplyfi-text-muted text-sm mt-6">
            <Link to="/auth/login" className="link-primary">
              Back to login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
