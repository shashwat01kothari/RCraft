"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <nav
      className={`bg-white text-gray-900 p-4 sticky top-0 z-50 ${
        isScrolled ? 'border-b border-gray-200' : ''
      }`}
      role="navigation"
      aria-label="Main Navigation"
    >
      <div className="container mx-auto flex items-center justify-between">
        {/* Logo on the left */}
        <div className="flex-shrink-0">
          <Link href="/" className="text-2xl font-bold">
            L
          </Link>
        </div>

        {/* Centered Nav Links for Desktop */}
        {/* CHANGE: Added "CoverGen" to the navigation links */}
        <div className="hidden md:flex flex-grow items-center justify-center space-x-2">
          <Link href="/" className="px-4 py-2 rounded-md hover:bg-gray-100 transition-all duration-200">
            Home
          </Link>
          <Link href="/analyzer" className="px-4 py-2 rounded-md hover:bg-gray-100 transition-all duration-200">
            Analyzer
          </Link>
          <Link href="/optimizer" className="px-4 py-2 rounded-md hover:bg-gray-100 transition-all duration-200">
            Optimizer
          </Link>
          <Link href="/covergen" className="px-4 py-2 rounded-md hover:bg-gray-100 transition-all duration-200">
            CoverGen
          </Link>
        </div>

        {/* Right side: Login Button (Desktop) and Hamburger (Mobile) */}
        <div className="flex items-center">
          <div className="hidden md:block">
            <Link href="/login" className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition duration-300">
              Log In
            </Link>
          </div>

          <div className="md:hidden ml-4">
            <button
              onClick={toggleMenu}
              aria-expanded={isOpen}
              aria-controls="mobile-menu"
              aria-label="Open main menu"
              className="focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              <span className="sr-only">Open main menu</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={isOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16m-7 6h7'}></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {/* CHANGE: Added "CoverGen" to the mobile menu */}
      {isOpen && (
        <div id="mobile-menu" className="md:hidden mt-4 bg-white text-gray-900">
          <Link href="/" className="block py-2 px-4 text-sm hover:bg-gray-100" onClick={toggleMenu}>
            TheJWord
          </Link>
          <Link href="/analyzer" className="block py-2 px-4 text-sm hover:bg-gray-100" onClick={toggleMenu}>
            Analyzer
          </Link>
          <Link href="/optimizer" className="block py-2 px-4 text-sm hover:bg-gray-100" onClick={toggleMenu}>
            Optimizer
          </Link>
          <Link href="/covergen" className="block py-2 px-4 text-sm hover:bg-gray-100" onClick={toggleMenu}>
            CoverGen
          </Link>
          <Link href="/login" className="block py-2 px-4 text-sm font-bold text-blue-500 hover:bg-gray-100" onClick={toggleMenu}>
            Log In
          </Link>
        </div>
      )}
    </nav>
  );
};

export default Navbar;