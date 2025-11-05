'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-3xl font-bold text-center">Secure Auth</CardTitle>
          <CardDescription className="text-center">
            Professional password authentication with advanced hashing
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Link href="/login" className="block">
            <Button className="w-full" size="lg">
              Sign In
            </Button>
          </Link>
          <Link href="/register" className="block">
            <Button variant="outline" className="w-full" size="lg">
              Create Account
            </Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
