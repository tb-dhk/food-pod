import React from 'react';

export default function Creditsdiv({ props }) {
  return (
    <div className="credits-container">
      <h1 className="credits-title">Credits</h1>
      <div className="credits-content">
        <section className="credits-section">
          <h2 className="section-heading">Made By:</h2>
          <ul className="credits-list">
            <li>Wang Xinjie</li>
            <li>Johann Young</li>
            <li>Keegan Cheng</li>
            <li>Joshua Soh</li>
            <li>Chen Yixu</li>
          </ul>
        </section>
        <section className="credits-section">
          <h2 className="section-heading">Special Thanks To:</h2>
          <ul className="credits-list">
            <li>Sembcorp Industries</li>
            <li>Mr. Tiong Heng Liong</li>
            <li>Mr. Firdaus Hamzah</li>
          </ul>
        </section>
      </div>
    </div>
  );
}

