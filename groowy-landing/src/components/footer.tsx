export default function Footer() {
    return (
        <footer className="bg-black text-white py-8 sm:py-12 mt-12 sm:mt-16 md:mt-24">
            <div className="max-w-5xl mx-auto px-4 sm:px-6 flex flex-col items-center justify-center">
                <div className="flex items-center space-x-2 sm:space-x-3">
                    <img src="/logo.png" alt="Groowy Logo" className="h-12 sm:h-14 md:h-16 w-auto" />
                    <h3 className="text-xl sm:text-2xl font-semibold">groowy</h3>
                </div>
            </div>
        </footer>
    );
}
