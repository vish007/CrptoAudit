import { useSelector, useDispatch } from 'react-redux';
import { useCallback, useEffect } from 'react';
import {
  selectUser,
  selectToken,
  selectIsAuthenticated,
  selectIsLoading,
  selectError,
  selectUserRole,
  selectUserPermissions,
  login,
  logout,
  refreshToken as refreshTokenAction,
} from '../store/slices/authSlice';
import { SESSION_TIMEOUT, TOKEN_REFRESH_THRESHOLD } from '../utils/constants';

/**
 * Custom hook for authentication state and actions
 * @returns {Object} Auth state and methods
 */
export const useAuth = () => {
  const dispatch = useDispatch();

  const user = useSelector(selectUser);
  const token = useSelector(selectToken);
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const isLoading = useSelector(selectIsLoading);
  const error = useSelector(selectError);
  const userRole = useSelector(selectUserRole);
  const userPermissions = useSelector(selectUserPermissions);

  const handleLogin = useCallback(
    (email, password) => {
      return dispatch(login({ email, password }));
    },
    [dispatch]
  );

  const handleLogout = useCallback(() => {
    return dispatch(logout());
  }, [dispatch]);

  const handleRefreshToken = useCallback(() => {
    return dispatch(refreshTokenAction());
  }, [dispatch]);

  // Auto refresh token before expiration
  useEffect(() => {
    if (!isAuthenticated || !token) return;

    const interval = setInterval(() => {
      const expirationTime = new Date(localStorage.getItem('tokenExpiration'));
      const now = new Date();
      const timeUntilExpiration = expirationTime - now;

      if (timeUntilExpiration < TOKEN_REFRESH_THRESHOLD && timeUntilExpiration > 0) {
        dispatch(refreshTokenAction());
      }
    }, 60000); // Check every minute

    return () => clearInterval(interval);
  }, [isAuthenticated, token, dispatch]);

  // Auto logout after session timeout
  useEffect(() => {
    if (!isAuthenticated) return;

    let timeout;
    const resetTimeout = () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        dispatch(logout());
      }, SESSION_TIMEOUT);
    };

    const events = ['mousedown', 'keydown', 'scroll', 'touchstart'];

    events.forEach((event) => {
      document.addEventListener(event, resetTimeout);
    });

    resetTimeout();

    return () => {
      events.forEach((event) => {
        document.removeEventListener(event, resetTimeout);
      });
      clearTimeout(timeout);
    };
  }, [isAuthenticated, dispatch]);

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    userRole,
    userPermissions,
    login: handleLogin,
    logout: handleLogout,
    refreshToken: handleRefreshToken,
  };
};

export default useAuth;
