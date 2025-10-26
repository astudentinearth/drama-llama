import { useEffect, useState } from "react"
import { useUserMode } from "@/contexts/user-mode-context"

function Topbar() {
    const [selected, setSelected] = useState<'individual' | 'business'>('individual');
    const { setUserMode } = useUserMode();
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        // set UserModeContext state based on selected
        setUserMode(selected);
    }, [selected, setUserMode]);

    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 0) {
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
        <nav className={`w-full  backdrop-blur-3xl transition-all duration-500 shadow ${isScrolled ? 'shadow-xl bg-gray-900' : 'bg-gray-500'}`}>
            <div className="max-w-5xl h-8 mx-auto flex justify-between items-center py-2 text-white">
                <ul className="flex space-x-12 text-sm">
                    <li
                        onClick={() => setSelected('individual')}
                        className="hover:cursor-pointer relative pb-1"
                    >
                        For Individual
                        <span
                            className={`absolute bottom-0 left-0 h-0.5 bg-white transition-transform duration-300 ease-out origin-left ${selected === 'individual' ? 'w-full scale-x-100' : 'w-full scale-x-0'
                                }`}
                        />
                    </li>
                    <li
                        onClick={() => setSelected('business')}
                        className="hover:cursor-pointer relative pb-1"
                    >
                        For Business
                        <span
                            className={`absolute bottom-0 left-0 h-0.5 bg-white transition-transform duration-300 ease-out origin-left ${selected === 'business' ? 'w-full scale-x-100' : 'w-full scale-x-0'
                                }`}
                        />
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default Topbar
