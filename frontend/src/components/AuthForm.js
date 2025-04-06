import React, { useState } from 'react';
import axios from 'axios';

export default function AuthForm({ setUser }) {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setErrorMsg('');

        const endpoint = isLogin ? 'http://127.0.0.1:5000/auth/login' : 'http://127.0.0.1:5000/auth/signup';

        try {
            const response = await axios.post(endpoint, { username, password });

            if (response.data.access_token) {
                localStorage.setItem('token', response.data.access_token);
                setUser(response.data.username || username);
            } else {
                setErrorMsg('Unexpected response. Please try again.');
            }
        } catch (err) {
            const message =
                err.response?.data?.message || 'An error occurred. Please try again.';
            setErrorMsg(message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-form w-full max-w-sm mx-auto p-6 border rounded-lg shadow-lg bg-white">
            <h2 className="text-2xl font-semibold text-center mb-4">
                {isLogin ? 'Login' : 'Sign Up'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    required
                    className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={loading}
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                    className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={loading}
                />
                <button
                    type="submit"
                    className="w-full p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
                    disabled={loading}
                >
                    {loading ? (
                        <span className="flex justify-center items-center">
                            <svg
                                className="animate-spin h-5 w-5 mr-3 text-white"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    d="M4 6h16M4 12h16m-7 6h7"
                                />
                            </svg>
                            Please wait...
                        </span>
                    ) : isLogin ? 'Log In' : 'Sign Up'}
                </button>
            </form>

            {errorMsg && (
                <p className="text-red-500 text-center mt-2" aria-live="assertive">
                    {errorMsg}
                </p>
            )}

            <p
                onClick={() => setIsLogin(!isLogin)}
                className="text-center text-blue-500 cursor-pointer mt-4"
            >
                {isLogin ? "Don't have an account?" : 'Already have an account?'} Click here
            </p>
        </div>
    );
}
