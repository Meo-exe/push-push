"use client";
import Link from 'next/link';
import { useState } from 'react';
import { importData } from '@/services/api';

export default function Home() {
  const [season, setSeason] = useState(2023);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleImport = async () => {
    try {
      setLoading(true);
      const response = await importData(season);
      setMessage(response.message);
    } catch (error) {
      setMessage(`Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <main className="">
      <h1>F1 Statistics Dashboard</h1>
      
      <div className="">
        <Link href="/drivers" className="">
          <h2>Drivers</h2>
          <p>View all F1 drivers and their details.</p>
        </Link>
        
        <Link href="/teams" className="">
          <h2>Teams</h2>
          <p>Explore constructor teams in Formula 1.</p>
        </Link>
        
        <Link href="/races" className="">
          <h2>Races</h2>
          <p>Browse race information by season.</p>
        </Link>
        
        <Link href="/results" className="">
          <h2>Results</h2>
          <p>Check race results and standings.</p>
        </Link>
      </div>
    </main>
  );
}