'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<{ email?: string; algorithm?: string } | null>(null);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    } else {
      router.push('/login');
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/');
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black p-4">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <Button variant="outline" onClick={handleLogout}>
            Logout
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Welcome back!</CardTitle>
            <CardDescription>Your account information</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1">
              <Label className="text-sm text-muted-foreground">Email</Label>
              <p className="text-lg font-medium">{user.email}</p>
            </div>
            <div className="space-y-1">
              <Label className="text-sm text-muted-foreground">Hashing Algorithm</Label>
              <p className="text-lg font-medium uppercase">{user.algorithm}</p>
            </div>
            <div className="pt-4 border-t">
              <p className="text-sm text-muted-foreground">
                Your password is securely hashed using {user.algorithm === 'scrypt' ? 'Scrypt' : 'PBKDF2'} algorithm.
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="mt-4 text-center">
          <Link href="/" className="text-sm text-muted-foreground hover:underline">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}


