export default function Footer() {
    return (
        <footer className="bg-black text-white py-12 mt-24">
            <div className="max-w-5xl mx-auto px-6 flex flex-col items-center justify-center">
                <div className="flex items-center space-x-3">
                    <img src="/logo.png" alt="Groowy Logo" className="h-16 w-auto" />
                    <h3 className="text-2xl font-semibold">Groowy</h3>
                </div>
            </div>
        </footer>
    );
}
