import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Mail, Lock, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login, isLoading, error } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [formError, setFormError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setFormError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');

    if (!formData.email || !formData.password) {
      setFormError('Please fill in all fields');
      return;
    }

    try {
      await login(formData.email, formData.password);
      toast.success('Login successful');
      navigate('/dashboard');
    } catch (err) {
      const errorMessage = err.message || 'Login failed. Please try again.';
      setFormError(errorMessage);
      toast.error(errorMessage);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-simplyfi-dark-navy to-simplyfi-navy flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center gap-2 mb-4">
            <div className="w-10 h-10 bg-simplyfi-gold rounded-lg flex items-center justify-center font-bold text-simplyfi-dark-navy">
              SF
            </div>
            <span className="text-3xl font-bold text-white">SimplyFI</span>
          </div>
          <h1 className="text-xl text-gray-200">Proof of Reserves Audit Platform</h1>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-simplyfi-text-dark mb-6">Sign In</h2>

          {/* Error Alert */}
          {(formError || error) && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-simplyfi-red-warning flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-simplyfi-red-warning">{formError || error}</p>
              </div>
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Input */}
            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-simplyfi-text-muted" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                  className="form-input pl-10"
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Password Input */}
            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-simplyfi-text-muted" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  className="form-input pl-10"
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 text-sm text-simplyfi-text-muted cursor-pointer">
                <input type="checkbox" className="rounded" />
                Remember me
              </label>
              <Link to="/auth/forgot-password" className="text-sm link-primary">
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              isLoading={isLoading}
              disabled={isLoading}
              className="mt-6"
            >
              Sign In
            </Button>
          </form>

          {/* Divider */}
          <div className="my-6 relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-simplyfi-border-light" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-simplyfi-text-muted">or</span>
            </div>
          </div>

          {/* Sign Up Link */}
          <p className="text-center text-simplyfi-text-muted text-sm">
            Don't have an account?{' '}
            <Link to="/auth/register" className="link-primary">
              Sign up
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-gray-400 text-xs mt-8">
          Banking-grade security for professional crypto audits
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
