'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { register, checkHealth } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [algorithm, setAlgorithm] = useState<'scrypt' | 'pbkdf2'>('scrypt');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [apiConnected, setApiConnected] = useState<boolean | null>(null);

  useEffect(() => {
    checkHealth().then(setApiConnected).catch(() => setApiConnected(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setLoading(true);

    try {
      await register({ email, password, confirmPassword, algorithm });
      setSuccess(true);
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-3xl font-bold text-center">Create Account</CardTitle>
          <CardDescription className="text-center">
            Sign up for a new account with secure password hashing
          </CardDescription>
        </CardHeader>
        <CardContent>
          {apiConnected === false && (
            <div className="mb-4 p-3 text-sm text-yellow-500 bg-yellow-500/10 border border-yellow-500/20 rounded-md">
              <p className="font-medium">⚠️ Backend API not connected</p>
              <p className="text-xs mt-1">Please start the Flask backend server:</p>
              <code className="block mt-2 text-xs bg-black/50 p-2 rounded">python3 api.py</code>
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-destructive bg-destructive/10 border border-destructive/20 rounded-md">
                {error}
              </div>
            )}
            {success && (
              <div className="p-3 text-sm text-green-500 bg-green-500/10 border border-green-500/20 rounded-md">
                Account created successfully! Redirecting to login...
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading || success}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="At least 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading || success}
                minLength={8}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirmPassword">Confirm Password</Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="Confirm your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                disabled={loading || success}
                minLength={8}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="algorithm">Hashing Algorithm</Label>
              <select
                id="algorithm"
                value={algorithm}
                onChange={(e) => setAlgorithm(e.target.value as 'scrypt' | 'pbkdf2')}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                disabled={loading || success}
              >
                <option value="scrypt">Scrypt (Recommended)</option>
                <option value="pbkdf2">PBKDF2</option>
              </select>
            </div>
            <Button type="submit" className="w-full" disabled={loading || success || apiConnected === false}>
              {loading ? 'Creating account...' : success ? 'Account Created!' : apiConnected === false ? 'Backend Not Available' : 'Create Account'}
            </Button>
          </form>
          <div className="mt-4 text-center text-sm">
            <span className="text-muted-foreground">Already have an account? </span>
            <Link href="/login" className="text-primary hover:underline">
              Sign in
            </Link>
          </div>
          <div className="mt-2 text-center">
            <Link href="/" className="text-sm text-muted-foreground hover:underline">
              ← Back to home
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

