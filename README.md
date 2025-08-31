# Hedamo Product Showcase

A modern, responsive product showcase web application built with Next.js 13, TypeScript, and Tailwind CSS. This application displays a collection of Hedamo products with beautiful card-based layouts, smooth animations, and a seamless user experience.

## Features

- 🚀 Built with Next.js 13 App Router and React Server Components
- 🎨 Styled with Tailwind CSS for a beautiful, responsive design
- ✨ Smooth animations and micro-interactions with Framer Motion
- 🔍 Full-text search and category filtering
- 📱 Fully responsive layout for all device sizes
- ♿ Accessible UI components with proper ARIA labels
- ⚡ Optimized performance with code splitting and lazy loading
- 🔄 Real-time search and filtering without page reloads

## Prerequisites

- Node.js 18.0.0 or later
- npm 9.x or later, or yarn 1.22.x or later
- Git for version control

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/product-showcase.git
   cd product-showcase
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

```
src/
├── app/                  # App router pages and layouts
│   ├── products/         # Product-related pages
│   │   └── [id]/         # Dynamic product detail pages
│   └── globals.css       # Global styles
├── components/           # Reusable UI components
│   ├── ProductCard.tsx   # Product card component
│   └── ProductSearch.tsx # Search and filter component
├── data/                 # Static data and types
│   └── products.ts       # Product data and types
└── lib/                  # Utility functions
```

## Deployment

### Vercel (Recommended)

1. Push your code to a GitHub, GitLab, or Bitbucket repository
2. Sign in to [Vercel](https://vercel.com)
3. Click "Add New..." > "Project"
4. Import your repository
5. Configure project settings (leave defaults for most cases)
6. Click "Deploy"

### Manual Deployment

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Build the project:
   ```bash
   npm run build
   ```

3. Deploy to Vercel:
   ```bash
   vercel --prod
   ```
   
   Or use the deployment script:
   ```bash
   .\deploy-vercel.cmd
   ```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run check-types` - Run TypeScript type checking

## Technologies Used

- [Next.js](https://nextjs.org/) - React framework
- [TypeScript](https://www.typescriptlang.org/) - Type checking
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Framer Motion](https://www.framer.com/motion/) - Animations
- [Heroicons](https://heroicons.com/) - Icons

## Deployment

The easiest way to deploy this application is to use [Vercel](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by modern e-commerce and product showcase designs
- Built with the latest web technologies for optimal performance
