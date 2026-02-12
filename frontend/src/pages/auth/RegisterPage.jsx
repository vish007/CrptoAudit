import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Button from '../../components/common/Button';

const RegisterPage = () => {
  const navigate = useNavigate();

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
          <h2 className="text-2xl font-bold text-simplyfi-text-dark mb-6">Create Account</h2>

          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Full Name
              </label>
              <input type="text" placeholder="John Doe" className="form-input" />
            </div>

            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Email Address
              </label>
              <input type="email" placeholder="you@example.com" className="form-input" />
            </div>

            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Password
              </label>
              <input type="password" placeholder="••••••••" className="form-input" />
            </div>

            <Button variant="primary" size="lg" fullWidth className="mt-6">
              Create Account
            </Button>
          </form>

          <p className="text-center text-simplyfi-text-muted text-sm mt-6">
            Already have an account?{' '}
            <Link to="/auth/login" className="link-primary">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
