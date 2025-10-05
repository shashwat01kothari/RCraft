
// We will create these placeholder components later
// import TrustSection from './components/homepage/TrustSection';
// import Footer from './components/Footer';

import FeaturesSection from "./components/homepage/FeaturesSection";
import HeroSection from "./components/homepage/HeroSection";
import MarqueeSection from "./components/homepage/MarqueeSection";

export default function Home() {
  return (
    <main>
      <HeroSection />
      <FeaturesSection />
      <MarqueeSection />
      {/* <TrustSection /> */}
      {/* <Footer /> */}
    </main>
  );
}