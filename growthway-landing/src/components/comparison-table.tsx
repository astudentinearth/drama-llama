import { div } from "framer-motion/client";

type ComparisonRow = {
    platform: string;
    description: string;
    icon: React.ReactNode;
    speed: boolean;
    flexibility: boolean;
    quality: boolean;
    scalability: boolean;
    affordable: boolean;
    isHighlighted?: boolean;
};

const Logo = () => (
    <div className="w-8 h-8 flex items-center justify-center">
        <img src="/logo.png" alt="Logo" className="h-full w-auto" />
    </div>
);

const TeamIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 35 36" fill="none" className="w-8 h-8">
        <g clipPath="url(#clip0_931_33167)">
            <path d="M31.9091 17.4642C31.0287 16.5714 29.9944 15.8448 28.8559 15.3194C29.6935 14.6269 30.3567 13.7475 30.7921 12.7519C31.2275 11.7562 31.4231 10.6723 31.3629 9.58725C31.3028 8.50223 30.9886 7.4465 30.4458 6.50511C29.903 5.56371 29.1467 4.76296 28.2377 4.16735C27.3288 3.57175 26.2927 3.19794 25.2129 3.07603C24.1331 2.95412 23.0397 3.08753 22.0209 3.4655C21.002 3.84348 20.0862 4.45545 19.3472 5.25213C18.6081 6.04881 18.0665 7.00793 17.766 8.05223H17.2361C16.9356 7.00793 16.394 6.04881 15.6549 5.25213C14.9159 4.45545 14.0001 3.84348 12.9812 3.4655C11.9624 3.08753 10.8691 2.95412 9.78923 3.07603C8.7094 3.19794 7.6733 3.57175 6.76438 4.16735C5.85546 4.76296 5.09913 5.56371 4.55631 6.50511C4.01349 7.4465 3.69936 8.50223 3.63921 9.58725C3.57906 10.6723 3.77458 11.7562 4.21003 12.7519C4.64547 13.7475 5.30866 14.6269 6.14617 15.3194C4.30564 16.1551 2.74557 17.5045 1.65338 19.2055C0.561198 20.9064 -0.0166357 22.8865 -0.0106969 24.9079C-0.0107 25.3464 0.0758693 25.7805 0.244044 26.1855C0.412219 26.5904 0.658691 26.9581 0.969319 27.2676C1.27995 27.5771 1.64862 27.8221 2.05418 27.9888C2.45975 28.1554 2.89422 28.2404 3.33269 28.2387H7.11765C7.01608 28.805 6.96541 29.3792 6.96625 29.9545C6.96622 30.8336 7.31368 31.677 7.93287 32.3009C8.55206 32.9248 9.39279 33.2786 10.2718 33.2853H24.7303C25.6115 33.282 26.4555 32.9296 27.0774 32.3053C27.6993 31.681 28.0485 30.8357 28.0485 29.9545C28.0493 29.3792 27.9987 28.805 27.8971 28.2387H31.6821C32.5632 28.2354 33.4072 27.883 34.0291 27.2587C34.651 26.6344 35.0002 25.7891 35.0002 24.9079C35.0022 23.5245 34.7301 22.1544 34.1995 20.8767C33.669 19.5991 32.8905 18.4392 31.9091 17.4642ZM24.4402 5.52892C25.6113 5.52892 26.7345 5.99416 27.5626 6.82228C28.3907 7.6504 28.8559 8.77357 28.8559 9.94471C28.8559 11.1159 28.3907 12.239 27.5626 13.0671C26.7345 13.8953 25.6113 14.3605 24.4402 14.3605C24.3279 13.1173 23.8817 11.9275 23.1488 10.917C22.4159 9.90652 21.4236 9.11286 20.2767 8.61997C20.5594 7.73355 21.1134 6.95831 21.8604 6.40369C22.6075 5.84907 23.5098 5.54308 24.4402 5.52892ZM21.9168 14.9913C21.9168 15.8647 21.6579 16.7184 21.1727 17.4446C20.6874 18.1708 19.9978 18.7368 19.1909 19.071C18.384 19.4052 17.4962 19.4927 16.6396 19.3223C15.783 19.1519 14.9962 18.7313 14.3786 18.1138C13.7611 17.4962 13.3405 16.7094 13.1701 15.8528C12.9997 14.9962 13.0872 14.1084 13.4214 13.3015C13.7556 12.4946 14.3216 11.8049 15.0478 11.3197C15.774 10.8345 16.6277 10.5755 17.5011 10.5755C18.6722 10.5755 19.7954 11.0408 20.6235 11.8689C21.4516 12.697 21.9168 13.8202 21.9168 14.9913ZM6.14617 9.94471C6.13447 8.88456 6.50568 7.85579 7.19161 7.04737C7.87753 6.23894 8.83212 5.70516 9.88002 5.54406C10.9279 5.38296 11.9988 5.60537 12.8958 6.17043C13.7929 6.7355 14.456 7.60527 14.7633 8.61997C13.6164 9.11286 12.6241 9.90652 11.8912 10.917C11.1583 11.9275 10.7121 13.1173 10.5998 14.3605C10.0167 14.3655 9.43846 14.255 8.89834 14.0353C8.35821 13.8156 7.86694 13.4911 7.45288 13.0806C7.03882 12.6701 6.71017 12.1816 6.48589 11.6433C6.26161 11.1051 6.14615 10.5278 6.14617 9.94471ZM3.33269 25.7154C3.12073 25.7121 2.91858 25.6255 2.76987 25.4745C2.62116 25.3234 2.53782 25.1199 2.53784 24.9079C2.53618 23.8537 2.7426 22.8095 3.14526 21.8353C3.54792 20.861 4.13891 19.9757 4.88435 19.2303C5.62979 18.4849 6.51502 17.8939 7.4893 17.4912C8.46358 17.0886 9.50776 16.8821 10.562 16.8838H10.8395C11.2279 18.2467 12.0249 19.4577 13.1231 20.3534C10.7729 21.4417 8.89853 23.3474 7.84941 25.7154H3.33269ZM24.7808 30.762H10.2718C10.0598 30.7587 9.85767 30.6722 9.70896 30.5211C9.56025 30.37 9.47692 30.1665 9.47694 29.9545C9.47694 27.8264 10.3223 25.7854 11.8272 24.2806C13.332 22.7758 15.3729 21.9304 17.5011 21.9304C19.6292 21.9304 21.6702 22.7758 23.175 24.2806C24.6798 25.7854 25.5252 27.8264 25.5252 29.9545C25.5252 30.1665 25.4419 30.37 25.2932 30.5211C25.1444 30.6722 24.9423 30.7587 24.7303 30.762H24.7808ZM31.7199 25.7154H27.1527C26.1011 23.3521 24.227 21.4512 21.879 20.366C22.9793 19.467 23.7766 18.2513 24.1626 16.8838H24.4402C26.5673 16.8871 28.6063 17.7336 30.1104 19.2377C31.6145 20.7418 32.4609 22.7808 32.4643 24.9079C32.4643 25.1199 32.381 25.3234 32.2323 25.4745C32.0835 25.6255 31.8814 25.7121 31.6694 25.7154H31.7199Z" fill="currentColor" />
        </g>
    </svg>
);

const BrushIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 35 36" fill="none" className="w-8 h-8">
        <g clipPath="url(#clip0_931_33182)">
            <path d="M33.6872 1.95934C32.836 1.14854 31.7054 0.696289 30.5299 0.696289C29.3543 0.696289 28.2238 1.14854 27.3726 1.95934L11.029 18.2927C10.5206 18.1948 10.0039 18.146 9.48613 18.1468C8.43351 18.1438 7.39074 18.3497 6.41823 18.7524C5.44571 19.1552 4.56276 19.7469 3.8205 20.4933C1.0205 23.2991 0.270918 32.1877 0.145501 33.9406L0.034668 35.6118L1.70446 35.4952C3.45446 35.3756 12.3503 34.6304 15.1532 31.826C16.0804 30.8962 16.7648 29.7527 17.1463 28.4962C17.5277 27.2397 17.5945 25.9087 17.3407 24.6204L33.6872 8.27393C34.5223 7.43539 34.9912 6.30012 34.9912 5.11664C34.9912 3.93316 34.5223 2.79789 33.6872 1.95934ZM13.0911 29.7639C11.7349 31.1187 6.86842 32.0389 3.21238 32.4327C3.62509 28.641 4.58758 23.8518 5.88259 22.5554C6.85419 21.6803 8.12458 21.2115 9.43172 21.2456C10.7389 21.2798 11.9831 21.8143 12.9077 22.7389C13.8323 23.6635 14.3668 24.9076 14.4009 26.2148C14.435 27.5219 13.9662 28.7923 13.0911 29.7639ZM31.628 6.21184L16.139 21.7023C15.5636 20.8309 14.8198 20.0832 13.9515 19.5031L29.4347 4.01851C29.7293 3.73716 30.121 3.58018 30.5284 3.58018C30.9358 3.58018 31.3275 3.73716 31.6222 4.01851C31.7668 4.162 31.8818 4.33262 31.9604 4.5206C32.039 4.70858 32.0797 4.91022 32.0802 5.11397C32.0808 5.31772 32.0411 5.51957 31.9635 5.70797C31.8859 5.89636 31.7719 6.06759 31.628 6.21184Z" fill="currentColor" />
        </g>
    </svg>
);

const FreelancerIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 35 36" fill="none" className="w-8 h-8">
        <g clipPath="url(#clip0_931_33196)">
            <path d="M17.3805 19.3665C12.22 19.3665 8.02002 15.1665 8.02002 10.006C8.02002 4.84552 12.22 0.645508 17.3805 0.645508C22.541 0.645508 26.741 4.84552 26.741 10.006C26.741 15.1665 22.541 19.3665 17.3805 19.3665ZM17.3805 3.08738C13.5712 3.08738 10.4619 6.19669 10.4619 10.006C10.4619 13.8153 13.5712 16.9246 17.3805 16.9246C21.1898 16.9246 24.2991 13.8153 24.2991 10.006C24.2991 6.19669 21.1898 3.08738 17.3805 3.08738Z" fill="currentColor" />
            <path d="M23.5987 35.6466C22.98 35.6466 22.394 35.4187 21.9707 34.9954C21.4661 34.4908 21.2382 33.7582 21.3521 32.9931L21.6614 30.7954C21.7428 30.2256 22.0847 29.5582 22.4917 29.1349L28.2545 23.3721C30.5661 21.0605 32.601 22.3791 33.594 23.3721C34.4405 24.2186 34.8801 25.1303 34.8801 26.0419C34.8801 26.9698 34.4568 27.8326 33.594 28.6954L27.8311 34.4582C27.4241 34.8652 26.7405 35.2071 26.1708 35.2885L23.9729 35.5976C23.8427 35.6302 23.7289 35.6466 23.5987 35.6466ZM30.908 24.528C30.615 24.528 30.3545 24.7233 29.9801 25.0977L24.2173 30.8605C24.1684 30.9094 24.087 31.0722 24.087 31.1373L23.794 33.1722L25.8289 32.8791C25.894 32.8629 26.0566 32.7815 26.1055 32.7326L31.8684 26.9698C32.1289 26.7094 32.4382 26.3349 32.4382 26.0419C32.4382 25.7977 32.2429 25.4559 31.8684 25.0977C31.4777 24.707 31.1847 24.528 30.908 24.528Z" fill="currentColor" />
            <path d="M31.9026 29.9002C31.7887 29.9002 31.6747 29.8841 31.577 29.8515C29.4282 29.2492 27.7189 27.5399 27.1166 25.391C26.9375 24.7398 27.3119 24.0724 27.9631 23.8933C28.6142 23.7143 29.2817 24.0887 29.4608 24.7398C29.8352 26.0747 30.8933 27.1329 32.2282 27.5073C32.8794 27.6864 33.2538 28.3701 33.0747 29.005C32.9282 29.5422 32.4398 29.9002 31.9026 29.9002Z" fill="currentColor" />
            <path d="M3.39681 35.6468C2.72936 35.6468 2.17587 35.0933 2.17587 34.4259C2.17587 27.4747 8.99686 21.8096 17.3806 21.8096C19.1551 21.8096 20.9132 22.07 22.5574 22.5584C23.2086 22.7538 23.5667 23.4375 23.3714 24.0724C23.176 24.7235 22.4923 25.0817 21.8574 24.8863C20.4248 24.4631 18.9272 24.2352 17.3806 24.2352C10.348 24.2352 4.61774 28.7933 4.61774 34.4096C4.61774 35.0933 4.06425 35.6468 3.39681 35.6468Z" fill="currentColor" />
        </g>
    </svg>
);

const COMPARISON_DATA: ComparisonRow[] = [
    {
        platform: "groowy",
        description: "An AI-powered platform that guides candidates to their goals and provides employers with a pool of proven talent.",
        icon: <Logo />,
        speed: true,
        flexibility: true,
        quality: true,
        scalability: true,
        affordable: true,
        isHighlighted: true,
    },
    {
        platform: "Traditional Job Boards",
        description: "Massive networks that match resumes to listings. Relies on a candidate's past self-reported claims.",
        icon: <TeamIcon />,
        speed: false,
        flexibility: false,
        quality: false,
        scalability: true,
        affordable: true,
    },
    {
        platform: "Online Course Sites",
        description: "A giant digital course library. Users must find their own path. Completely disconnected from the hiring process.",
        icon: <BrushIcon />,
        speed: true,
        flexibility: true,
        quality: false,
        scalability: true,
        affordable: false,
    },
    {
        platform: "Bootcamps",
        description: "Human-led, intensive programs that train small cohorts and place them in partner companies.",
        icon: <FreelancerIcon />,
        speed: true,
        flexibility: false,
        quality: true,
        scalability: false,
        affordable: false,
    },
];

const CheckIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 40 41" fill="none" className="w-6 h-6">
        <path d="M35.8843 12.2796L15.8843 32.2796C15.7682 32.3958 15.6304 32.488 15.4786 32.5509C15.3269 32.6138 15.1642 32.6462 15 32.6462C14.8357 32.6462 14.673 32.6138 14.5213 32.5509C14.3695 32.488 14.2317 32.3958 14.1156 32.2796L5.36559 23.5296C5.13104 23.2951 4.99927 22.9769 4.99927 22.6452C4.99927 22.3135 5.13104 21.9954 5.36559 21.7609C5.60014 21.5263 5.91826 21.3945 6.24996 21.3945C6.58167 21.3945 6.89979 21.5263 7.13434 21.7609L15 29.628L34.1156 10.5109C34.3501 10.2763 34.6683 10.1445 35 10.1445C35.3317 10.1445 35.6498 10.2763 35.8843 10.5109C36.1189 10.7454 36.2507 11.0635 36.2507 11.3952C36.2507 11.7269 36.1189 12.0451 35.8843 12.2796Z" fill="currentColor" />
    </svg>
);

const CrossIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 40 41" fill="none" className="w-6 h-6">
        <path d="M32.1344 30.5109C32.2505 30.627 32.3427 30.7649 32.4055 30.9166C32.4684 31.0683 32.5007 31.231 32.5007 31.3952C32.5007 31.5595 32.4684 31.7221 32.4055 31.8738C32.3427 32.0256 32.2505 32.1635 32.1344 32.2796C32.0183 32.3957 31.8804 32.4879 31.7286 32.5507C31.5769 32.6136 31.4143 32.6459 31.25 32.6459C31.0858 32.6459 30.9231 32.6136 30.7714 32.5507C30.6197 32.4879 30.4818 32.3957 30.3657 32.2796L20 21.9124L9.6344 32.2796C9.39985 32.5142 9.08173 32.6459 8.75002 32.6459C8.41832 32.6459 8.1002 32.5142 7.86565 32.2796C7.6311 32.0451 7.49933 31.7269 7.49933 31.3952C7.49933 31.0635 7.6311 30.7454 7.86565 30.5109L18.2328 20.1452L7.86565 9.7796C7.6311 9.54505 7.49933 9.22693 7.49933 8.89523C7.49933 8.56352 7.6311 8.2454 7.86565 8.01085C8.1002 7.7763 8.41832 7.64453 8.75002 7.64453C9.08173 7.64453 9.39985 7.7763 9.6344 8.01085L20 18.378L30.3657 8.01085C30.6002 7.7763 30.9183 7.64453 31.25 7.64453C31.5817 7.64453 31.8998 7.7763 32.1344 8.01085C32.369 8.2454 32.5007 8.56352 32.5007 8.89523C32.5007 9.22693 32.369 9.54505 32.1344 9.7796L21.7672 20.1452L32.1344 30.5109Z" fill="currentColor" />
    </svg>
);

export default function ComparisonTable() {
    return (
        <section className="w-full mx-auto py-20 overflow-hidden max-w-5xl">
            {/* Header */}
            <div className="text-center mb-12">
                <div className="inline-block px-4 py-2 bg-gray-100 rounded-full mb-4">
                    <span className="text-sm font-medium text-gray-700">Why Choose Us</span>
                </div>
                <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    <span className="bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">groowy's</span> Alternative?
                    <br />
                    <span className="bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Think</span> One More Time!
                </h2>
            </div>

            {/* Table Container - Stack layout for better mobile support */}
            <div className="max-w-6xl mx-auto">
                {/* Desktop: Header Row */}
                <div className="hidden lg:flex items-center mb-6 px-6">
                    <div className="w-[45%]">
                        <h6 className="text-xs font-bold text-gray-900 uppercase tracking-wider">Platform</h6>
                    </div>
                    <div className="flex-1 flex justify-around">
                        <h6 className="text-xs font-bold text-gray-900 uppercase tracking-wider text-center">Speed</h6>
                        <h6 className="text-xs font-bold text-gray-900 uppercase tracking-wider text-center">Flexibility</h6>
                        <h6 className="text-xs font-bold text-gray-900 uppercase tracking-wider text-center">Quality</h6>
                        <h6 className="text-xs font-bold text-gray-900 uppercase tracking-wider text-center">Scalability</h6>
                        <h6 className="text-xs font-bold text-gray-900 uppercase tracking-wider text-center">Affordable</h6>
                    </div>
                </div>

                {/* Data Rows */}
                <div className="space-y-4">
                    {COMPARISON_DATA.map((row, index) => (
                        <div key={index}>
                            {/* Desktop View */}
                            <div
                                className={`hidden lg:flex items-center gap-6 px-6 py-6 rounded-2xl transition-all duration-300 ${row.isHighlighted
                                    ? "bg-linear-to-r from-blue-50 via-purple-50 to-blue-50 border-2 border-blue-200 shadow-lg relative"
                                    : "bg-gray-900 hover:bg-gray-800"
                                    }`}
                            >
                                {/* Platform Info - 45% width */}
                                <div className="w-[45%] flex items-center gap-4">
                                    <div className={`shrink-0 p-3 rounded-xl ${row.isHighlighted ? "bg-white text-gray-900" : "bg-blue-500/10 text-blue-400"
                                        }`}>
                                        {row.icon}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <h3 className={`text-lg font-bold mb-1 ${row.isHighlighted ? "text-gray-900" : "text-white"
                                            }`}>
                                            {row.platform}
                                        </h3>
                                        <p className={`text-sm leading-relaxed ${row.isHighlighted ? "text-gray-600" : "text-gray-400"
                                            }`}>
                                            {row.description}
                                        </p>
                                    </div>
                                </div>

                                {/* Feature Columns - remaining space divided equally */}
                                <div className="flex-1 flex justify-around items-center">
                                    <div className={`${row.speed
                                        ? (row.isHighlighted ? "text-green-600" : "text-green-400")
                                        : (row.isHighlighted ? "text-red-600" : "text-red-400")
                                        }`}>
                                        {row.speed ? <CheckIcon /> : <CrossIcon />}
                                    </div>
                                    <div className={`${row.flexibility
                                        ? (row.isHighlighted ? "text-green-600" : "text-green-400")
                                        : (row.isHighlighted ? "text-red-600" : "text-red-400")
                                        }`}>
                                        {row.flexibility ? <CheckIcon /> : <CrossIcon />}
                                    </div>
                                    <div className={`${row.quality
                                        ? (row.isHighlighted ? "text-green-600" : "text-green-400")
                                        : (row.isHighlighted ? "text-red-600" : "text-red-400")
                                        }`}>
                                        {row.quality ? <CheckIcon /> : <CrossIcon />}
                                    </div>
                                    <div className={`${row.scalability
                                        ? (row.isHighlighted ? "text-green-600" : "text-green-400")
                                        : (row.isHighlighted ? "text-red-600" : "text-red-400")
                                        }`}>
                                        {row.scalability ? <CheckIcon /> : <CrossIcon />}
                                    </div>
                                    <div className={`${row.affordable
                                        ? (row.isHighlighted ? "text-green-600" : "text-green-400")
                                        : (row.isHighlighted ? "text-red-600" : "text-red-400")
                                        }`}>
                                        {row.affordable ? <CheckIcon /> : <CrossIcon />}
                                    </div>
                                </div>

                                {/* Glow Effects for Highlighted Row */}
                                {row.isHighlighted && (
                                    <>
                                        <div className="absolute -right-4 top-1/2 -translate-y-1/2 w-32 h-32 bg-blue-400/20 rounded-full blur-3xl pointer-events-none" />
                                        <div className="absolute -left-4 top-1/2 -translate-y-1/2 w-32 h-32 bg-purple-400/20 rounded-full blur-3xl pointer-events-none" />
                                    </>
                                )}
                            </div>

                            {/* Mobile View */}
                            <div className={`lg:hidden px-6 py-6 rounded-2xl ${row.isHighlighted
                                ? "bg-linear-to-r from-blue-50 via-purple-50 to-blue-50 border-2 border-blue-200 shadow-lg"
                                : "bg-gray-900"
                                }`}>
                                <div className="flex items-start gap-4 mb-4">
                                    <div className={`shrink-0 p-3 rounded-xl ${row.isHighlighted ? "bg-white text-gray-900" : "bg-blue-500/10 text-blue-400"
                                        }`}>
                                        {row.icon}
                                    </div>
                                    <div>
                                        <h3 className={`text-lg font-bold mb-1 ${row.isHighlighted ? "text-gray-900" : "text-white"
                                            }`}>
                                            {row.platform}
                                        </h3>
                                        <p className={`text-sm leading-relaxed ${row.isHighlighted ? "text-gray-600" : "text-gray-400"
                                            }`}>
                                            {row.description}
                                        </p>
                                    </div>
                                </div>
                                <div className="grid grid-cols-2 gap-3 text-sm">
                                    <div className="flex items-center justify-between">
                                        <span className={row.isHighlighted ? "text-gray-700 font-medium" : "text-gray-300 font-medium"}>Speed</span>
                                        <div className={row.speed ? "text-green-600" : "text-red-600"}>
                                            {row.speed ? <CheckIcon /> : <CrossIcon />}
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className={row.isHighlighted ? "text-gray-700 font-medium" : "text-gray-300 font-medium"}>Flexibility</span>
                                        <div className={row.flexibility ? "text-green-600" : "text-red-600"}>
                                            {row.flexibility ? <CheckIcon /> : <CrossIcon />}
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className={row.isHighlighted ? "text-gray-700 font-medium" : "text-gray-300 font-medium"}>Quality</span>
                                        <div className={row.quality ? "text-green-600" : "text-red-600"}>
                                            {row.quality ? <CheckIcon /> : <CrossIcon />}
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <span className={row.isHighlighted ? "text-gray-700 font-medium" : "text-gray-300 font-medium"}>Scalability</span>
                                        <div className={row.scalability ? "text-green-600" : "text-red-600"}>
                                            {row.scalability ? <CheckIcon /> : <CrossIcon />}
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between col-span-2">
                                        <span className={row.isHighlighted ? "text-gray-700 font-medium" : "text-gray-300 font-medium"}>Affordable</span>
                                        <div className={row.affordable ? "text-green-600" : "text-red-600"}>
                                            {row.affordable ? <CheckIcon /> : <CrossIcon />}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
