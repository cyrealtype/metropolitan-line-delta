// Metropolitan Line - Non-linear weight curve
// Regular=400 maps to 0.25 (not 0.43 linear)
// Result: light weights stay thin, bold weights thicken fast

const measurements = {
  weightMap: [
    [400, 0.25],   // Regular master
    [500, 0.40],
    [600, 0.60],
    [700, 0.78],
    [800, 0.92],
    [900, 1.0]     // Bold master
  ]
};

module.exports = measurements;