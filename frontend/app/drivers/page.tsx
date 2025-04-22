"use client";
import { useState, useEffect } from 'react';
import { fetchDrivers } from '@/services/api';

interface Driver {
  driver_id: string | number;
  first_name: string;
  last_name: string;
  code: string;
  number: number;
  nationality: string;
  date_of_birth?: string;
}

export default function Drivers() {
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadDrivers() {
      try {
        const data = await fetchDrivers();
        setDrivers(data);
      } catch (err) {
        setError('Failed to load drivers');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    
    loadDrivers();
  }, []);
  
  if (loading) return <p>Loading drivers...</p>;
  if (error) return <p>{error}</p>;
  
  return (
    <div className="">
      <h1>F1 Drivers</h1>
      
      <div className="">
        {drivers.map(driver => (
          <div key={driver.driver_id} className="">
            <h2>{driver.first_name} {driver.last_name}</h2>
            <p>Code: {driver.code}</p>
            <p>Number: {driver.number}</p>
            <p>Nationality: {driver.nationality}</p>
            {driver.date_of_birth && 
              <p>Born: {new Date(driver.date_of_birth).toLocaleDateString()}</p>
            }
          </div>
        ))}
      </div>
    </div>
  );
}