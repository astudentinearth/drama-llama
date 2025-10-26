import Topbar from "./components/topbar"
import LogoMarquee from "./components/logo-marquee"
import PlansSection from "./components/plans-section"
import ComparisonTable from "./components/comparison-table"
import Footer from "./components/footer"
import { PointerHighlight } from "@/components/ui/pointer-highlight";
import { HoverBorderGradient } from "./components/ui/hover-border-gradient"
import { TypewriterEffectSmooth } from "./components/ui/typewriter-effect"
import { motion } from "motion/react"
import { AnimatedSection, AnimatedElement } from "./components/ui/animated-section"
import RoadmapCTA from "./components/rounded-rectangle";

function App() {
  const words = [
    {
      text: "Where",
    },
    {
      text: "skills",
    },
    {
      text: "meet",
    },
    {
      text: "their",
    },
    {
      text: "future.",
      className: "text-[#2621BD]",
    },
  ];

  return (
    <div className="min-w-full z-100 relative">
      <div className="fixed w-full z-150">
        <Topbar />
        {/* <Navbar /> */}
      </div>

      <section className="max-w-5xl mx-auto space-y-6 flex flex-col justify-evenly  min-h-[80vh]">
        <AnimatedSection direction="up" delay={0.2} className="container">
          <h1 className="text-4xl font-semibold mb-24"><img src="/logo.png" alt="Groowy" className="inline-block h-12 w-auto me-2" />Groowy</h1>
          <h3 className="text-lg ">Personalized growth, Smarter hiring.</h3>
          <TypewriterEffectSmooth words={words} className="text-7xl font-semibold" />
        </AnimatedSection>
        <AnimatedElement delay={0.6} className="flex flex-row space-x-6 self-center justify-between w-full">
          <a href="/app">
            <HoverBorderGradient className="px-14 py-4 rounded-3xl dark:bg-black bg-white text-black dark:text-white flex items-center" >Start with Individual Account</HoverBorderGradient>
          </a>
          <a href="/app">
            <HoverBorderGradient className="px-18 py-4 rounded-3xl dark:bg-black bg-white text-black dark:text-white flex items-center">Start with Your Company</HoverBorderGradient>
          </a>
        </AnimatedElement>
      </section>
      <AnimatedSection direction="up" className="mb-48 text-center">
        <div className="flex flex-row items-center justify-center space-x-12 mb-8">
          <hr className="w-48" />
          <h4 className="text-2xl font-semibold">Our Clients</h4>
          <hr className="w-48" />
        </div>
        <LogoMarquee />
      </AnimatedSection>
      <motion.section className="max-w-5xl mx-auto flex flex-col items-center min-h-screen space-y-16 pb-24 container">
        <AnimatedElement delay={0.1} scale>
          <h1 className="text-5xl">Smart Careers, Supercharged by <PointerHighlight containerClassName="inline-block mx-1">AI</PointerHighlight></h1>
        </AnimatedElement>
        <AnimatedElement delay={0.3} scale>
          <img src="/chart.png" alt="" className="max-w-5xl mx-auto" />
        </AnimatedElement>
      </motion.section>
      <PlansSection />
      <ComparisonTable />
      <AnimatedSection direction="up" className="max-w-5xl mx-auto mb-48 text-center">
        <RoadmapCTA />
      </AnimatedSection>
      <Footer />
    </div>
  )
}

export default App