import React, { useState } from 'react';

const Profile = () => {
  const [isProfileWindow, setIsProfileWindow] = useState(false);

  const toggleProfileWindow = () => {
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
          {/* Profile details in new window mode */}
          <p>Profile Info (new window mode)</p>
        </div>
      ) : (
        <div>
          {/* Profile details on the same page */}
          <p>Profile Info (same page mode)</p>
        </div>
      )}
    </div>
  );
};

export default Profile;
