import axios from 'axios'

// Function to fetch data from an Azure SQL database
export default async function fetchFromAzure(endpoint) {
  try {
    const response = await axios.get(`https://food-pod.onrender.com/api/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data from Azure:', error);
    return [];
  }
}
