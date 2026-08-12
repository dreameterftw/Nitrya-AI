module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        western: {
          bg: "#0A0A0F",
          accent: "#FF3D5A",
          text: "#FFFFFF",
        },
        indian: {
          bg: "#FDF6EC",
          accent: "#B5651D",
          text: "#2A1A0F",
        },
      },
    },
  },
  plugins: [],
};
