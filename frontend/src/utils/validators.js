export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validatePassword = (password) => {
  return password.length >= 8;
};

export const validateUsername = (username) => {
  return username.length >= 3 && username.length <= 50;
};

export const validateFile = (file) => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  const allowedTypes = ['.py'];
  
  if (file.size > maxSize) {
    return { valid: false, error: 'File size exceeds 10MB' };
  }
  
  const extension = '.' + file.name.split('.').pop().toLowerCase();
  if (!allowedTypes.includes(extension)) {
    return { valid: false, error: 'Only Python (.py) files are allowed' };
  }
  
  return { valid: true };
};