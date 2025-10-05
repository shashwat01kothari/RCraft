const MarqueeSection = () => {
  const marqueeText = "Your Text Here ◆ Seamless Integration ◆ Boost Productivity ◆ 24/7 Support ◆";
  
  // We repeat the text to ensure a seamless loop
  const repeatedText = Array(5).fill(marqueeText).join(" ");

  return (
    <section className="bg-gray-900 text-white py-4 overflow-hidden">
      <div className="relative flex whitespace-nowrap">
        <div className="animate-marquee">
          <span className="text-xl font-semibold mx-4">{repeatedText}</span>
        </div>
        {/* This second div is a trick to make the loop appear seamless */}
        <div className="animate-marquee absolute top-0">
          <span className="text-xl font-semibold mx-4">{repeatedText}</span>
        </div>
      </div>
    </section>
  );
};

export default MarqueeSection;