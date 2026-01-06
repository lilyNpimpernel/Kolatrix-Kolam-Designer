document.addEventListener("DOMContentLoaded", function() {
  const canvas = document.getElementById("kolamCanvas");
  const ctx = canvas.getContext("2d");
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;

  const circles = 3;         
  const dotsPerCircle = 12;  
  const step = 3;            // fixed step for symmetry
  const lineColor = "#be185d";
  const dotColor = "#be185d";
  const dotRadius = 4;

  let patternLines = [];
  let animationIndex = 0;

  function getCircleDots(radius, n) {
    const dots = [];
    for (let i = 0; i < n; i++) {
      const angle = (i * 2 * Math.PI) / n;
      dots.push({
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      });
    }
    return dots;
  }

  function generateKolam() {
    patternLines = [];
    animationIndex = 0;
    const spacing = 50;

    for (let c = 1; c <= circles; c++) {
        const radius = c * spacing;
        const dots = getCircleDots(radius, dotsPerCircle);
        const step = Math.floor(Math.random() * 4) + 2; // random step 2..5
        const rotation = Math.random() * 2 * Math.PI; // random rotation

        for (let i = 0; i < dotsPerCircle; i++) {
            const j = (i + step) % dotsPerCircle;
            const p1 = {
                x: centerX + radius * Math.cos((i * 2 * Math.PI) / dotsPerCircle + rotation),
                y: centerY + radius * Math.sin((i * 2 * Math.PI) / dotsPerCircle + rotation),
            };
            const p2 = {
                x: centerX + radius * Math.cos((j * 2 * Math.PI) / dotsPerCircle + rotation),
                y: centerY + radius * Math.sin((j * 2 * Math.PI) / dotsPerCircle + rotation),
            };
            patternLines.push([p1, p2]);
        }
    }
}

  function drawKolam() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Central dot
    ctx.beginPath();
    ctx.arc(centerX, centerY, dotRadius + 2, 0, Math.PI * 2);
    ctx.fillStyle = dotColor;
    ctx.fill();

    for (let i = 0; i < animationIndex; i++) {
      const line = patternLines[i];
      ctx.beginPath();
      ctx.moveTo(line[0].x, line[0].y);
      ctx.lineTo(line[1].x, line[1].y);
      ctx.strokeStyle = lineColor;
      ctx.lineWidth = 2;
      ctx.stroke();

      [line[0], line[1]].forEach(dot => {
        ctx.beginPath();
        ctx.arc(dot.x, dot.y, dotRadius, 0, Math.PI * 2);
        ctx.fillStyle = dotColor;
        ctx.fill();
      });
    }

    if (animationIndex < patternLines.length) {
      animationIndex++;
      requestAnimationFrame(drawKolam);
    }
  }

  document.getElementById("generateKolam").addEventListener("click", () => {
    generateKolam();
    drawKolam();
  });

  generateKolam();
  drawKolam();
});



