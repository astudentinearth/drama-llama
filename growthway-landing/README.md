# Groowy Landing Page

A modern, animated landing page for Groowy - an AI-powered career growth platform that connects skills with their future opportunities.

## 🚀 Project Overview

Groowy is a comprehensive platform that provides personalized growth paths and smarter hiring solutions. This landing page serves as the marketing frontend, showcasing the platform's capabilities and encouraging user sign-ups.

### Key Features

- **AI-Powered Career Growth**: Personalized skill development paths
- **Smart Hiring Solutions**: Connect talented individuals with opportunities
- **Company Integration**: Tools for organizations to find and nurture talent
- **Individual Development**: Personal career roadmap creation and tracking

## 🎨 Landing Page Sections

### Hero Section
- Animated typewriter effect with tagline: "Where skills meet their future"
- Call-to-action buttons for individual and company sign-ups
- Modern gradient backgrounds and hover effects

### Client Showcase
- Animated logo marquee featuring partner companies
- Includes Meta, Ollama, and YTU Startup logos

### AI-Powered Features
- Interactive chart visualization
- Highlighted AI capabilities with pointer effects
- Motion animations for engagement

### Pricing Plans
- Multiple subscription tiers (Free, Starter, Premium, Enterprise)
- Visual plan comparison with feature highlights
- Responsive design for all screen sizes

### Comparison Table
- Detailed feature comparison across plans
- Interactive elements for better user experience

### Call-to-Action
- Roadmap creation invitation
- Integrated with main application flow

## 🛠️ Tech Stack

- **React 19** - Latest React with modern features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations and transitions
- **Lucide React** - Beautiful icon library
- **React Fast Marquee** - Smooth scrolling animations

## 📦 Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/astudentinearth/drama-llama.git
   cd drama-llama/growthway-landing
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open in browser**
   Navigate to `http://localhost:5173`

## 🏗️ Build & Deployment

### Development Build
```bash
npm run build
# or
yarn build
```

### Preview Production Build
```bash
npm run preview
# or
yarn preview
```

### Deployment Options
- **Static Hosting**: Deploy `dist/` folder to Vercel, Netlify, or GitHub Pages
- **CDN**: Upload to AWS S3, CloudFront, or similar CDN service
- **Docker**: Containerize for container orchestration platforms

## 📁 Project Structure

```
growthway-landing/
├── public/                 # Static assets
│   ├── logo.png           # Main Groowy logo
│   ├── chart.png          # AI features visualization
│   ├── graph.png          # Additional graphics
│   └── logos/             # Partner company logos
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── ui/           # Base UI components
│   │   ├── topbar.tsx    # Navigation top bar
│   │   ├── footer.tsx    # Page footer
│   │   ├── plans-section.tsx    # Pricing plans
│   │   └── comparison-table.tsx # Feature comparison
│   ├── contexts/         # React contexts
│   ├── lib/              # Utility functions
│   └── App.tsx           # Main application component
├── package.json          # Dependencies and scripts
└── vite.config.ts        # Vite configuration
```

## 🔗 Integration with Main Application

The landing page integrates with the main Groowy application through:

- **Authentication Flow**: Sign-up buttons redirect to `/app` for user registration
- **Company Onboarding**: Company sign-up flow connects to backend services
- **API Integration**: Connects to backend services for user management
- **Shared Assets**: Uses consistent branding and design system

## 🚀 Getting Started

1. **Development**: Run `npm run dev` to start the development server
2. **Customization**: Modify components in `src/components/` to update content
3. **Styling**: Use Tailwind classes or modify `src/index.css` for global styles
4. **Assets**: Replace images in `public/` directory with your own branding

## 📝 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint for code quality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Groowy platform. See the main project repository for licensing information.
