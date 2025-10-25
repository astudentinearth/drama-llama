import Navbar from "./components/navbar"
import Topbar from "./components/topbar"
import LogoMarquee from "./components/logo-marquee"
import { HoverBorderGradient } from "./components/ui/hover-border-gradient"

function App() {
  return (
    <div className="min-w-full z-100 relative">
      <div className="fixed w-full">
        <Topbar />
        {/* <Navbar /> */}
      </div>

      <section className="max-w-3xl mx-auto space-y-6 flex flex-col justify-center min-h-[80vh]">
        <div>
          <h1 className="text-4xl font-semibold mb-24">groowy</h1>
          <h3 className="text-lg">Personalized growth, Smarter hiring.</h3>
          <h1 className="text-6xl font-semibold bg-gradient-to-r from-black via-[#2621BD] to-black bg-clip-text text-transparent leading-20 pb-24">Where skills meet<br /> their future. </h1>
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
    </div>
  )
}

export default App