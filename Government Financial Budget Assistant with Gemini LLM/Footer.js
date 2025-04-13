import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <p>Government Financial Budget Assistant &copy; {currentYear}</p>
          </div>
          <div className="col-md-6 text-md-end">
            <p>Powered by Gemini LLM and Model Context Protocol</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
