import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from 'next/link';
import React from 'react';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Pushpush",
  description: "Formula 1 dashboard",
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header>
          <nav className="flex justify-center gap-2 items-center p-4 text-white">
            <Link href="/">Home</Link>
            <Link href="/drivers">Drivers</Link>
            <Link href="/teams">Teams</Link>
            <Link href="/races">Races</Link>
            <Link href="/results">Results</Link>
          </nav>
        </header>
        <main>{children}</main>
        <footer>
          <p>&copy; {new Date().getFullYear()} PushPush</p>
        </footer>
      </body>
    </html>
  );
}