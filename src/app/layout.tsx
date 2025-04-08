import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
// Temporarily disabled Clerk auth and ThemeProvider for troubleshooting

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Finance Assistant',
  description: 'Manage your finances with AI-powered insights and recommendations',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-black text-white dark`}>
        {children}
      </body>
    </html>
  );
}