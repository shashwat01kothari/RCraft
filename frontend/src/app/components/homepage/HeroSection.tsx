import { PlayCircleIcon } from '@heroicons/react/24/solid'; // A nice icon for one of our buttons

const HeroSection = () => {
  return (
    <section className="bg-white text-center py-20 px-4">
      <div className="container mx-auto">
        {/* Art/Image Placeholder */}
        {/* For production, replace this div with the Next.js <Image> component */}
        <div className="mx-auto mb-8 w-48 h-48 bg-gray-200 rounded-full flex items-center justify-center">
          <span className="text-gray-500">Your Art Here</span>
        </div>

        {/* Company Tagline */}
        <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 mb-4 leading-tight">
          Build Your Future, Faster
        </h1>

        {/* Description */}
        <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          Our revolutionary SaaS platform helps you streamline workflows, boost productivity, and achieve your goals with unprecedented speed.
        </p>

        {/* Call to Action Buttons */}
        <div className="flex justify-center items-center space-x-4 mb-12">
          <a
            href="/signup"
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-8 rounded-lg transition duration-300 shadow-lg"
          >
            Get Started Free
          </a>
          <a
            href="#video"
            className="flex items-center text-gray-800 font-bold py-3 px-6 rounded-lg hover:bg-gray-100 transition duration-300"
          >
            <PlayCircleIcon className="h-6 w-6 mr-2" />
            Watch Demo
          </a>
        </div>

        {/* SaaS Working Video */}
        <div id="video" className="max-w-6xl mx-auto">
          <div className="aspect-w-16 aspect-h-9 rounded-lg shadow-2xl overflow-hidden">
            {/* Replace with your actual video source */}
            <video
              src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
              autoPlay
              loop
              muted
              playsInline
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;