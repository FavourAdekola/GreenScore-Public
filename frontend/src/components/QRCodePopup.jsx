// QRCodePopup.jsx
import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import './QRCodePopup.css';

const QRCodePopup = ({ QRId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const predefinedString = QRId; // Change this to your desired string

  return (
    <div className="qr-container">
      <button
        onClick={() => setIsOpen(true)}
        className="qr-button"
      >
        Show QR Code
      </button>

      {isOpen && (
        <div className="qr-overlay">
          <div className="qr-modal">
            <button
              onClick={() => setIsOpen(false)}
              className="qr-close-button"
              aria-label="Close"
            >
              ×
            </button>
            
            <div className="qr-content">
              <h3 className="qr-title">Scan QR Code</h3>
              <div className="qr-code-wrapper">
                <QRCodeSVG 
                  value={predefinedString}
                  size={256}
                  level="H"
                  includeMargin={true}
                  bgColor="#FFFFFF"
                  fgColor="#000000"
                />
              </div>
              <div className="qr-alert">
                Scan this QR code or click to copy: {predefinedString}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default QRCodePopup;