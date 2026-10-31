import type { Metadata } from 'next';
import './globals.css';
export const viewport = { width: 'device-width', initialScale: 1, viewportFit: 'cover' };
export const metadata: Metadata = { title: 'Failure Detective AI', description: 'Agentic mechanical fault diagnosis and engineering investigation.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
