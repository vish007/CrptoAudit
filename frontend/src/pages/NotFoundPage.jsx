import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';
import { AlertCircle } from 'lucide-react';

const NotFoundPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-simplyfi-dark-navy to-simplyfi-navy">
      <div className="text-center">
        <AlertCircle className="w-16 h-16 mx-auto mb-4 text-simplyfi-gold" />
        <h1 className="text-6xl font-bold text-white mb-2">404</h1>
        <h2 className="text-2xl font-semibold text-gray-200 mb-4">Page Not Found</h2>
        <p className="text-gray-400 mb-8 max-w-md mx-auto">
          The page you are looking for does not exist or has been moved.
        </p>
        <Link to="/dashboard">
          <Button variant="accent" size="lg">
            Return to Dashboard
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;
