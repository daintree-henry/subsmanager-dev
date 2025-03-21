// Base URLs for different services
export const API_CONFIG = {
  USER_URL: `${import.meta.env.VITE_USER_API_URL || 'http://localhost:5005'}`,
  SUBSCRIPTION_URL: `${import.meta.env.VITE_SUBS_API_URL || 'http://localhost:5004'}`,
  RECOMMEND_URL: `${import.meta.env.VITE_RECO_API_URL || 'http://localhost:5003'}`,
};

export const createAuthHeader = () => ({
  headers: {
    Authorization: `Bearer ${localStorage.getItem('access_token')}`
  }
});

