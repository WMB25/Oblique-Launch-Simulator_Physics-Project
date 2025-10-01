let angle_arrow;
let height_arrow;
let velocity_slider;
let drag_slider;
let mass_slider;

const initial_line_x = 15;
const final_line_y = 700;
const line_lenght = 100;

let velocity = 100;
let gravity = 9.8;
let time = 0;
let launched = false;
let drag_coefficient = 0.01;
let mass = 1;

let pos_x, pos_y;
let vx, vy;
let trajectory = [];

function setup() {
  createCanvas(2000, 720);

  angle_arrow = createSlider(-180, 180, 45);   
  height_arrow = createSlider(50, 700, 700);  
  velocity_slider = createSlider(10, 200, 100);
  drag_slider = createSlider(0,100, 1);
  mass_slider = createSlider(1, 20, 1);

  angle_arrow.position(10, 10);
  height_arrow.position(10, 40);
  velocity_slider.position(270, 10);
  drag_slider.position(270, 40);
  
  button = createButton("Lançar");
  button.mousePressed(start_launch);
}

function draw() {
  Draw_cartesian_plan();
  draw_arrow();

  drag_coefficient = pow(10, map(drag_slider.value(), 0, 100, -3, -0.5));
  
  if (launched) {
    Simulate_projectile();
  }
  
  Shoe_labels();
}

function Draw_cartesian_plan() {
  background(17,17,132);

  stroke(254, 255, 250);
  // y
  line(15, 700, 15, 50);
  // X
  line(15, 700, 1190, 700);
}

function draw_arrow() {
  let angle_degrees = angle_arrow.value();
  let angle_radians = radians(angle_degrees);
  let launch_height = height_arrow.value();

  let arrow_pos_x = initial_line_x + line_lenght * cos(angle_radians);
  let arrow_pos_y = launch_height - line_lenght * sin(angle_radians);
  
  stroke(254, 255, 250);
  line(initial_line_x, launch_height, arrow_pos_x, arrow_pos_y);

  fill(255);
  circle(initial_line_x, launch_height, 25);
}

function start_launch() {
  time = 0;
  launched = true;
  trajectory = [];

  let angle_radians = radians(angle_arrow.value());
  pos_x = initial_line_x;
  pos_y = height_arrow.value();
  
  velocity = velocity_slider.value();
  vx = velocity * cos(angle_radians);
  vy = -velocity * sin(angle_radians);
}

function Simulate_projectile() {
  let dt = 0.1;
  time += dt;

  let v = sqrt(vx*vx + vy*vy);
  
  let drag_x = -drag_coefficient * vx * v;
  let drag_y = -drag_coefficient * vy * v;

  let ax = drag_x/mass;
  let ay = (mass * gravity + drag_y)/ mass;

  vx += ax * dt;
  vy += ay * dt;

  pos_x += vx * dt;
  pos_y += vy * dt;

  trajectory.push({ x: pos_x, y: pos_y });

  stroke(255, 255, 0);
  noFill();
  beginShape();
  for (let p of trajectory) {
    vertex(p.x, p.y);
  }
  endShape();

  fill(255);
  noStroke();
  circle(pos_x, pos_y, 20);

  if (pos_y >= final_line_y) {
    launched = false;
  }
}

function Shoe_labels()
{
  fill(255);
  noStroke();
  textSize(16);

  text("Ângulo: " + angle_arrow.value() + "°", angle_arrow.x * 2 + angle_arrow.width, 25);
  text("Altura: " + height_arrow.value() + " px", height_arrow.x * 2 + height_arrow.width, 55);
  text("Velocidade: " + velocity_slider.value() + " m/s", velocity_slider.x + velocity_slider.width + 10, velocity_slider.y + 15);
  text("Arrasto: " + nf(drag_coefficient, 1, 3), drag_slider.x + drag_slider.width + 10, drag_slider.y + 15);
  text("Massa: " + mass_slider.value() + "kg", mass_slider.x + mass_slider.width + 10, mass_slider.y + 15);
  
  let v = sqrt(vx*vx + vy*vy);
  let force = mass * sqrt((drag_coefficient * vx * v)**2 + (mass*gravity + drag_coefficient * vy * v)**2);
  
  let kinetic = 0.5 * mass * v * v;
  let height = final_line_y - pos_y;
  let potential = mass * gravity * height;
  let total_energy = kinetic + potential;

  text("Força resultante: " + nf(force, 1, 2) + " N", 600, 25);
  text("Energia Cinética: " + nf(kinetic, 1, 2) + " J", 600, 45);
  text("Energia Potencial: " + nf(potential, 1, 2) + " J", 600, 65);
  text("Energia Mecânica: " + nf(total_energy, 1, 2) + " J", 600, 85);

}
