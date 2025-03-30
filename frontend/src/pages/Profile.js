import React, { useState } from 'react';

const Profile = () => {
  const [isProfileWindow, setIsProfileWindow] = useState(false);
  const [profileWindow, setProfileWindow] = useState(null); // Track the new window

  const toggleProfileWindow = () => {
    if (isProfileWindow && profileWindow) {
      // If it's already open, focus on the new window
      profileWindow.focus();
    } else {
      // Open a new window and store the reference
      const newWindow = window.open('', '', 'width=400,height=400');
      newWindow.document.write(`
        <h1>Your Profile</h1>
        <p>Profile Info (new window mode)</p>
      `);
      setProfileWindow(newWindow);
    }
    setIsProfileWindow(!isProfileWindow);
  };

  return (
    <div>
      <h1>Your Profile</h1>
      <button onClick={toggleProfileWindow}>
        {isProfileWindow ? 'Show on Same Page' : 'Show in New Window'}
      </button>
      {isProfileWindow ? (
        <div>
          {/* Profile details on the same page */}
          <p>Profile Info (same page mode)</p>
        </div>
      ) : (
        <div>
          {/* Profile details in new window mode */}
          <p>Profile Info (new window mode)</p>
        </div>
      )}
    </div>
  );
};

export default Profile;
