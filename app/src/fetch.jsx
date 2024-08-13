import axios from 'axios';

const BASE_URL = 'https://food-pod.onrender.com/api';
const LOCAL_URL = 'https://localhost:8080/api';
const TIMEOUT = 1000; // 1 second

// Utility function to fetch data with a retry mechanism
const fetchData = async (url, endpoint) => {
  try {
    const response = await axios.get(`${url}/${endpoint}`, { timeout: TIMEOUT });
    return response.data;
  } catch (error) {
    console.error(`Error fetching data from ${url}/${endpoint}.`, error);
    throw error;
  }
};

export default async function fetchFromAzure(endpoint) {
  try {
    // Attempt to fetch data from the remote server
    const data = await fetchData(BASE_URL, endpoint);
    return data; // If successful, return the data and stop further attempts
  } catch (error) {
    console.warn('Remote server failed. Trying localhost...');

    try {
      // Wait for 1 second before retrying
      await new Promise(resolve => setTimeout(resolve, TIMEOUT));
      const localData = await fetchData(LOCAL_URL, endpoint);
      return localData; // Return data if localhost is successful
    } catch (error) {
      console.error('Both remote and local servers failed.', error);
      return []; // Return an empty array if both attempts fail
    }
  }
}

