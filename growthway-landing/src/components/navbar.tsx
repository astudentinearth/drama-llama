import React from 'react'

function Navbar() {
    const [scrolled, setScrolled] = React.useState(false)

    React.useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 0) {
                setScrolled(true)
            } else {
                setScrolled(false)
            }
        }

        window.addEventListener('scroll', handleScroll)
        return () => {
            window.removeEventListener('scroll', handleScroll)
        }
    }, [])

    return (
        // when scrolled bg-white/40
        <nav className={`h-16 backdrop-blur-2xl ${scrolled ? 'bg-white/20' : 'bg-white/40'}`}>
            <ul className="flex space-x-8 max-w-3xl mx-auto justify-end items-center h-full text-sm">
                <li>
                    <button className='cursor-pointer'>Log In</button>
                </li>
                <li>
                    <button className="from-[#0F1A2C] via-[#33363A] to-[#000000] bg-linear-to-r text-white px-12 py-3 rounded-2xl cursor-pointer">Join</button>
                </li>
            </ul>
        </nav>
    )
}

export default Navbar