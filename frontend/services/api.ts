import axios from 'axios';

const API_URL = 'https://push-push.onrender.com';

const api = axios.create({
  baseURL: API_URL,
});

export const fetchDrivers = async () => {
  const response = await api.get('/api/drivers');
  return response.data;
};

export const fetchTeams = async () => {
  const response = await api.get('/api/teams');
  return response.data;
};

export const fetchRaces = async () => {
  const response = await api.get('/api/races');
  return response.data;
};

export const fetchResults = async (raceId = null) => {
  const url = raceId ? `/api/results?race_id=${raceId}` : '/api/results';
  const response = await api.get(url);
  return response.data;
};

export const importData = async (season: number) => {
  const response = await api.get(`/api/import-data/${season}`);
  return response.data;
};