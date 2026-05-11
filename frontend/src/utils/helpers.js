export const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

export const getSeverityColor = (severity) => {
  const colors = {
    HIGH: '#dc2626',
    MEDIUM: '#f59e0b',
    LOW: '#10b981',
  };
  return colors[severity.toUpperCase()] || '#6b7280';
};

export const downloadJSON = (data, filename) => {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};