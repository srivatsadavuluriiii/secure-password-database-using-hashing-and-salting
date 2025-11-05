// Try multiple ports in case 5000 is in use
const getApiUrl = () => {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  // Default to 5001 if 5000 is likely in use (common on macOS)
  return 'http://localhost:5001/api';
};

const API_URL = getApiUrl();

export interface RegisterData {
  email: string;
  password: string;
  confirmPassword: string;
  algorithm: 'scrypt' | 'pbkdf2';
}

export interface LoginData {
  email: string;
  password: string;
}

export interface ApiResponse<T = any> {
  message?: string;
  error?: string;
  email?: string;
  algorithm?: string;
}

export async function register(data: RegisterData): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const result = await response.json().catch(() => ({ error: 'Network error or invalid response' }));
      throw new Error(result.error || `Registration failed: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to connect to server. Make sure the backend is running on port 5000.');
  }
}

export async function login(data: LoginData): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const result = await response.json().catch(() => ({ error: 'Network error or invalid response' }));
      throw new Error(result.error || `Login failed: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to connect to server. Make sure the backend is running on port 5000.');
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

