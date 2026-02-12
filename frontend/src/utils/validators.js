export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password) => {
  if (!password || password.length < 8) return false;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpecialChar = /[@$!%*?&]/.test(password);
  return hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar;
};

export const validatePhoneNumber = (phone) => {
  const phoneRegex = /^\+?[\d\s\-()]{7,}$/;
  return phoneRegex.test(phone);
};

export const validateCryptoAddress = (address) => {
  if (!address) return false;
  return /^0x[a-fA-F0-9]{40}$/.test(address) || /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$/.test(address);
};

export const validateEthereumAddress = (address) => {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
};

export const validateBitcoinAddress = (address) => {
  return /^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$/.test(address);
};

export const validateURL = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

export const validateJSON = (str) => {
  try {
    JSON.parse(str);
    return true;
  } catch {
    return false;
  }
};

export const validateNumber = (value) => {
  return !isNaN(parseFloat(value)) && isFinite(value);
};

export const validatePositiveNumber = (value) => {
  return validateNumber(value) && parseFloat(value) >= 0;
};

export const validateNonZeroNumber = (value) => {
  return validateNumber(value) && parseFloat(value) !== 0;
};

export const validateDecimalPlaces = (value, places) => {
  if (!validateNumber(value)) return false;
  const decimalPart = value.toString().split('.')[1];
  return !decimalPart || decimalPart.length <= places;
};

export const validateHexString = (str) => {
  return /^[0-9a-fA-F]*$/.test(str);
};

export const validateHash = (hash, type = 'sha256') => {
  const lengths = {
    sha256: 64,
    sha512: 128,
    md5: 32,
  };

  const expectedLength = lengths[type];
  if (!expectedLength) return false;

  return hash.length === expectedLength && validateHexString(hash);
};

export const validateFileSize = (fileSize, maxSizeMB) => {
  return fileSize <= maxSizeMB * 1024 * 1024;
};

export const validateFileType = (fileName, allowedTypes) => {
  const fileExtension = fileName.split('.').pop().toLowerCase();
  return allowedTypes.includes(fileExtension);
};

export const validateMimeType = (mimeType, allowedTypes) => {
  return allowedTypes.includes(mimeType);
};

export const validateUsername = (username) => {
  const usernameRegex = /^[a-zA-Z0-9_-]{3,20}$/;
  return usernameRegex.test(username);
};

export const validateIPAddress = (ip) => {
  const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return ipRegex.test(ip);
};

export const validateMerkleRoot = (hash) => {
  return validateHash(hash, 'sha256');
};

export const validateDate = (date) => {
  return date instanceof Date && !isNaN(date);
};

export const validateDateString = (dateStr, format = 'YYYY-MM-DD') => {
  try {
    const date = new Date(dateStr);
    return !isNaN(date.getTime());
  } catch {
    return false;
  }
};

export const validateDateRange = (startDate, endDate) => {
  if (!validateDate(startDate) || !validateDate(endDate)) return false;
  return startDate < endDate;
};

export const validateUUID = (uuid) => {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
};

export const validateCIDR = (cidr) => {
  const cidrRegex = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
  return cidrRegex.test(cidr);
};

export const validateCompanyName = (name) => {
  return name && name.length >= 2 && name.length <= 255;
};

export const validateDomain = (domain) => {
  const domainRegex = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i;
  return domainRegex.test(domain);
};

export const createValidator = (rules) => {
  return (data) => {
    const errors = {};

    Object.keys(rules).forEach((field) => {
      const fieldRules = rules[field];
      const value = data[field];

      if (Array.isArray(fieldRules)) {
        fieldRules.forEach((rule) => {
          const error = rule(value, data);
          if (error) {
            errors[field] = error;
          }
        });
      } else if (typeof fieldRules === 'function') {
        const error = fieldRules(value, data);
        if (error) {
          errors[field] = error;
        }
      }
    });

    return {
      isValid: Object.keys(errors).length === 0,
      errors,
    };
  };
};

export const required = (fieldName = 'This field') => {
  return (value) => {
    if (!value || (typeof value === 'string' && !value.trim())) {
      return `${fieldName} is required`;
    }
    return null;
  };
};

export const minLength = (min, fieldName = 'This field') => {
  return (value) => {
    if (value && value.length < min) {
      return `${fieldName} must be at least ${min} characters`;
    }
    return null;
  };
};

export const maxLength = (max, fieldName = 'This field') => {
  return (value) => {
    if (value && value.length > max) {
      return `${fieldName} must be at most ${max} characters`;
    }
    return null;
  };
};

export const email = (fieldName = 'Email') => {
  return (value) => {
    if (value && !validateEmail(value)) {
      return `${fieldName} must be a valid email address`;
    }
    return null;
  };
};

export const password = (fieldName = 'Password') => {
  return (value) => {
    if (value && !validatePassword(value)) {
      return `${fieldName} must contain uppercase, lowercase, number, and special character`;
    }
    return null;
  };
};

export const match = (fieldToMatch, fieldName = 'This field') => {
  return (value, allData) => {
    if (value !== allData[fieldToMatch]) {
      return `${fieldName} does not match`;
    }
    return null;
  };
};

export const customPattern = (pattern, message) => {
  return (value) => {
    if (value && !pattern.test(value)) {
      return message;
    }
    return null;
  };
};

export const customValidator = (fn, message) => {
  return (value) => {
    if (value && !fn(value)) {
      return message;
    }
    return null;
  };
};
