const FeaturesSection = () => {
  return (
    <section className="bg-white py-20 px-4">
      <div className="container mx-auto">
        {/* Main/New Feature Section */}
        <div className="flex flex-col md:flex-row items-center gap-12 mb-12">
          {/* Video on the left */}
          <div className="md:w-1/2">
            <div className="aspect-w-16 aspect-h-9 rounded-lg shadow-lg overflow-hidden">
              <video
                src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
                autoPlay
                loop
                muted
                playsInline
                className="w-full h-full object-cover"
              />
            </div>
          </div>
          {/* Text on the right */}
          <div className="md:w-1/2">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Discover Our Newest Feature
            </h2>
            <p className="text-gray-600 text-lg">
              We've just launched an innovative new tool that revolutionizes how you manage your data. This video showcases the seamless workflow and powerful capabilities that will save you hours of work every week.
            </p>
          </div>
        </div>

        {/* Older Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Older Feature 1 */}
          <div className="flex flex-col">
            <div className="aspect-w-16 aspect-h-9 rounded-lg shadow-lg overflow-hidden mb-4">
              <video
                src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
                autoPlay
                loop
                muted
                playsInline
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-2xl font-semibold text-gray-800">Time-Saving Automation</h3>
            <p className="text-gray-500 mt-2">Automate repetitive tasks and focus on what matters most.</p>
          </div>

          {/* Older Feature 2 */}
          <div className="flex flex-col">
            <div className="aspect-w-16 aspect-h-9 rounded-lg shadow-lg overflow-hidden mb-4">
              <video
                src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
                autoPlay
                loop
                muted
                playsInline
                className="w-full h-full object-cover"
              />
            </div>
            <h3 className="text-2xl font-semibold text-gray-800">Advanced Analytics</h3>
            <p className="text-gray-500 mt-2">Gain deep insights into your performance with our powerful dashboard.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;