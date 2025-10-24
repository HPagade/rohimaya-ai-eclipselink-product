import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'EclipseLink AI - Clinical Handoff Platform',
  description: 'Voice-enabled clinical handoff platform with AI-powered SBAR generation',
  manifest: '/manifest.json',
  themeColor: '#1a9b8e',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'EclipseLink AI'
  }
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
