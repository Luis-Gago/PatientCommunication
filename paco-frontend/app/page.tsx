'use client';

import { useState, useEffect } from 'react';
import ResearchIDScreen from '@/components/ResearchIDScreen';
import DisclaimerScreen from '@/components/DisclaimerScreen';
import ElevenLabsWidget from '@/components/ElevenLabsWidget';
import { PaCoAPI } from '@/lib/api';
import { AppScreen } from '@/types';

export default function Home() {
  const [screen, setScreen] = useState<AppScreen>('research-id');
  const [researchId, setResearchId] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  // Restore session from localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem('paco_token');
    const savedResearchId = localStorage.getItem('paco_research_id');
    const savedExpiry = localStorage.getItem('paco_token_expiry');

    if (savedToken && savedResearchId && savedExpiry) {
      const expiryDate = new Date(savedExpiry);
      if (expiryDate > new Date()) {
        setToken(savedToken);
        setResearchId(savedResearchId);
        setScreen('chat');
      } else {
        // Token expired, clear storage
        localStorage.removeItem('paco_token');
        localStorage.removeItem('paco_research_id');
        localStorage.removeItem('paco_token_expiry');
      }
    }
  }, []);

  const handleResearchIDValidated = (validatedId: string) => {
    setResearchId(validatedId);
    setScreen('disclaimer');
  };

  const handleDisclaimerAcknowledged = async () => {
    if (!researchId) return;

    try {
      // Login to get token
      const loginResponse = await PaCoAPI.login({ research_id: researchId });

      // Save to state and localStorage
      setToken(loginResponse.access_token);
      localStorage.setItem('paco_token', loginResponse.access_token);
      localStorage.setItem('paco_research_id', researchId);
      localStorage.setItem('paco_token_expiry', loginResponse.expires_at);

      // Navigate to chat
      setScreen('chat');
    } catch (error) {
      console.error('Login failed:', error);
      alert('Failed to log in. Please try again.');
    }
  };

  const handleLogout = () => {
    // Clear state
    setToken(null);
    setResearchId(null);
    setScreen('research-id');

    // Clear localStorage
    localStorage.removeItem('paco_token');
    localStorage.removeItem('paco_research_id');
    localStorage.removeItem('paco_token_expiry');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {screen === 'research-id' && (
          <ResearchIDScreen onValidated={handleResearchIDValidated} />
        )}

        {screen === 'disclaimer' && researchId && (
          <DisclaimerScreen
            researchId={researchId}
            onAcknowledged={handleDisclaimerAcknowledged}
          />
        )}

        {screen === 'chat' && researchId && token && (
          <ElevenLabsWidget researchId={researchId} token={token} onLogout={handleLogout} />
        )}
      </div>
    </div>
  );
}
