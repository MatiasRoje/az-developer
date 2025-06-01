// Azure Design System Color Palette
// Based on Microsoft's official Azure design guidelines
const azColors = {
  primary: "#0078D4", // Fixed syntax error - Azure Blue
  
  // Primary color variations (tints and shades)
  blue: {
    50: "#F4F9FF",   // Lightest tint
    100: "#E1F0FF",  // Very light
    200: "#C7E0F4",  // Light (your current medium)
    300: "#A3D1FF",  // Medium light
    400: "#69B7FF",  // Medium
    500: "#0078D4",  // Primary Azure Blue
    600: "#106EBE",  // Medium dark
    700: "#005A9E",  // Dark
    800: "#004B8D",  // Darker (your current dark)
    900: "#003F75",  // Darkest
    950: "#002952",  // Deepest
  },
  
  // Neutral grays that work well with Azure Blue
  gray: {
    50: "#FAFAFA",   // Almost white
    100: "#F5F5F5",  // Very light gray
    200: "#E5E5E5",  // Light gray
    300: "#D4D4D4",  // Medium light gray
    400: "#A3A3A3",  // Medium gray
    500: "#737373",  // True gray
    600: "#525252",  // Medium dark gray
    700: "#404040",  // Dark gray
    800: "#262626",  // Very dark gray
    900: "#171717",  // Almost black
    950: "#0A0A0A",  // Deep black
  },
  
  // Semantic colors following Azure conventions
  semantic: {
    success: "#13A10E",    // Azure green
    warning: "#FF8C00",    // Azure orange
    error: "#D13438",      // Azure red
    info: "#0078D4",       // Same as primary
  }
};

export { azColors };