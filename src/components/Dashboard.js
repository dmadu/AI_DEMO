import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [accountData, setAccountData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem('token') || (user && user.token);
        const response = await fetch('/api/user/account', {
          headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch account details');
        }

        const data = await response.json();
        setAccountData(data);
      } catch (err) {
        setError(err.message || 'An error occurred while fetching account details.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user]);

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', borderBottom: '1px solid #eaeaea', paddingBottom: '1rem' }}>
        <h1>Dashboard</h1>
        <button
          onClick={logout}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Logout
        </button>
      </header>

      {loading ? (
        <p>Loading account details...</p>
      ) : error ? (
        <div style={{ color: 'red', backgroundColor: '#f8d7da', padding: '1rem', borderRadius: '4px' }}>
          {error}
        </div>
      ) : (
        <div>
          <div style={{ backgroundColor: '#e2f0d9', padding: '1.5rem', borderRadius: '6px', marginBottom: '1.5rem' }}>
            <h2>Welcome, {accountData?.name || user?.name || 'User'}!</h2>
            <p>We are glad to have you back.</p>
          </div>

          <div style={{ backgroundColor: '#f9f9f9', padding: '1.5rem', borderRadius: '6px', border: '1px solid #ddd' }}>
            <h3>Account Status</h3>
            <p><strong>Email:</strong> {accountData?.email || user?.email || 'N/A'}</p>
            <p><strong>Status:</strong> <span style={{ color: accountData?.status === 'Active' ? 'green' : 'inherit' }}>{accountData?.status || 'Active'}</span></p>
            <p><strong>Member Since:</strong> {accountData?.memberSince || 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
