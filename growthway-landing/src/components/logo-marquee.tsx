import Marquee from "react-fast-marquee";

function LogoMarquee() {
    const logos = [
        { src: "/logos/meta.png", alt: "Meta" },
        { src: "/logos/ollama.png", alt: "Ollama" },
        { src: "/logos/ytustartup.png", alt: "YTU Startup" },
    ];

    return (
        <Marquee autoFill>
            {
                logos.map((logo, index) => (
                    <div key={index} className="mx-24">
                        <img src={logo.src} alt={logo.alt} className="h-12 object-contain" />
                    </div>
                ))
            }
        </Marquee>
    );
}

export default LogoMarquee;
