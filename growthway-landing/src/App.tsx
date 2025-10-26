import Navbar from "./components/navbar"
import Topbar from "./components/topbar"
import LogoMarquee from "./components/logo-marquee"
import { HoverBorderGradient } from "./components/ui/hover-border-gradient"
import { TypewriterEffectSmooth } from "./components/ui/typewriter-effect"
import { motion } from "motion/react"

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
      <div className="fixed w-full">
        <Topbar />
        {/* <Navbar /> */}
      </div>

      <section className="max-w-5xl mx-auto space-y-6 flex flex-col justify-evenly  min-h-[80vh]">
        <div>
          <h1 className="text-4xl font-semibold mb-24">groowy</h1>
          <h3 className="text-lg ">Personalized growth, Smarter hiring.</h3>
          <TypewriterEffectSmooth words={words} className="text-7xl font-semibold" />
        </div>
        <div className="flex flex-row space-x-6 self-center justify-between w-full">
          <HoverBorderGradient className="px-14 py-4 rounded-3xl dark:bg-black bg-white text-black dark:text-white flex items-center" >Start with Individual Account</HoverBorderGradient>
          <HoverBorderGradient className="px-18 py-4 rounded-3xl dark:bg-black bg-white text-black dark:text-white flex items-center">Start with Your Company</HoverBorderGradient>
        </div>
      </section>
      <section className="mb-48 text-center">
        <div className="flex flex-row items-center justify-center space-x-12 mb-8">
          <hr className="w-48" />
          <h4 className="text-2xl font-semibold">Clients</h4>
          <hr className="w-48" />
        </div>
        <LogoMarquee />
      </section>
      <motion.section className="max-w-5xl mx-auto flex flex-col items-center h-screen space-y-16">
        <h1 className="text-5xl">Smart Careers, Supercharged by AI</h1>
        <img src="/chart.png" alt="" className="max-w-5xl mx-auto" />
      </motion.section>
    </div>
  )
}

export default App